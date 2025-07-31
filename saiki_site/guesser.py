"""
backend/saiki_site/guesser.py

...
"""

from __future__ import annotations

from dataclasses import dataclass
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from saiki_data.entities import HistoricalEntity
from saiki_data.database import saiki_entities
from core.enc import int_list_to_b64, b64_to_int_list, permute, unpermute, generate_key


@dataclass(init=True, repr=True, eq=False, frozen=False, slots=True)
class GuessState:
    """Represents the state of the player in the Guess game mode."""

    key: str  # the player's session id
    selected: None | int  # a pointer to the entity currently selected
    attempted: list[int]  # already guessed...

    @staticmethod
    def from_request(request: WSGIRequest) -> GuessState:
        """Retrieves the Player's guessing state by the request.

        :param request: The Django request.
        :return: The user's guessing state. Creates a new if it doesn't identify one.
        """

        key: None | str = request.COOKIES.get("key")

        if key is None:
            key: str = generate_key()
            assert len(key) == 64

        selected: None | str = request.COOKIES.get("selected")

        try:
            selected: int = int(selected)

        except TypeError:
            # couldn't make the casting...
            pass

        try:
            b64_array: str = request.COOKIES.get("A#")
            if not b64_array:
                raise TypeError

            attempted: list[int] = b64_to_int_list(b64_array, 4)

        except TypeError:
            attempted: list[int] = []

        print(f"COOKIE GET. key: {key} ({type(key)}); selected: {selected} ({type(selected)}); attempted: {attempted}")

        return GuessState(
            key, selected, attempted
        )

    def set_cookie(self, response_json: JsonResponse, reset: bool = False) -> JsonResponse:
        """Set the cookies reply on the json response.
            :param response_json: The Json response the cookies will be set to.
            :param reset: If to reset the cookies."""

        if reset:
            response_json.delete_cookie("key", samesite="Lax")
            response_json.delete_cookie("selected", samesite="Lax")
            response_json.delete_cookie("A#", samesite="Lax")

            return response_json

        response_json.set_cookie("key", self.key, secure=False, httponly=True, samesite="Lax")
        response_json.set_cookie("selected", self.selected, secure=False, httponly=True, samesite="Lax")

        """
        from .enc import int_to_base64
        for i, v in enumerate(self.attempted):
            b64_v: str = int_to_base64(v, 4)
            response_json.set_cookie(f"A#", b64_v, secure=False, httponly=True, samesite="Lax")
        """
        response_json.set_cookie(f"A#", int_list_to_b64(self.attempted, 4), secure=False, httponly=True, samesite="Lax")

        return response_json

    def add_attempt(self, attempt_index: int) -> None:
        """..."""

        if not isinstance(attempt_index, int):
            raise TypeError

        self.attempted.append(
            permute(attempt_index, self.key, 1000)
        )

        return None

    @property
    def __real_indexes(self) -> list[int]:
        return list(map(lambda x: unpermute(x, self.key, 1000), self.attempted))

    @property
    def attempted_names(self) -> list[str]:
        real_indexes: list[int] = self.__real_indexes
        return list(map(
            lambda index: saiki_entities[index]["name"], real_indexes
        ))

    def get_collection(self, _: dict) -> JsonResponse:
        """Returns all the entity data serialized."""

        real_indexes: list[int] = self.__real_indexes

        # will hold the JSON data in python.
        response_list: list[dict] = list()

        # retrieving the data.
        for index in real_indexes:
            entity = saiki_entities[index]

            response = self.__check_entity(entity_name=entity["name"])

            response_list.append(
                response
            )

        return JsonResponse({
            "tries": len(response_list),
            "entities": response_list,
        })

    def __check_entity(self, entity_name: str) -> dict:
        """Checks the fields of the player's guessing. Returns the JSON format response (as a dictionary).

        :param entity_name: Name of the entity being guessed.
        :returns: Entity's guessing response in JSON format."""

        # making sure the state have a selected entity.
        guesser.select_entity(self)

        # the entity that is marked to be solved by the player.
        real_selected_index: int = unpermute(self.selected, self.key, 1000)
        correct_entity: HistoricalEntity = saiki_entities[real_selected_index]

        # the one matching what he inserted.
        match_entity: HistoricalEntity
        match_entity_index: int

        # will hold the JSON response back to the user.
        response: dict = {}

        try:
            match_entity, match_entity_index = guesser.fetch(entity_name)

        except KeyError as ke:
            # couldn't find the entity. returns empty.
            print(f"COULDN'T FIND!", ke)
            return response

        # at least it was found on the database...
        
        response: dict = {
            "name": match_entity["name"],
            "data": {},
            "guessed": "correct"
        }

        checked: dict[str, tuple[list[str], str]] = match_entity.check(correct_entity)

        # iterating over the entity data fields...
        for field, value in checked.items():
            response["data"][field] = value
            guess_type: str = value[1]

            if response["guessed"] == "correct":
                # if the response is correct up to now, it can potentially make the whole answer wrong.
                response["guessed"] = guess_type

            elif response["guessed"] == "partial" and guess_type != "correct":
                # else, it can either be partial or wrong.
                response["guessed"] = guess_type

            # wrong will be wrong...

        self.add_attempt(match_entity_index)
        return response

    def guess(self, entity_name: str) -> JsonResponse:
        """Checks the fields of the player's guessing. Updates the guessing state (through the response).

        :param entity_name: Name of the entity being guessed.
        :returns: Returns the entity guessing response."""

        response = self.__check_entity(entity_name)
        response_json: JsonResponse = JsonResponse(response)

        to_reset_cookies: bool = response["guessed"] == "correct" if "guessed" in response else False
        self.set_cookie(response_json, to_reset_cookies)

        return response_json


class Guesser(object):
    """Handles the `Guess` game mode inner logical structure.

    Obs: Currently, most stateless."""

    def __init__(self) -> None:
        """Initializes the guesser state."""

        ...

    @staticmethod
    def fetch(entity_name: str) -> tuple[HistoricalEntity, int]:
        """Fetches an entity by its name on the data pool. Stateless."""

        entity_name: str = entity_name.lower()
        return saiki_entities.fetch_entity(entity_name)

    @staticmethod
    def select_entity(state: GuessState) -> GuessState:
        """Collapses the entity selection; chooses one from the data pool as the correct.
            :param state: The current player's guess mode state.
            :return: the new state after the selection. The parameter is modified.

            As of now, it is stateless.
        """

        from random import randint

        if state.selected is not None:
            return state

        # choosing an entity at random; uniform distribution...
        state.selected = randint(0, len(saiki_entities) - 1)

        # encrypting it
        state.selected = permute(state.selected, state.key, 1000)

        return state

    @staticmethod
    def match_name(state: GuessState, name: str) -> list[str]:
        """Matches an entity name over the collection. Returns a list of possible results.

        Stateless."""

        from difflib import get_close_matches
        from typing import Iterable

        max_query_results: int = 5
        cutoff: float = 0.35

        attempt_names: list[str] = state.attempted_names
        name_list: Iterable[str] = filter(
            lambda x: x not in attempt_names,
            saiki_entities    # entity names.
        )
        matches: list[str] = get_close_matches(name, name_list, n=max_query_results, cutoff=cutoff)

        return matches


"""Global initialization"""

guesser: Guesser = Guesser()

if __name__ == "__main__":
    ...

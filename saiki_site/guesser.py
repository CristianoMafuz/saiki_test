"""
backend/saiki_site/guesser.py

...
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse


@dataclass(init=True, repr=True, eq=False, frozen=False, slots=True)
class GuessState:
    """Represents the state of the player in the Guess game mode."""

    key: str    # the player's session id
    selected: None | int    # a pointer to the entity currently selected
    attempted: list[int]  # already guessed...

    @staticmethod
    def from_request(request: WSGIRequest) -> GuessState:
        """Retrieves the Player's guessing state by the request."""

        key: None | str = request.COOKIES.get("key")

        if key is None:
            from .enc import generate_key
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

            from .enc import b64_to_int_list
            attempted: list[int] = b64_to_int_list(b64_array, 4)

        except TypeError:
            attempted: list[int] = []

        """
        attempted: list[int] = []
        iterator: int = 0
        while True:
            try:
                attempted.append(
                    int(request.COOKIES.get(f"attempt_{iterator}"))
                )
            except TypeError:
                break

            iterator += 1
        """

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
        from .enc import int_list_to_b64
        response_json.set_cookie(f"A#", int_list_to_b64(self.attempted, 4), secure=False, httponly=True, samesite="Lax")

        return response_json

    def add_attempt(self, attempt_index: int) -> None:
        if not isinstance(attempt_index, int):
            raise TypeError

        from .enc import permute
        self.attempted.append(
            permute(attempt_index, self.key, 1000)
        )

        return None


class Guesser(object):
    """Handles the Guess game mode inner logical structure."""

    __static_json_data_stream: list[dict]

    def __init__(self) -> None:
        """Initializes the guesser state."""

        from os import path

        data_path: str = path.join(path.dirname(__file__), "../../frontend/site/scripts/test.json")

        # Currently, the database fetch is mocked.
        with open(data_path, "r", encoding="utf-8") as file:
            self.__static_json_data_stream: list[dict] = json.load(file)

    def fetch_entity(self, entity_name: str) -> tuple[None | dict, int]:
        """Fetches an entity by its name on the data pool."""

        for i, entity in enumerate(self.__static_json_data_stream):
            # @TODO: to abstract and improve comparison!
            if entity["name"].lower() == entity_name:
                return entity, i

        return None, 0

    def select_entity(self, state: GuessState) -> GuessState:
        """Collapses the entity selection; chooses one from the data pool as the correct.
            :param state: The current player's guess mode state.
            :return: the new state after the selection. The parameter is modified.
        """
        from random import randint

        if state.selected is not None:
            return state

        # choosing an entity at random; uniform distribution...
        state.selected = randint(0, len(self.__static_json_data_stream) - 1)

        # encrypting it
        from .enc import permute
        state.selected = permute(state.selected, state.key, 1000)

        return state

    def get_entity(self, index: int) -> dict:
        """Retrieves an entity by its index in the data pool.
            :param index: The 0-based index.
            :return: The json dictionary associated with the entity entry.
            :raises TypeError: If the index is out of the bounds."""
        return self.__static_json_data_stream[index]


"""Global initialization"""

guesser: Guesser = Guesser()


if __name__ == "__main__":
    ...

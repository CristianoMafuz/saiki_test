"""
backend/saiki_site/database.py

Defines the databases interface.
Interaction externally to this module must be made via them.
"""

import json
from typing import Iterator, Iterable

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import ModelAlgorithm
from .entities import HistoricalEntity


class SaikiEntityDatabase(object):
    """Handles the historical-entity database for the project.
    @TODO: Singleton. Base-class."""

    __slots__: list[str] = [
        "__static_json_data_stream",
        "__entities",
        "__entity_names"
    ]

    __static_json_data_stream: list[dict]

    def __init__(self) -> None:

        # self.__load_entities()    # <- Deprecated
        # self.__load_static_json_data_stream() # <- Deprecated
        self.__load_entity_names()

    def __load_entity_names(self) -> None:
        """Step #3 in migrating to DB usage.

        Load all the entity names.
        Attempts improving entity name approximated name in the backend by caching them."""

        try:
            self.__entity_names: list[str] = list(map(lambda x: x.name, ModelAlgorithm.objects.all()))

        except Exception:
            self.__entity_names: list = list()

        print(self.__entity_names)

    def __load_entities(self) -> None:
        """Step #2 in migrating to DB usage. Obs: Deprecated."""

        try:
            __all_objects = list(ModelAlgorithm.objects.all())
            self.__entities = list(map(lambda x: x.to_historical_entity(), __all_objects))

        except Exception as e:
            # something went wrong.
            # @TODO: To identify the error.
            raise e

            self.__entities: list = list()

        print(self.__entities)

    def __load_static_json_data_stream(self) -> None:
        """Step #1 in migrating to DB usage. Obs: Deprecated."""

        # For mocked database results.
        from os import path
        data_path: str = path.join(path.dirname(__file__), "test.json")

        with open(data_path, "r", encoding="utf-8") as file:
            self.__static_json_data_stream: list[dict] = json.load(file)

        for entry in self.__static_json_data_stream:
            entry: dict = entry["data"]

            for data_field in entry:
                if not isinstance(entry[data_field], list):
                    # then we have to list it.
                    entry[data_field] = [entry[data_field]]

    def __len__(self) -> int:
        """Returns how many historical entities are there in the database."""
        return ModelAlgorithm.objects.count()

    def __getitem__(self, item: int) -> HistoricalEntity:
        """`get_entity()` callback. Retrieves an entity by its index."""
        if not isinstance(item, int):
            raise TypeError()

        return self.get_entity(index=item)
    
    def all(self) -> Iterable[HistoricalEntity]:
        return iter(ModelAlgorithm.objects.all())

    def get_entity(self, index: int) -> HistoricalEntity:
        """Retrieves an entity by its index in the data pool.
            :param index: The 0-based index.
            :return: The json dictionary associated with the entity entry.
            :raises IndexError: If the index is out of the bounds."""

        if index < 0 or index >= len(self):
            raise IndexError()

        # !! old.
        # return HistoricalEntity.from_json_mock_data(self.__static_json_data_stream[index])
        # return self.__entities[index]

        try:
            return ModelAlgorithm.objects.get(entity_id=index).to_historical_entity()

        except ObjectDoesNotExist or MultipleObjectsReturned:
            raise LookupError(f"DB Inconsistency")

    def fetch_entity(self, name: str) -> tuple[HistoricalEntity, int]:
        """Attempts finding an entity on the database. Returns it, as well as its index.
        Raises KeyError in case not finding."""

        try:
            the_model = ModelAlgorithm.objects.get(name__iexact=name)
            return ModelAlgorithm.objects.get(name__iexact=name).to_historical_entity(), the_model.entity_id

        except ObjectDoesNotExist:
            raise KeyError(f"Didn't found entity with name {name}.")

        except MultipleObjectsReturned:
            raise KeyError(f"DB Inconsistency")

        # !! old.
        for i, entity in enumerate(self.__entities):
            if entity["name"].lower() == name:
                # return HistoricalEntity.from_json_mock_data(entity), i
                return entity, i

        raise KeyError(f"Couldn't find entity with name '{name}'.")

    def __iter__(self) -> Iterator[HistoricalEntity]:
        """Iterates over all the entity names."""

        # @TODO: Replace mock with ModelAlgorithm interaction.
        # This method's behavior is mainly used for the entity name matching used in the guesser.
        # As such, it can be substituted for a direct such search in the database.

        def __generate_entities() -> Iterator[HistoricalEntity]:
            """Generator over the static mocked data."""
            for entity in self.__entity_names:
                yield entity

        return __generate_entities()


# Main Instantiation
# ------------------

saiki_entities: SaikiEntityDatabase = SaikiEntityDatabase()


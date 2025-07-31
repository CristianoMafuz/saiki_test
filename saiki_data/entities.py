"""
backend/saiki_site/entities.py

Stores the interface historical entities.
Interaction externally to this module must be made via them.
"""

from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Iterator, override


class HistoricalEntity(ABC):
    """Represents a historical-entity in the system."""

    _json_dict: dict[str, list]

    @property
    def name(self) -> str:
        """Retrieves the entity's name."""
        return self["name"]

    @property
    @abstractmethod
    def type_name(self) -> str:
        return "entity"

    def __repr__(self):
        return self.name

    @abstractmethod
    def __iter__(self) -> Iterator:
        """Iterates over the data fields of the entity."""

        # @TODO: Frontend is accounting for the keys in sorted order, such that the set approach doesn't work...
        # return iter(self._json_dict.keys() - {"name"})

    def __init__(self, name: str, ** kwargs) -> None:
        self._json_dict: dict[str, str | list] = {
            "name": name
        }

        for kw, v in kwargs.items():
            kw: str
            self._json_dict[kw]: str = v

    def __getitem__(self, item: str) -> str | list:
        """Returns the corresponding JSON item."""
        if not isinstance(item, str):
            raise TypeError

        return self._json_dict[item]

    def __matmul__(self, item: tuple[str, list]) -> str:
        """`compare_field` operator wrapper."""

        if not isinstance(item, tuple) and len(item) == 2 or not isinstance(item[1], list):
            raise TypeError(f"Item: {item}")

        return self.compare_field(* item)

    def compare_field(self, field_name: str, field_item: list[str]) -> str:
        """Compares two entities fields for guessing, verifying if A \\subseteq B.
        Let A be the parameter field and B be the corresponding on this object.
        Returns "correct", if A == B, "partial" if A \\subset B, and "wrong" otherwise."""

        if field_name not in self._json_dict:
            raise ValueError(f"field_name: {field_name} ({self._json_dict})")

        # A == B
        if field_item == self._json_dict[field_name]:
            return "correct"

        # A \\subset B
        for a in field_item:
            if a in self._json_dict[field_name]:
                return "partial"

        # A \\nsubset B
        return "wrong"

    def check(self, other: HistoricalEntity) -> dict[str, tuple[list[str], str]]:
        """Checks against other entity of the same type. So it does the comparison based on the assumption `other` is
        correct.
        :param other: Other compatible (should be at least of the same class as this) HistoricalEntity to compare with.
        :returns: A dictionary mapping the fields comparing to it check - if it is "correct", "wrong" or "partial"
        (ly correct)."""

        if not isinstance(other, self.__class__):
            raise TypeError()

        response: dict[str, tuple[list[str], str]] = {}

        for field in self:
            field: str

            # if the field is correct, for all effects.
            guess_type: str = other @ (field, self[field])

            # adding the respective field to the response...
            response[field] = self[field], guess_type

        return response

    @staticmethod
    def from_type(entity_type: str, *args, **kwargs) -> HistoricalEntity:
        """Returns an HistoricalEntity from the specified type."""

        possible_entities_type: dict[str, type] = {
            "algorithm": Algorithm,
        }
        
        if entity_type not in possible_entities_type:
            raise ValueError(f"Not a possible entity type.")

        # callbacks the type constructor.
        return possible_entities_type[entity_type](*args, **kwargs, )

    @staticmethod
    def from_json_mock_data(__json_data: dict) -> HistoricalEntity:
        """@TODO OBS: Mocked. Temporary."""
        return HistoricalEntity.from_type(__json_data["type"].lower(), __json_data["name"], **__json_data["data"])


class Algorithm(HistoricalEntity):
    """Represents the algorithm entity."""

    @property
    def type_name(self) -> str:
        return "algorithm"

    def __init__(self, name: str, ** kwargs) -> None:
        fields: list[str] = ["category", "year", "average_time_complexity", "auxiliary_space_complexity",
                             "data_structure", "kind_of_solution", "generality"]

        for key in kwargs:
            if key not in fields:
                raise KeyError(f"Invalid key: {key}")

            fields.pop(fields.index(key))

            if not isinstance(kwargs[key], list):
                kwargs[key] = [kwargs[key]]

        if fields:
            raise KeyError(f"Missing keys: {fields}")

        super().__init__(name, ** kwargs)

    @override
    def __iter__(self) -> Iterator:

        # !! The following approach is only valid while we do not know other entity than algorithms.
        return iter(["category", "year", "average_time_complexity", "auxiliary_space_complexity", "data_structure",
                     "kind_of_solution", "generality"])


if __name__ == "__main__":
    Algorithm("Victor's algorithm", category="cmrd", year=2025, average_time_complexity="O(n)",
              auxiliary_space_complexity="O(n)", data_structure="List", kind_of_solution="Just wrong",
              generality="Doidera")

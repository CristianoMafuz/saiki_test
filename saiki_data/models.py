"""
backend/saiki_data/models.py

System's database models.

For all effects, relies on Django's type.
"""

from __future__ import annotations

from django.db import models
from django.db.models import CharField, IntegerField
from django.http import JsonResponse
from . import entities


class SaikiDB_Manager(models.Manager):
    def get_queryset(self):
        # assuring that `saiki_data_db` is used for this model.
        return super().get_queryset().using("saiki_data_db")


class ModelAlgorithm(models.Model):
    """Represents an algorithm; the entity."""

    entity_id: IntegerField = IntegerField()

    name: CharField = CharField(max_length=32)
    year: IntegerField = IntegerField()

    category: CharField = CharField(max_length=32)
    design_paradigm: CharField = CharField(max_length=32)
    generality: CharField = CharField(max_length=32)
    data_structure: CharField = CharField(max_length=32)
    temporal_complexity: CharField = CharField(max_length=32)
    spatial_complexity: CharField = CharField(max_length=32)
    solution_type: CharField = CharField(max_length=32)

    objects = SaikiDB_Manager()

    def to_json(self) -> JsonResponse:

        # Note: doesn't propagate the ID to the JSON.
        data: dict[str, CharField] = {
            "name": self.name, "year": self.year,
            "category": self.category,
            "design_paradigm": self.design_paradigm,
            "generality": self.generality,
            "data_structure": self.data_structure,
            "temporal_complexity": self.temporal_complexity,
            "spatial_complexity": self.spatial_complexity,
            "solution_type": self.solution_type,
        }

        return JsonResponse(data)

    @staticmethod
    def from_json(json_dict: dict) -> ModelAlgorithm:
        if json_dict["type"] != "Algorithm":
            raise ValueError

        # ID is relative to the current count.
        new_id: int = ModelAlgorithm.objects.count()

        return ModelAlgorithm.objects.create(
            entity_id=new_id,
            name=json_dict["name"],
            category=json_dict["data"]["category"],
            year=json_dict["data"]["year"],
            temporal_complexity=json_dict["data"]["average_time_complexity"],
            spatial_complexity=json_dict["data"]["auxiliary_space_complexity"],
            data_structure=json_dict["data"]["data_structure"],
            kind_of_solution=json_dict["data"]["kind_of_solution"],
            generality=json_dict["data"]["generality"],
        )

    def to_historical_entity(self) -> entities.Algorithm:
        data_structure: str = self.data_structure
        
        return entities.Algorithm(
            name=str(self.name),
            year=self.year,
            category=self.category,
            average_time_complexity=self.temporal_complexity,
            auxiliary_space_complexity=self.spatial_complexity,
            data_structure=data_structure.split(","),
            kind_of_solution=self.solution_type,
            generality=self.generality,
        )

    def __str__(self) -> str:
        return self.name.__str__()


# Testing.
if __name__ == "__main__":
    example_algorithm = ModelAlgorithm(name="Merge sort",
                                       year=1945,
                                       category="Sorting",
                                       time_complexity="O(n log n)",
                                       space_complexity="O(n)",
                                       data_structure=["array"],
                                       solution_kind="exact",
                                       generality="general-purpose")

    print(example_algorithm)

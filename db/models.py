"""
backend/db/models.py

System's database models.

For all effects, relies on Django's type.
"""

from django.db import models
from django.db.models import CharField, IntegerField
from django.http import JsonResponse


class Model_Algorithm(models.Model):
    """Represents an algorithm; the entity."""

    name = CharField(max_length=32)
    year = IntegerField(max_length=32)
    category = CharField(max_length=32)
    design_paradigm = CharField(max_length=32)
    generality = CharField(max_length=32)
    temporal_complexity = CharField(max_length=32)
    spatial_complexity = CharField(max_length=32)
    solution_type = CharField(max_length=32)

    def to_json(self) -> JsonResponse:
        data: dict[str, CharField] = {
            "name": self.name,
            "year": self.year,
            "category": self.category,
            "design_paradigm": self.design_paradigm,
            "generality": self.generality,
            "temporal_complexity": self.temporal_complexity,
            "spatial_complexity": self.spatial_complexity,
            "solution_type": self.solution_type,
        }

        return JsonResponse(data)


# Testing
example_algorithm = Model_Algorithm(name="Merge sort",
                                    year=1945,
                                    category="Sorting",
                                    time_complexity="O(n log n)",
                                    space_complexity="O(n)",
                                    data_structure=["array"],
                                    solution_kind="exact",
                                    generality="general-purpose")


if __name__ == "__main__":
    ...

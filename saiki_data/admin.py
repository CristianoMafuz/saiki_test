"""
backend/saiki_data/admin.py

...
"""

from django.contrib import admin
from .models import ModelAlgorithm


@admin.register(ModelAlgorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ("name",  "category", "year")
    search_fields = ("name", "category")
    list_filter = ("category", "year")


if __name__ == "__main__":
    ...

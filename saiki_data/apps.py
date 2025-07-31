"""
backend/saiki_data/apps.py

...
"""

from django.apps import AppConfig


class SaikiDatabaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name: str = "saiki_data"
    verbose_name = "Saiki Data"


if __name__ == "__main__":
    ...

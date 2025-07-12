"""
backend/db/__init__.py

Project's database module.
"""

# from src.backend.db.models import Model_Algorithm


class SaikiDatabase(object):
    """Handles the database for the project."""

    def __init__(self) -> None:
        ...

    def fetch_algorithm(self, name: str) -> None:
        """Attempts getting an entity on the database."""
        ...


# Main Instantiation
# ------------------

saiki_database: SaikiDatabase = SaikiDatabase()


if __name__ == "__main__":
    ...

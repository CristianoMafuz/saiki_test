"""
backend/saiki_django/router.py

Django routing settings for saiki_django project.
"""


class SaikiDataRouter(object):
    """Routes to the SaikiData database."""

    app_label = "saiki_data"

    # disclaimer: below is auto-generated.

    def db_for_read(self, model, ** hints):
        print(f"read {model}")
        if model._meta.app_label == self.app_label:
            return "saiki_data_db"
        return None

    def db_for_write(self, model, **hints):
        print(f"write {model}")
        if model._meta.app_label == self.app_label:
            return "saiki_data_db"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(f"migrate {model_name}")
        if app_label == self.app_label:
            return db == "saiki_data_db"
        return None

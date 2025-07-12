"""
backend/saiki_site/models.py

Django models used by the site.
"""

from django.db import models


"""
(Initially on src/backend/db/models.py. 
@TODO: CHANGE IT TO THERE, EVENTUALLY)
"""

from django.db import models
from django.db.models import CharField, IntegerField
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
#------------------------------------------------Model Algorithm---------------------------------------------------------------------
class Model_Algorithm(models.Model):
    """Represents an algorithm; the entity."""

    name = CharField(max_length=32)
    year = IntegerField()
    category = CharField(max_length=32)
    data_structures = CharField(max_length=512)
    design_paradigm = CharField(max_length=32)
    generality = CharField(max_length=32)
    temporal_complexity = CharField(max_length=32)
    spatial_complexity = CharField(max_length=32)
    solution_kind = CharField(max_length=32)

    def to_json(self) -> JsonResponse:
        data: dict[str, CharField] = {
            "name": self.name,
            "year": self.year,
            "category": self.category,
            "design_paradigm": self.design_paradigm,
            "generality": self.generality,
            "temporal_complexity": self.temporal_complexity,
            "spatial_complexity": self.spatial_complexity,
            "solution_kind": self.solution_kind,
        }

        return JsonResponse(data)


#------------------------------------------------------------------------------------------------------------------------------------
class Jogador(models.Model):
    """Represents a player; the entity."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    name_public = models.CharField(max_length=32)
    name_user = models.CharField(max_length=32, unique=True)
    name_email = models.CharField(max_length=64, unique=True)
    name_password = models.CharField(max_length=128)  # Hashed password
    last_login = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)  # False = inactive, True = active

    @property
    def user_stats(self):
        return {
            "last_login": self.last_login,
            "status": self.status,
        }

    def set_password(self, raw_password):
        self.name_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.name_password)

    @property
    def userconfigs(self):
        return {
            "public": self.name_public,
            "user": self.name_user,
            "email": self.name_email,
            "password": self.name_password,
        }

    def __str__(self):
        return self.name_user
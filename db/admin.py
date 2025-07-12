
from .models import *

from django.contrib import admin


class DoideraAdmin(admin.ModelAdmin):
    model = Model_Algorithm


if __name__ == "__main__":
    admin.site.register(Model_Algorithm, DoideraAdmin)


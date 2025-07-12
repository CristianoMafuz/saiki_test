"""
backend/saiki_django/urls.py

URL configuration for saiki_django project.
"""

from django.contrib import admin
from django.urls import path, include
from django.urls.resolvers import URLPattern, URLResolver
from django.views.generic import TemplateView


urlpatterns: list[URLPattern | URLResolver] = [
    path('admin/', admin.site.urls),

    # Derived URL configurations
    path("", include("saiki_site.urls"))
    # path('', TemplateView.as_view(template_name="index.html")),
]

"""
backend/saiki_site/admin.py

...
"""

from django.contrib import admin
from .models import Jogador
from .forms import JogadorForm  # importe o form

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    form = JogadorForm  # aqui você conecta o form customizado
    list_display = ('id', 'name_public', 'name_user', 'name_email', 'last_login', 'status')
    search_fields = ('name_public', 'name_user', 'name_email','last_login' ,'status')
    readonly_fields = ('id', 'last_login', 'status')  # campos que não podem ser editados diretamente
    fieldsets = (
        (None, {
            'fields': ('name_public', 'name_user', 'name_email', 'name_password', 'last_login', 'status')
        }),
    )
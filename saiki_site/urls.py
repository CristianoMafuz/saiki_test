"""
backend/saiki_site/urls.py

URL configuration for saiki_site Django's application.
"""

from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views


urlpatterns: list[URLPattern | URLResolver] = [

    # Frontend views.
    path("", views.FrontendView.serve_frontend),
    path("custom/", views.FrontendView.serve_custom_mode, name='custom'),
    path("daily/", views.FrontendView.serve_daily_mode, name='daily'),
    path("tof/", views.FrontendView.serve_tof_mode, name='tof'),

    # Guess mode requests.
    path("api/guess/hint/", views.GuessView.request_hint),
    path("api/guess/entity/", views.GuessView.request_entity),
    path("api/guess/load/", views.GuessView.request_load),

    # Models URLS
    path('jogador/novo/', views.jogador_create, name='jogador_create'),
    path('jogador/sucesso/', views.jogador_success, name='jogador_success'), 
    path('login/', views.jogador_login, name='jogador_login'),
    path('register/', views.jogador_create, name='jogador_register'),
    path('painel/', views.painel_jogador, name='painel_jogador'),
    path('criar-sessao/', views.criar_sessao, name='criar_sessao'),
    path('sessao/<int:sessao_id>/', views.ver_sessao, name='ver_sessao'),
    path('sessao/<int:sessao_id>/encerrar/', views.encerrar_sessao, name='encerrar_sessao'),
    path('entrar-sessao/', views.entrar_sessao, name='entrar_sessao'),
]

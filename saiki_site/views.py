"""
backend/saiki_site/views.py

Viewing configuration for saiki_site Django's application.
"""

from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .guesser import guesser, GuessState
from typing import Any
import json


class FrontendView(object):
    """Handles the view of the frontend via the backend."""

    @staticmethod
    def serve_frontend(req) -> HttpResponse:
        """Provides the frontend main page.

            @TODO: This method can and may have variations concerning the different web pages."""

        from os import path

        # inferring the request...
        print(type(req), req)

        # the html source
        index_path: str = path.join(path.dirname(__file__), "../../frontend/site/html/index.html")

        # opening and sending the HTML over
        with open(index_path, encoding="utf-8") as index:
            return HttpResponse(index.read(), content_type="text/html")


class GuessView(object):
    """Handles the view of the Guess game mode."""

    @staticmethod
    @csrf_exempt  # Cookies~
    def request_hint(req: WSGIRequest) -> JsonResponse:
        """Processes the request of a hint, via POST."""

        if req.method != "POST":
            # empty return~
            return JsonResponse({})

        try:
            data = json.loads(req.body)
            name: str = data.get("attempt")

            if not isinstance(name, str):
                raise TypeError

        except TypeError | KeyError as e:
            name: str = "undef"
            print(e)

        return JsonResponse({
            "name": name.upper()
        })

    @staticmethod
    def __check_fields(state: GuessState, entity_name: str) -> JsonResponse:
        """Checks the fields of the player's guessing (and returns the response)."""

        # making sure the state have a selected entity.
        guesser.select_entity(state)

        # the entity that is marked to be solved by the player.
        from .enc import unpermute
        real_selected_index: int = unpermute(state.selected, state.key, 1000)
        correct_entity: dict = guesser.get_entity(real_selected_index)

        # the one matching what he inserted.
        match_entity: dict | None
        match_entity_index: int
        match_entity, match_entity_index = guesser.fetch_entity(entity_name)

        # will hold the JSON response back to the user.
        response: dict = {}

        if match_entity is not None:
            # meaning that at least it was found on the database...

            response: dict = {
                "name": match_entity["name"],
                "data": {},
                "type": "correct"
            }

            for field in match_entity["data"]:

                # if the field is correct, for all effects.
                guess_type: str = "correct" if match_entity["data"][field] == correct_entity["data"][field] else "wrong"

                # adding the respective field to the response...
                response["data"][field] = [match_entity["data"][field], guess_type]

                if response["type"] == "correct":
                    # if the response is correct up to now, it can potentially make the whole answer wrong.
                    response["type"] = guess_type

            state.add_attempt(match_entity_index)
        
        response_json: JsonResponse = JsonResponse(response)

        to_reset_cookies: bool = response["type"] == "correct" if "type" in response else False
        state.set_cookie(response_json, to_reset_cookies)

        return response_json

    @staticmethod
    @csrf_exempt  # Cookies~
    def request_entity(req: WSGIRequest) -> JsonResponse:
        """Processes the request of an entity, via POST."""

        if req.method != "POST":
            # empty return~
            return JsonResponse({})

        data: dict[str, Any] = json.loads(req.body)

        try:
            entity: str = data["entity"]

        except KeyError:
            return JsonResponse({})

        guess_state: GuessState = GuessState.from_request(req)
        return GuessView.__check_fields(guess_state, entity)


class OtherView(object):

    @staticmethod
    def read_root(req) -> JsonResponse:
        return JsonResponse(
            {
                "msg": "Hello from backend! Camarada"
            }
        )


def read_root1(req) -> JsonResponse:
    return JsonResponse(
        {
            "msg": "Helicóptero"
        }
    )


# -------------------------------------------------------------------------------------------
from .forms import JogadorForm, JogadorLoginForm
from .models import Jogador
from django.contrib import messages
from django.contrib.auth import login


def jogador_login(request):
    if request.method == "POST":
        form = JogadorLoginForm(request.POST)
        if form.is_valid():
            name_user = form.cleaned_data['name_user']
            password = form.cleaned_data['password']
            try:
                jogador = Jogador.objects.get(name_user=name_user)
                if jogador.check_password(password):
                    login(request, jogador.user)  # o User real associado
                    return redirect('painel_jogador')  # ou outra view pós-login
                else:
                    messages.error(request, "Senha incorreta.")
            except Jogador.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
    else:
        form = JogadorLoginForm()
    return render(request, "jogador_login.html", {"form": form})


def painel_jogador(request):
    if not request.user.is_authenticated:
        return redirect('jogador_login')

    try:
        jogador = Jogador.objects.get(user=request.user)
    except Jogador.DoesNotExist:
        jogador = None

    return render(request, "painel_jogador.html", {"jogador": jogador})


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def jogador_create(request):
    if request.method == 'POST':
        form = JogadorForm(request.POST)
        if form.is_valid():
            # Cria o usuário base do Django
            user = User.objects.create_user(
                username=form.cleaned_data['name_user'],
                email=form.cleaned_data['name_email'],
                password=form.cleaned_data['name_password']
            )

            jogador = form.save(commit=False)
            jogador.user = user  # associa o usuário criado
            jogador.set_password(form.cleaned_data['name_password'])  # hash na senha
            jogador.save()

            return redirect('jogador_success')  # ou a tela que desejar
    else:
        form = JogadorForm()

    return render(request, 'jogador_form.html', {'form': form})


def jogador_success(request):
    return HttpResponse("Jogador criado com sucesso!")

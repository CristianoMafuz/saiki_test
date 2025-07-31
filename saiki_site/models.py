"""
backend/saiki_site/models.py

Django models used by the site.
"""

from django.db import models
from django.utils import timezone
from django.db import models
from django.db.models import CharField, IntegerField
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


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

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"


    def __str__(self):
        return self.name_user

class message(models.Model):
    """Represents a message; the entity."""

    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='sent_messages')
    receivers = models.ManyToManyField(Jogador, related_name='received_messages')
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        receptores = ", ".join([r.name_user for r in self.receivers.all()])
        return f"Message from {self.sender.name_user} to {receptores} at {self.timestamp}"

class chat(models.Model):
    """Represents a chat; the entity."""

    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(Jogador, related_name='chats')
    messages = models.ManyToManyField(message, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    frequency = models.IntegerField(default=0)  # Frequency of messages in the chat

    number_of_messages = models.IntegerField(default=0)  # Total number of messages in the chat
    
    def add_message(self, msg: message):
        """Adds a message to the chat and updates the frequency."""
        self.messages.add(msg)
        self.number_of_messages += 1
        self.frequency += 1
        self.save()

    def __str__(self):
        return f"Chat {self.id} with {self.participants.count()} participants"

class Session(models.Model):
    """Represents a session; the entity."""

    id = models.AutoField(primary_key=True)
    public_key = models.CharField(max_length=64, unique=True)

    root_player = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='root_sessions')
    players = models.ManyToManyField(Jogador, related_name='sessions')

    chat = models.ForeignKey(chat, on_delete=models.CASCADE, null=True, blank=True)

    data_inicio = models.DateTimeField(editable=False)
    data_termino = models.DateTimeField(null=True, blank=True)
    session_time = models.DurationField(null=True, blank=True)

    active_players = models.ManyToManyField(Jogador, related_name='active_sessions', blank=True)

    # 🟢 status da sessão: ativa ou finalizada
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Sessão {self.id} - Jogador: {self.root_player.name_user}"

    def save(self, *args, **kwargs):
        creating = not self.id  # Verifica se é nova

        if creating:
            self.data_inicio = timezone.now()
            self.status = True  # Sessão começa ativa

        if not self.chat:
            self.chat = chat.objects.create()

        super().save(*args, **kwargs)

        # Adiciona o root_player como player e player ativo após salvar a primeira vez
        if creating:
            self.players.add(self.root_player)
            self.active_players.add(self.root_player)

    def start_session(self):
        """Ativa a sessão e define todos os jogadores como ativos."""
        self.active_players.set(self.players.all())
        self.data_termino = None
        self.session_time = None
        self.status = True
        self.save()

    def end_session(self):
        """Finaliza a sessão e marca como inativa."""
        self.data_termino = timezone.now()
        self.session_time = self.data_termino - self.data_inicio
        self.active_players.clear()
        self.status = False
        self.save()

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
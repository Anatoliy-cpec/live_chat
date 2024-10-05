from django.apps import AppConfig
import asyncio
from websockets.asyncio.server import serve



class ChatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatApp'

    def ready(self):
            from chatApp import signals  # выполнение модуля -> регистрация сигналов



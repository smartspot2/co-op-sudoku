
from django.urls import re_path

from .consumers import GameConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

websocket_urlpatterns = [
    re_path(r"game/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
]

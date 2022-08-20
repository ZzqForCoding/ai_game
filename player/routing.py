from django.urls import path
from player.consumers.game.index import MultiPlayerGame

websocket_urlpatterns = [
    path("wss/multiplayer/snake/", MultiPlayerGame.as_asgi(), name="wss_multiplayer"),
]

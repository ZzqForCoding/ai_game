from django.urls import path
from player.consumers.game.index import MultiPlayerGame
from player.consumers.hall.index import Hall

websocket_urlpatterns = [
    path("wss/multiplayer/snake/", MultiPlayerGame.as_asgi(), name="wss_multiplayer"),
    path("wss/hall/", Hall.as_asgi(), name="wss_hall"),
]

from django.urls import path
from player.consumers.game.snake import MultiPlayerSnakeGame
from player.consumers.game.gobang import MultiPlayerGobangGame
from player.consumers.game.reversi import MultiPlayerReversiGame
from player.consumers.hall.index import Hall

websocket_urlpatterns = [
    path("wss/multiplayer/snake/", MultiPlayerSnakeGame.as_asgi(), name="wss_multiplayer_snake"),
    path("wss/multiplayer/gobang/", MultiPlayerGobangGame.as_asgi(), name="wss_multiplayer_gobang"),
    path("wss/multiplayer/reversi/", MultiPlayerReversiGame.as_asgi(), name="wss_multiplayer_reversi"),
    path("wss/hall/", Hall.as_asgi(), name="wss_hall"),
]

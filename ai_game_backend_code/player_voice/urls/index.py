from django.urls import path, include

urlpatterns = [
    path('freshnews/', include('player_voice.urls.freshnews.index')),
    path('game_intro/', include('player_voice.urls.game_intro.index')),
]

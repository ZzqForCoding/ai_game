from django.urls import path, include

urlpatterns = [
    path('freshnews/', include('player_voice.urls.freshnews.index')),
]

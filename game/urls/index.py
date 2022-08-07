from django.urls import path
from game.views.getlist import GetListView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='game_getlist'),
]

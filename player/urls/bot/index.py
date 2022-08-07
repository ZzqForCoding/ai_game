from django.urls import path
from player.views.bot.add import AddView
from player.views.bot.remove import RemoveView
from player.views.bot.update import UpdateView
from player.views.bot.getlist import GetListView
from player.views.bot.getlist_game import GetListByGameView

urlpatterns = [
    path('add/', AddView.as_view(), name='bot_add'),
    path('remove/', RemoveView.as_view(), name='bot_remove'),
    path('update/', UpdateView.as_view(), name='bot_update'),
    path('getlist/', GetListView.as_view(), name='bot_getlist_user'),
    path('getlist_game/', GetListByGameView.as_view(), name='bot_getlist_game'),
]

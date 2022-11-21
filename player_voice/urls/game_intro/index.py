from django.urls import path
from player_voice.views.game_intro.getlist import GetListView
from player_voice.views.game_intro.get_id import GetIdView
from player_voice.views.game_intro.post import PostView
from player_voice.views.game_intro.remove import RemoveView
from player_voice.views.game_intro.edit import EditView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='game_intro_getlist'),
    path('get/<int:id>/', GetIdView.as_view(), name='game_intro_get_userid'),
    path('post/', PostView.as_view(), name='game_intro_post'),
    path('remove/', RemoveView.as_view(), name='game_intro_remove'),
    path('edit/', EditView.as_view(), name='game_intro_edit'),
]

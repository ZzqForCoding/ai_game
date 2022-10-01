from django.urls import path
from player_voice.views.fresh_news.getlist import GetListView
from player_voice.views.fresh_news.post import PostView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='player_voice_getlist'),
    path('post/', PostView.as_view(), name='player_voice_post'),
]

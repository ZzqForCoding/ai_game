from django.urls import path
from player_voice.views.fresh_news.getlist import GetListView
from player_voice.views.fresh_news.getlist_userid import GetListForUserIdView
from player_voice.views.fresh_news.post import PostView
from player_voice.views.fresh_news.remove import RemoveView
from player_voice.views.fresh_news.forward import ForwardView
from player_voice.views.fresh_news.add_like import AddLikeView
from player_voice.views.fresh_news.del_like import DelLikeView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='player_voice_getlist'),
    path('getlist/<int:userId>/', GetListForUserIdView.as_view(), name='player_voice_getlist_userid'),
    path('post/', PostView.as_view(), name='player_voice_post'),
    path('remove/', RemoveView.as_view(), name='player_voice_remove'),
    path('forward/', ForwardView.as_view(), name='player_voice_forward'),
    path('addlike/', AddLikeView.as_view(), name='player_voice_addlike'),
    path('dellike/', DelLikeView.as_view(), name='player_voice_dellike'),
]

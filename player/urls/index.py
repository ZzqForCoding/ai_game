from django.urls import path, include
from player.views.getinfo import InfoView
from player.views.register import RegisterView
from player.views.getranklist import GetRankListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='player_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='player_refresh'),
    path('getinfo/', InfoView.as_view(), name='player_getinfo'),
    path('register/', RegisterView.as_view(), name='player_register'),
    path('getranklist/', GetRankListView.as_view(), name='player_ranklist'),
    path('bot/', include('player.urls.bot.index')),
]

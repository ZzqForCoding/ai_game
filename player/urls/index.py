from django.urls import path
from player.views.index import index
from player.views.getinfo import InfoView
from player.views.register import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", index, name="index"),
    path('token/', TokenObtainPairView.as_view(), name='player_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='player_refresh'),
    path('getinfo/', InfoView.as_view(), name='player_getinfo'),
    path('register/', RegisterView.as_view(), name='player_register'),
]

from django.urls import path, include
from player.views.getinfo import InfoView
from player.views.getinfo_userId import InfoByUserIdView
from player.views.register import RegisterView
from player.views.getranklist import GetRankListView
from player.views.getplayer_page import GetPlayerPageView
from player.views.login import LoginView
from player.views.phone_login import PhoneLoginView
from player.views.verify_code import VerifyCodeView
from player.views.update_password import UpdatePasswordView
from player.views.update_token import UpdateTokenView
from player.views.update_info import UpdateInfoView
from player.views.get_chart_data import GetChartDataView
from player.views.binding_phone import BindingPhoneView
from player.views.send_msg import SendMsgView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', LoginView.as_view(), name='player_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='player_refresh'),
    path('token/update/', UpdateTokenView.as_view(), name='player_token_update'),
    path('phone_login/', PhoneLoginView.as_view(), name='player_phone_login'),
    path('verify_code/', VerifyCodeView.as_view(), name='player_verify_code'),
    path('update_password/', UpdatePasswordView.as_view(), name='player_update_password'),
    path('getinfo/', InfoView.as_view(), name='player_getinfo'),
    path('getinfo/<int:userId>/', InfoByUserIdView.as_view(), name='player_getinfo_userid'),
    path('register/', RegisterView.as_view(), name='player_register'),
    path('getranklist/', GetRankListView.as_view(), name='player_ranklist'),
    path('getplayerpage/', GetPlayerPageView.as_view(), name='player_page'),
    path('getchartdata/', GetChartDataView.as_view(), name='player_get_chart_data'),
    path('binding_phone/', BindingPhoneView.as_view(), name='player_binging_phone'),
    path('send_msg/', SendMsgView.as_view(), name='player_send_msg'),
    path('update_info/', UpdateInfoView.as_view(), name='player_update_info'),
    path('bot/', include('player.urls.bot.index')),
    path('acwing/', include('player.urls.acwing.index')),
    path('qq/', include('player.urls.qq.index')),
    path('img/', include('player.urls.img.index')),
]

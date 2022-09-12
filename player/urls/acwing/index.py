from django.urls import path
from player.views.third_login.acwing.apply_code import apply_code as web_apply_code
from player.views.third_login.acwing.receive_code import receive_code as web_receive_code

urlpatterns = [
    path("web/apply_code/", web_apply_code, name="player_acwing_web_apply_code"),
    path("web/receive_code/", web_receive_code, name="player_acwing_web_receive_code"),
]

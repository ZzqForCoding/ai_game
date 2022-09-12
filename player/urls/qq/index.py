from django.urls import path
from player.views.third_login.qq.apply_code import apply_code as web_apply_code
from player.views.third_login.qq.receive_code import receive_code as web_receive_code

urlpatterns = [
    path("apply_code/", web_apply_code, name="player_qq_web_apply_code"),
    path("receive_code/", web_receive_code, name="player_qq_web_receive_code"),
]

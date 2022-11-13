from django.urls import path
from player.views.upload_avatar.apply import ApplyView
from player.views.upload_avatar.receive import ReceiveView
from player.views.upload_avatar.update_avatar import UpdateAvatarView

urlpatterns = [
    path('apply/', ApplyView.as_view(), name='player_apply_upload_avatar'),
    path('receive/', ReceiveView.as_view(), name='player_receive_upload_avatar'),
    path('update_avatar/', UpdateAvatarView.as_view(), name='player_update_avatar'),
]

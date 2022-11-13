from django.urls import path
from player.views.bot.add import AddView
from player.views.bot.remove import RemoveView
from player.views.bot.update import UpdateView
from player.views.bot.getlist import GetListView
from player.views.bot.getlist_game import GetListByGameView
from player.views.bot.debug import DebugView
from player.views.bot.alipay.apply_alipay import ApplyAliPayView
from player.views.bot.alipay.alipay_back import AliPayBackView
from player.views.bot.is_expand import IsExpandView

urlpatterns = [
    path('add/', AddView.as_view(), name='bot_add'),
    path('remove/', RemoveView.as_view(), name='bot_remove'),
    path('update/', UpdateView.as_view(), name='bot_update'),
    path('getlist/<int:userId>/', GetListView.as_view(), name='bot_getlist_user'),
    path('getlist_game/<int:gameId>/', GetListByGameView.as_view(), name='bot_getlist_game'),
    path('debug/', DebugView.as_view(), name='bot_debug'),
    path('alipay/', ApplyAliPayView.as_view(), name='pay_jump'),
    path('alipay/back/', AliPayBackView.as_view(), name='pay_result'),
    path('isexpand/', IsExpandView.as_view(), name='bot_isexpand'),
]

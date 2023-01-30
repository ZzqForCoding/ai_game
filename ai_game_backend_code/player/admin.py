from django.contrib import admin
from player.models.player import Player
from player.models.bot import Bot
from player.models.order import Order
from player.models.img import Img
from player.models.platform_data import PlatformData

admin.site.site_header = 'AIGame Platform'  # 设置header
admin.site.site_title = 'AIGame Platform Administration'   # 设置title
admin.site.index_title = 'AIGame Platform'

# Register your models here.
admin.site.register(Player)
admin.site.register(Bot)
admin.site.register(Order)
admin.site.register(Img)
admin.site.register(PlatformData)

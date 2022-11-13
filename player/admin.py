from django.contrib import admin
from player.models.player import Player
from player.models.bot import Bot
from player.models.order import Order
from player.models.img import Img

# Register your models here.
admin.site.register(Player)
admin.site.register(Bot)
admin.site.register(Order)
admin.site.register(Img)

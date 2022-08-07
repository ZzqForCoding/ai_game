from django.contrib import admin
from player.models.player import Player
from player.models.bot import Bot

# Register your models here.
admin.site.register(Player)
admin.site.register(Bot)

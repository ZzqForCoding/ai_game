from django.contrib import admin
from player_voice.models.fresh_news import FreshNews
from player_voice.models.player_like_fresh_news import Player_Like_Fresh_News
from player_voice.models.game_intro import GameIntro

# Register your models here.
admin.site.register(FreshNews)
admin.site.register(Player_Like_Fresh_News)
admin.site.register(GameIntro)

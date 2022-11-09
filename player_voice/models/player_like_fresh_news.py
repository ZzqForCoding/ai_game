from django.db import models
from django.contrib.auth.models import User
from player_voice.models.fresh_news import FreshNews

class Player_Like_Fresh_News(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    freshNews = models.ForeignKey(
        FreshNews,
        on_delete=models.CASCADE
    )

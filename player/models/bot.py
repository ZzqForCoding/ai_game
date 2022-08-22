from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from game.models.game import Game

class Bot(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_bot'
    )
    game = models.ForeignKey(
        Game,
        null=True,
        on_delete=models.CASCADE,
        related_name='game_bot'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    content = models.TextField(max_length=10000)
    createtime = models.DateTimeField(default=timezone.now)
    modifytime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.game) + ' - ' + str(self.user) + ' - ' + str(self.title)

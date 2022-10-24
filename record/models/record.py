from django.db import models
from django.utils import timezone
from game.models.game import Game

class Record(models.Model):
    game = models.ForeignKey(
        Game,
        null=True,
        on_delete=models.CASCADE,
        related_name='game_record'
    )
    a_id = models.IntegerField()
    a_is_robot = models.BooleanField(default=False)
    a_language = models.CharField(max_length=20, default="", blank=True, null=True)
    b_id = models.IntegerField()
    b_is_robot = models.BooleanField(default=False)
    b_language = models.CharField(max_length=20, default="", blank=True, null=True)
    a_steps = models.TextField(max_length=1000)
    b_steps = models.TextField(max_length=1000)
    map = models.TextField(max_length=1000, default="", blank=True, null=True)
    loser = models.CharField(max_length=10)
    createtime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.game) + '-' + str(self.a_id) + '-' + str(self.b_id) + '-' + str(self.createtime)

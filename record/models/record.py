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
    a_sx = models.IntegerField()
    a_sy = models.IntegerField()
    b_id = models.IntegerField()
    b_sx = models.IntegerField()
    b_sy = models.IntegerField()
    a_steps = models.TextField(max_length=1000)
    b_steps = models.TextField(max_length=1000)
    map = models.TextField(max_length=1000)
    loser = models.CharField(max_length=10)
    createtime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.game) + '-' + str(self.a_id) + '-' + str(self.b_id) + '-' + str(self.createtime)
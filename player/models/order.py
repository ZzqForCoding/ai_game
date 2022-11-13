from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_order'
    )
    trade_id = models.CharField(max_length=100)
    out_trade_no = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    create_time = models.DateTimeField(default=timezone.now)
    finish_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.out_trade_no) + '- ' + str(self.user) + '-' + str(self.create_time)

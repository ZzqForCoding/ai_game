from django.db import models
from django.contrib.auth.models import User

class Img(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_img'
    )
    filename = models.CharField(max_length=300)
    randomname = models.CharField(max_length=100)
    size = models.IntegerField()
    mimetype = models.CharField(max_length=50)
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.URLField(max_length=256, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + self.filename


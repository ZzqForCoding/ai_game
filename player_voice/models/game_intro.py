from django.db import models
from django.contrib.auth.models import User

class GameIntro(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=20000, blank=True, null=True)
    createdtime = models.DateTimeField(auto_now_add=True)
    is_post = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " " + str(self.title)

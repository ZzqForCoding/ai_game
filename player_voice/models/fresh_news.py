from django.db import models
from django.contrib.auth.models import User

class FreshNews(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_freshnews'
    )
    content = models.TextField(max_length=5000)
    createdtime = models.DateTimeField(auto_now_add=True)

    def __str(self):
        return str(self.user) + " " + str(self.content)

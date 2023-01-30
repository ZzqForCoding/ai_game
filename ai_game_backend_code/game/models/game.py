from django.db import models

class Game(models.Model):
    name = models.CharField(default="", max_length=50)

    def __str__(self):
        return str(self.name)

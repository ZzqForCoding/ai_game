from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class FreshNews(MPTTModel):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_freshnews'
    )
    content = models.TextField(max_length=5000)
    createdtime = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers',
    )

    # class MPTTMeta:
    #     order_insertion_by = ['createdtime']

    def __str__(self):
        return str(self.user) + " " + str(self.content)

from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(max_length=256, default="https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg")
    rating = models.IntegerField(default=1500)
    openid = models.CharField(default="", max_length=50, blank=True, null=True)
    token = models.CharField(default="", max_length=500, blank=True, null=True)
    job = models.CharField(max_length=20, blank=True, null=True)
    desp = models.CharField(max_length=200, blank=True, null=True)
    cpp_code_compile_cnt = models.IntegerField(default=0)
    cpp_code_compile_success_cnt = models.IntegerField(default=0)
    java_code_compile_cnt = models.IntegerField(default=0)
    java_code_compile_success_cnt = models.IntegerField(default=0)
    py_code_compile_cnt = models.IntegerField(default=0)
    py_code_compile_success_cnt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' ' + str(self.rating)

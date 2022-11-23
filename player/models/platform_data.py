from django.db import models

class PlatformData(models.Model):
    # 形如2022-11-02这样的时间
    date = models.DateField()
    register_cnt = models.IntegerField(default=0)
    login_cnt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date) + ', 注册人数：' + str(self.register_cnt) + ', 登录人数：' + str(self.login_cnt)

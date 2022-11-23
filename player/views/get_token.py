from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from player.models.player import Player
from player.models.platform_data import PlatformData
import datetime

class RemTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        player = Player.objects.filter(user=self.user)[0]
        player.token = "Bearer %s" % (data['access'])
        player.save()

        # 记录登录人数
        users = cache.get('login_users', [])
        if self.user.id not in users:
            today = datetime.date.today()
            platformData = PlatformData.objects.filter(date=today)
            if not platformData.exists():
                platformData = PlatformData.objects.create(date=today, login_cnt=1)
            else:
                platformData = platformData.first()
                platformData.login_cnt += 1
            platformData.save()
            users.append(self.user.id)
            st = datetime.datetime.now()
            ed = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.datetime.min.time())
            cache.set('login_users', users, (ed - st).seconds)

        return data

class RemTokenObtainPairView(TokenObtainPairView):
    serializer_class = RemTokenObtainPairSerializer

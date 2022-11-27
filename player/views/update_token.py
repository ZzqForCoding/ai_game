from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from player.models.player import Player
from player.models.platform_data import PlatformData
import datetime

class UpdateTokenView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        player = Player.objects.get(user=request.user)
        player.token = "Bearer %s" % (request.POST['token'])
        player.save()

        # 记录登录人数
        users = cache.get('login_users', [])
        if player.user.id not in users:
            today = datetime.date.today()
            platformData = PlatformData.objects.filter(date=today)
            if not platformData.exists():
                platformData = PlatformData.objects.create(date=today, login_cnt=1)
            else:
                platformData = platformData.first()
                platformData.login_cnt += 1
            platformData.save()
            users.append(player.user.id)
            st = datetime.datetime.now()
            ed = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.datetime.min.time())
            cache.set('login_users', users, (ed - st).seconds)

        return Response({
            'result': "success"
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.db.models import Q
from player.models.player import Player
from player.models.platform_data import PlatformData
import datetime
import pika
import json

class LoginView(APIView):
    def __init__(self):
        self.credentials = pika.PlainCredentials('zzq', 'zxc123')

    def post(self, request):
        data = request.POST
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return Response({
                'result': "用户名和密码不能为空"
            })
        player = Player.objects.filter(Q(user__username=username) | Q(phone=username))
        if not player.exists():
            return Response({
                'result': "用户名或手机号不存在"
            })
        else:
            player = player.first()

        if player.user.check_password(password):
            refresh = RefreshToken.for_user(player.user)
            token = str(refresh.access_token)
            refresh = str(refresh)
            player.token = "Bearer %s" % token
            player.save()

            # 若当前已在线，则通知给用户
            is_online = cache.get('notification_%d' % player.user.id, '')
            if is_online:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',
                    port=5672, credentials=self.credentials))
                channel = connection.channel()
                body = {
                    'event': "account_notification",
                    'target_user_id': player.user.id,
                    'data': {
                        'title': "[通知] 帐号异常",
                        'msg': '您的帐号再别的地方登陆，若不是您请修改密码',
                    },
                }
                channel.basic_publish(exchange='', routing_key='notification_queue', body=json.dumps(body),
                        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
                connection.close()

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
                'result': "success",
                'access': token,
                'refresh': refresh,
            })
        else:
            return Response({
                'result': "密码错误"
            })

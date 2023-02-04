from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
import pika
import re
import json

class SendMsgView(APIView):

    def __init__(self):
        self.credentials = pika.PlainCredentials('zzq', 'zxc123')

    def post(self, request):
        data = request.POST
        phone = data.get('phone', '')
        flag = data.get('flag', '')

        if flag == '':
            return Response({
                'result': "缺少参数"
            })
        if not phone:
            return Response({
                'result': "电话字段不能为空"
            })
        if not re.match('^1[3-9]\d{9}$', phone):
            return Response({
                'result': "不是合法的电话字段"
            })

        player = None
        if flag == "binding":
            user = request.user
            player = Player.objects.get(user=user)
        elif flag == "login" or flag == "update_password":
            player = Player.objects.filter(phone=phone)
            if not player.exists():
                return Response({
                    'result': "账号不存在"
                })
            else:
                player = player.first()
        if not player.user.is_superuser:
            return Response({
                'result': "由于平台太穷了，只有管理员能够发送短信验证码"
            })

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',
            port=5672, credentials=self.credentials))
        channel = connection.channel()
        body = {
            'target_user_id': player.user.id,
            "phone": phone
        }
        channel.basic_publish(exchange='', routing_key='send_msg_queue', body=json.dumps(body),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        connection.close()
        return Response({
            'result': "success"
        })

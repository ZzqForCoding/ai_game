from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from player.permissions.one_user_login import OneUserLogin
import pika
import re
import json

class SendMsgView(APIView):
    permission_classes = ([OneUserLogin])

    def __init__(self):
        self.credentials = pika.PlainCredentials('admin', 'zxc123')

    def post(self, request):
        phone = request.POST.get('phone', '')
        user = request.user

        if not phone:
            return Response({
                'result': "电话字段不能为空"
            })
        if not re.match('^1[3-9]\d{9}$', phone):
            return Response({
                'result': "不是合法的电话字段"
            })
        if not user.is_superuser:
            return Response({
                'result': "由于平台太穷了，只有管理员能够发送短信验证码"
            })

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='120.76.157.21',
            port=20105, credentials=self.credentials))
        channel = connection.channel()
        body = {
            'target_user_id': user.id,
            "phone": phone
        }
        channel.basic_publish(exchange='', routing_key='send_msg_queue', body=json.dumps(body),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        connection.close()

        return Response({
            'result': "success"
        })

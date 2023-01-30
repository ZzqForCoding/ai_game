from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews
import pika
import json

class PostView(APIView):
    permission_classes = ([OneUserLogin])

    def __init__(self):
        self.credentials = pika.PlainCredentials('admin', 'zxc123')

    def post(self, request):
        data = request.POST
        user = request.user
        content = data.get('content')
        parent_id = data.get('parent_id', -1)

        map = {}
        if content == '':
            map['result'] = '内容不能为空'
            return Response(map)

        if len(content) > 5000:
            map['result'] = "内容长度不能超过5000个字符"
            return Response(map)

        freshNews = FreshNews.objects.create(user=user, content=content)

        if parent_id != -1:
            parent = FreshNews.objects.get(id=parent_id)
            freshNews.parent_id = parent.get_root().id
            freshNews.reply_to = parent.user

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='backend',
                port=15671, credentials=self.credentials))
            channel = connection.channel()
            substr_msg = parent.content[:5]
            if len(substr_msg) == 5: substr_msg += '...'
            body = {
                'event': "freshnews_notification",
                'target_user_id': parent.user.id,
                'data': {
                    'userId': user.id,
                    'username': user.username,
                    'freshNewsId': parent.id,
                    'title': "[动态] 新消息",
                    'msg': substr_msg,
                },
            }
            channel.basic_publish(exchange='', routing_key='notification_queue', body=json.dumps(body),
                    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
            connection.close()


        freshNews.save()
        map['result'] = 'success'
        return Response(map)

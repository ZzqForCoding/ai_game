from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
import re

class BindingPhoneView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        data = request.POST

        code = data.get('code', '').strip()
        phone = data.get('phone', '').strip()

        if not phone:
            return Response({
                'result': "电话字段不能为空"
            })
        if not re.match('^1[3-9]\d{9}$', phone):
            return Response({
                'result': "不是合法的电话字段"
            })
        players = Player.objects.filter(phone=phone)
        if players.exists():
            return Response({
                'result': "一个手机号只能绑定一个账号"
            })
        cache_code = str(cache.get(phone, ''))
        if code != cache_code:
            return Response({
                'result': "验证码不一致"
            })

        player = Player.objects.get(user=user)
        player.phone = phone
        player.save()

        return Response({
            'result': "success"
        })

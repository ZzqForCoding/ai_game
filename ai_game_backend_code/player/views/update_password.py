from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from player.models.player import Player
import re

class UpdatePasswordView(APIView):
    def post(self, request):
        data = request.POST
        state = data.get('state', '')
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', '')

        if not state:
            return Response({
                'result': "参数传递错误"
            })
        phone = cache.get(state, '')
        if not phone:
            return Response({
                'result': "state不存在, 没有权限修改密码"
            })

        if password != password_confirm:
            return Response({
                'result': "两个密码不一致，请再次输入"
            })

        if not re.match(r'[a-zA-Z0-9]{6,}', password):
            return Response({
                'result': '密码强度不合格'
            })
        player = Player.objects.filter(phone=phone)
        if not player.exists():
            return Response({
                'result': "系统错误，请刷新页面"
            })
        else:
            player = player.first()

        player.user.set_password(password)
        player.user.save()
        return Response({
            'result': "success"
        })

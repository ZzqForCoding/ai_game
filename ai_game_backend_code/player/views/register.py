from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from player.models.player import Player
from player.models.platform_data import PlatformData
from datetime import date
import re

class RegisterView(APIView):
    def post(self, request):
        data = request.POST
        username = data.get("username", "").strip()
        password = data.get("password", "")
        password_confirm = data.get("password_confirm", "")
        if not username or not password:
            return Response({
                'result': "用户名和密码不能为空"
            })
        if password != password_confirm:
            return Response({
                'result': "两个密码不一致"
            })
        if Player.objects.filter(Q(user__username=username) | Q(phone=username)).exists():
            return Response({
                'result': '用户名或手机号已存在'
            })

        if not re.match(r'[a-zA-Z0-9]{6,}', password):
            return Response({
                'result': '密码强度不合格'
            })

        user = User(username=username)
        user.set_password(password)
        user.save()
        Player.objects.create(user=user, photo="https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg")

        # 记录注册人数
        today = date.today()
        platformData = PlatformData.objects.filter(date=today)
        if not platformData.exists():
            platformData = PlatformData.objects.create(date=today, register_cnt=1)
        else:
            platformData = platformData.first()
            platformData.register_cnt += 1
        platformData.save()

        return Response({
            'result': "success",
        })

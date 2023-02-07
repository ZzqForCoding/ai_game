from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from django.contrib.auth.models import User
from player.models.player import Player

class UpdateInfoView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        data = request.POST

        username = data.get("username", '')
        job = data.get("job", '')
        desp = data.get("desp", '')

        if not username or len(username) > 15:
            return Response({
                'result': "用户名不能为空且不能超过15个字符",
            })
        if User.objects.filter(username=username) and user.username != username:
            return Response({
                'result': "用户名已被使用"
            })
        if len(job) > 20:
            return Response({
                'result': "职业描述不能超过20个字符"
            })
        if len(desp) > 200:
            return Response({
                'result': "个性签名长度不能超过200个字符"
            })
        user.username = username
        user.save()
        if job or desp:
            player = Player.objects.get(user=user)
            player.job = job
            player.desp = desp
            player.save()

        return Response({
            'result': "success",
        })

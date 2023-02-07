from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot

class RemoveView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        bot_id = request.POST.get('bot_id', 0)

        bot = Bot.objects.filter(id=bot_id)

        map = {}
        if not bot.exists():
            map['result'] = 'Bot不存在或已被删除'
            return Response(map)
        bot = bot[0]
        if bot.user != user:
            map['result'] = '没有权限删除该Bot'
            return Response(map)

        bot.delete()
        map['result'] = 'success'
        return Response(map)

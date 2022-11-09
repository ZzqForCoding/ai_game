from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot

class GetListView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, userId):
        bots = Bot.objects.filter(user__id=userId)

        resp = []
        for bot in bots:
            resp.append({
                'id': bot.id,
                'game': bot.game.name,
                'title': bot.title,
                'description': bot.description,
                'content': bot.content,
                'language': bot.language,
                'createtime': bot.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                'modifytime': bot.modifytime.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return Response({
            'result': "success",
            'bots': resp
        })

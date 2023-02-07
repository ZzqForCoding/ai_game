from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot
from game.models.game import Game

class GetListByGameView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, gameId):
        userId  = request.GET.get('userId', -1)
        if userId == -1:
            return Response({
                'result': "不存在此用户",
            })
        game = Game.objects.filter(id=gameId)

        if not game:
            return Response({
                'result': '不存在这个游戏',
            })

        bots = Bot.objects.filter(user__id=userId, game=game[0]).order_by('-modifytime')

        resp = []
        for bot in bots:
            resp.append({
                'id': bot.id,
                'game': bot.game.name,
                'title': bot.title,
                'description': bot.description,
                'language': bot.language,
                'content': bot.content,
                'createtime': bot.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                'modifytime': bot.modifytime.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return Response({
            'result': "success",
            'bots': resp,
        })

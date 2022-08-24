from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from player.models.bot import Bot
from game.models.game import Game

class GetListByGameView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        user = request.user
        game_id  = request.GET.get('game_id', 0)
        game = Game.objects.filter(id=game_id)

        if not game:
            return Response({
                'result': '不存在这个游戏',
            })

        bots = Bot.objects.filter(user=user, game=game[0])

        resp = []
        for bot in bots:
            resp.append({
                'id': bot.id,
                'game': bot.game.name,
                'title': bot.title,
                'description': bot.description,
                'content': bot.content,
                'createtime': bot.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                'modifytime': bot.modifytime.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return Response(resp)

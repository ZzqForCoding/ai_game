from rest_framework.views import APIView
from rest_framework.response import Response
from player.models.player import Player
from player_voice.models.game_intro import GameIntro
from player_voice.utils.time_since import time_since_zh

class GetIdView(APIView):
    def get(self, request, id):
        gameIntro = GameIntro.objects.filter(id=id)

        if gameIntro.exists():
            gameIntro = gameIntro.first()
            if not gameIntro.is_post:
                return Response({
                    'result': "此说明并未发布"
                })
        else:
            return Response({
                'result': "参数错误"
            })
        player = Player.objects.get(user__id=gameIntro.user.id)
        return Response({
            'result': 'success',
            'data': {
                "id": gameIntro.id,
                "userId": player.user.id,
                "username": player.user.username,
                "photo": player.photo,
                "title": gameIntro.title,
                "content": gameIntro.content,
                "since": time_since_zh(gameIntro.createdtime),
            }
        })

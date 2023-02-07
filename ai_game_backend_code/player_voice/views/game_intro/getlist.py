from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player.models.player import Player
from player_voice.models.game_intro import GameIntro
from player_voice.utils.time_since import time_since_zh

class GetListView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        resp = []
        gameIntros = GameIntro.objects.filter(is_post=True).order_by('-createdtime')
        for gameIntro in gameIntros:
            player = Player.objects.get(user__id=gameIntro.user_id)
            data = {
                'id': gameIntro.id,
                'userId': player.user.id,
                'username': player.user.username,
                'photo': player.photo,
                'title': gameIntro.title,
                'content': gameIntro.content,
                'since': time_since_zh(gameIntro.createdtime),
            }
            resp.append(data)
        return Response({
            'result': 'success',
            'gameIntros': resp,
            'count': gameIntro.count()
        })

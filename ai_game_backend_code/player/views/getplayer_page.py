from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from ai_game_platform import settings
from player.models.player import Player
import json

class GetPlayerPageView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        user = request.user
        players = Player.objects.all().order_by('-rating')
        player = Player.objects.get(user=user)

        idx = -1
        for i in range(len(players)):
            if players[i] == player:
                idx = i + 1
                break

        page = int(idx / settings.player_rank_page_size) + 1

        return Response({
            'result': "success",
            'page': page,
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player

class InfoByUserIdView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, userId):
        player = Player.objects.get(user__id=userId)
        return Response({
            'result': "success",
            "player_info": {
                'username': player.user.username,
                'photo': player.photo,
            }
        })

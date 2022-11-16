from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player

class InfoView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        user = request.user
        player = Player.objects.get(user=user)
        return Response({
            'result': 'success',
            'id': user.id,
            'username': user.username,
            'job': player.job,
            'desp': player.desp,
            'photo': player.photo,
            'rating': player.rating,
        })

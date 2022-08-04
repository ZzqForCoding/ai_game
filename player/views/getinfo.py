from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from player.models.player import Player

class InfoView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        user = request.user
        player = Player.objects.get(user=user)
        return Response({
            'result': 'success',
            'id': user.id,
            'username': user.username,
            'photo': player.photo
        })

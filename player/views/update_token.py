from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from player.models.player import Player

class UpdateTokenView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        player = Player.objects.get(user=request.user)
        player.token = "Bearer %s" % (request.POST['token'])
        player.save()
        return Response({
            'result': "success"
        })

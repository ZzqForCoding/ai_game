from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.game import Game

class GetListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        games = Game.objects.all()
        resp = []
        for game in games:
            resp.append({
                'id': game.id,
                'name': game.name,
            })

        return Response(resp)

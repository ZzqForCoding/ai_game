from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from game.models.game import Game

class GetListView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        games = Game.objects.all()
        resp = []
        for game in games:
            resp.append({
                'id': game.id,
                'name': game.name,
            })

        return Response({
            'result': "success",
            "games": resp
        })

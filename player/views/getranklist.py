from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from player.models.player import Player
import json

class PlayerRankPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None

class GetRankListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        players = Player.objects.all().order_by('-rating')
        players_count = players.count()
        pagination = PlayerRankPagination()
        page_players = pagination.paginate_queryset(queryset=players, request=request, view=self)
        resp = []
        for player in page_players:
            item = {}
            item['username'] = player.user.username
            item['photo'] = player.photo
            item['rating'] = player.rating
            resp.append(item)

        return Response({
            'players': json.dumps(resp),
            'players_count': players_count
        })

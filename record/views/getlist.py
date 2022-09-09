from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from record.models.record import Record
from player.models.player import Player
import json

class RecordPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None

class GetListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        records = Record.objects.all().order_by('-createtime')
        records_count = records.count()
        pagination = RecordPagination()
        page_records = pagination.paginate_queryset(queryset=records, request=request, view=self)
        items = []
        for record in page_records:
            playerA = Player.objects.get(id=record.a_id)
            playerB = Player.objects.get(id=record.b_id)
            item = {}
            item['game_id'] = record.game.id
            item['game'] = record.game.name
            item['a_photo'] = playerA.photo
            item['a_username'] = playerA.user.username
            item['b_photo'] = playerB.photo
            item['b_username'] = playerB.user.username
            item['id'] = record.id
            item['a_id'] = record.a_id
            item['a_sx'] = record.a_sx
            item['a_sy'] = record.a_sy
            item['b_id'] = record.b_id
            item['b_sx'] = record.b_sx
            item['b_sy'] = record.b_sy
            item['a_steps'] = record.a_steps
            item['b_steps'] = record.b_steps
            item['map'] = record.map
            item['createtime'] = record.createtime.strftime('%Y-%m-%d %H:%M:%S')
            item['result'] = record.loser
            items.append(item)
        resp = {
            'records': json.dumps(items),
            'records_count': records_count
        }
        return Response(resp)

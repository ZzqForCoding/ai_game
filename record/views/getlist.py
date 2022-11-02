from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from record.models.record import Record
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
import json

class RecordPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None

class GetListView(APIView):
    # permission_classes = ([OneUserLogin])

    def get(self, request):
        records = Record.objects.all().order_by('-createtime')
        records_count = records.count()
        pagination = RecordPagination()
        page_records = pagination.paginate_queryset(queryset=records, request=request, view=self)
        items = []
        for record in page_records:
            playerA = Player.objects.get(user__id=record.a_id)
            playerB = Player.objects.get(user__id=record.b_id)
            item = {}
            item['game_id'] = record.game.id
            item['game'] = record.game.name
            item['a_photo'] = playerA.photo
            item['a_username'] = playerA.user.username
            item['b_photo'] = playerB.photo
            item['b_username'] = playerB.user.username
            item['id'] = record.id
            item['a_id'] = record.a_id
            item['a_is_robot'] = record.a_is_robot
            item['a_language'] = record.a_language
            item['b_id'] = record.b_id
            item['b_is_robot'] = record.b_is_robot
            item['b_language'] = record.b_language
            item['a_steps'] = record.a_steps
            item['b_steps'] = record.b_steps
            item['map'] = record.map
            item['createtime'] = record.createtime.strftime('%Y-%m-%d %H:%M:%S')
            item['result'] = record.loser
            items.append(item)
        return Response({
            'result': "success",
            'records': json.dumps(items),
            'records_count': records_count
        })

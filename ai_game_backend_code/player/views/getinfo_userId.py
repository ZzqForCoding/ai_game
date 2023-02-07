from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from utils.permissions.one_user_login import OneUserLogin
from player.models.player import Player
from record.models.record import Record
from player_voice.models.fresh_news import FreshNews
from player.models.bot import Bot

class InfoByUserIdView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, userId):
        player = Player.objects.get(user__id=userId)
        record_cnt = Record.objects.filter(Q(a_id = userId) | Q(b_id = userId)).count()
        bot_cnt = Bot.objects.filter(user__id=userId).count()
        freshNews_cnt = FreshNews.objects.filter(user__id=userId, parent=None).count()

        return Response({
            'result': "success",
            "player_info": {
                'username': player.user.username,
                'photo': player.photo,
                'job': player.job,
                'desp': player.desp,
                'recordCnt': record_cnt,
                'botCnt': bot_cnt,
                'freshNewsCnt': freshNews_cnt,
                'isSuperUser': player.user.is_superuser,
            }
        })

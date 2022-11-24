from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
from record.models.record import Record
from player_voice.models.fresh_news import FreshNews
from player.models.bot import Bot

class InfoView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        user = request.user
        player = Player.objects.get(user=user)
        record_cnt = Record.objects.filter(Q(a_id = user.id) | Q(b_id = user.id)).count()
        bot_cnt = Bot.objects.filter(user=user).count()
        freshNews_cnt = FreshNews.objects.filter(user=user, parent=None).count()

        return Response({
            'result': 'success',
            'id': user.id,
            'username': user.username,
            'job': player.job,
            'desp': player.desp,
            'photo': player.photo,
            # 'rating': player.rating,
            'recordCnt': record_cnt,
            'botCnt': bot_cnt,
            'freshNewsCnt': freshNews_cnt,
            'isSuperUser': user.is_superuser,
            'phone': player.phone,
        })

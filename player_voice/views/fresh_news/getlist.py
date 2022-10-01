from rest_framework.views import APIView
from rest_framework.response import Response
from player.models.player import Player
from player_voice.models.fresh_news import FreshNews
from django.utils import timezone
import math

class GetListView(APIView):
    def time_since_zh(self, value):
        now = timezone.now()
        diff = now - value

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return '刚刚'
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 60 * 60:
            return str(math.floor(diff.seconds / 60)) + "分钟前"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 24 * 60 * 60:
            return str(math.floor(diff.seconds / 3600)) + "小时前"
        if diff.days >= 1 and diff.days < 30:
            return str(diff.days) + "天前"
        if diff.days >= 30 and diff.days < 365:
            return str(math.floor(diff.days / 30)) + "个月前"
        if diff.days >= 365:
            return str(math.floor(diff.days / 365)) + "年前"

    def get(self, request):
        freshNews = FreshNews.objects.all().order_by('-createdtime')
        resp = []
        for item in freshNews:
            player = Player.objects.get(user__id=item.user_id)
            resp.append({
                'id': item.id,
                'photo': player.photo,
                'username': player.user.username,
                'content': item.content,
                'since': self.time_since_zh(item.createdtime)
            })
        return Response({
            'result': "success",
            'freshNews': resp
        })

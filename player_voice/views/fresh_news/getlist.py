from rest_framework.views import APIView
from rest_framework.response import Response
from player.models.player import Player
from player_voice.models.fresh_news import FreshNews
from django.utils import timezone
import math

from mptt.templatetags.mptt_tags import cache_tree_children

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
            return value.strftime("%Y-%m-%d %H:%M:%S")

    def get(self, request):
        freshNews = FreshNews.objects.all().order_by('-createdtime')
        resp = []
        for item in freshNews:
            if item.parent != None:
                continue
            player = Player.objects.get(user__id=item.user_id)
            msg = {
                'id': item.id,
                'photo': player.photo,
                'username': player.user.username,
                'content': item.content,
                'since': self.time_since_zh(item.createdtime)
            }
            children = item.get_children()
            childLen = len(children)
            if childLen != 0:
                msg['children'] = []
                for child in children:
                    player = Player.objects.get(user__id=child.user_id)
                    msg['children'].append({
                        'id': child.id,
                        'photo': player.photo,
                        'username': player.user.username,
                        'content': child.content,
                        'since': self.time_since_zh(child.createdtime),
                        'reply': child.reply_to.username
                    })
            resp.append(msg)
        return Response({
            'result': "success",
            'freshNews': resp
        })

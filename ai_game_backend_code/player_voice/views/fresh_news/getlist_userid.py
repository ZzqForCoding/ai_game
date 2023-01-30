from rest_framework.views import APIView
from rest_framework.response import Response
from player_voice.pagination.fresh_news_pagination import FreshNewsPagination
from player_voice.models.fresh_news import FreshNews
from player_voice.models.player_like_fresh_news import Player_Like_Fresh_News
from player_voice.utils.time_since import time_since_zh
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
from mptt.templatetags.mptt_tags import cache_tree_children

class GetListForUserIdView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, userId):
        freshNews = FreshNews.objects.filter(parent=None, user__id=userId).order_by('-createdtime')
        pagination = FreshNewsPagination()
        page_freshNews = pagination.paginate_queryset(queryset=freshNews, request=request, view=self)
        resp = []
        for item in page_freshNews:
            player = Player.objects.get(user__id=item.user_id)
            pl = Player_Like_Fresh_News.objects.filter(user__id=userId, freshNews=item)
            forwarded_user = None
            if item.forwarded_id != -1: forwarded_user = FreshNews.objects.get(id=item.forwarded_id).user
            msg = {
                'id': item.id,
                'userId': player.user.id,
                'photo': player.photo,
                'username': player.user.username,
                'content': item.content,
                'since': time_since_zh(item.createdtime),
                'is_like': True if pl else False,
                'likes': item.likes,
                'forward_count': item.forward_count,
                'forwarded_id': item.forwarded_id,
                'forwarded_userId': -1 if item.forwarded_id == -1 else forwarded_user.id,
                'forwarded_username': "" if item.forwarded_id == -1 else forwarded_user.username,
            }
            children = item.get_children()
            childLen = len(children)
            if childLen != 0:
                msg['children'] = []
                for child in children:
                    player = Player.objects.get(user__id=child.user.id)
                    pl = Player_Like_Fresh_News.objects.filter(user__id=userId, freshNews=child)
                    msg['children'].append({
                        'id': child.id,
                        'userId': player.user.id,
                        'photo': player.photo,
                        'username': player.user.username,
                        'content': child.content,
                        'since': time_since_zh(child.createdtime),
                        'reply_id': child.reply_to.id,
                        'reply': child.reply_to.username,
                        'is_like': True if pl else False
                    })
            resp.append(msg)
        return Response({
            'result': "success",
            'freshNews': resp,
            'count': freshNews.count()
        })

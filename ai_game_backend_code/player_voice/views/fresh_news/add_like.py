from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews
from player_voice.models.player_like_fresh_news import Player_Like_Fresh_News

class AddLikeView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        freshNewsId = request.POST.get('freshNewsId', -1)
        if not user or freshNewsId == -1:
            return Response({
                'result': "点赞失败"
            })
        freshNews = FreshNews.objects.filter(id=freshNewsId)[0]
        if not freshNews:
            return Response({
                'result': "点赞失败"
            })

        t = Player_Like_Fresh_News.objects.create(user=user, freshNews=freshNews)
        t.save()
        freshNews.likes += 1
        freshNews.save()
        return Response({
            'result': "success"
        })




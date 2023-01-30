from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews

class RemoveView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        freshNewsId = request.POST.get('freshNewsId', 0)
        freshNews = FreshNews.objects.filter(id=freshNewsId)

        if not freshNews.exists():
            return Response({
                'result': "动态不存在或已被删除"
            })
        freshNews = freshNews[0]
        if freshNews.user != user:
            return Response({
                'result': "没有权限删除改动态"
            })
        if freshNews.forwarded_id != -1:
            forwarded_freshNews = FreshNews.objects.filter(id=freshNews.forwarded_id).first()
            forwarded_freshNews.forward_count -= 1
            forwarded_freshNews.save()
        freshNews.delete()
        return Response({
            'result': "success"
        })


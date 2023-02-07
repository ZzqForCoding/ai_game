from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews

class ForwardView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        forwarded_id = request.POST.get('forwarded_id', 0)

        if forwarded_id == 0:
            return Response({
                'result': "转发失败，请刷新页面"
            })
        forwarded_freshNews = FreshNews.objects.filter(id=forwarded_id)
        if forwarded_freshNews.exists():
            forwarded_freshNews = forwarded_freshNews.first()
            user = request.user
            freshNews = FreshNews.objects.create(user=user, content=forwarded_freshNews.content, forwarded_id=forwarded_id)
            freshNews.save()
            forwarded_freshNews.forward_count += 1
            forwarded_freshNews.save()
            return Response({
                'result': "success"
            })

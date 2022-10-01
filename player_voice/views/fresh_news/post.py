from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews

class PostView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        content = request.POST.get('content')

        map = {}
        if content == '':
            map['result'] = '内容不能为空'
            return Response(map)

        freshNews = FreshNews.objects.create(user=user, content=content)
        freshNews.save()
        map['result'] = 'success'
        return Response(map)

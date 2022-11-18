from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player_voice.models.fresh_news import FreshNews

class PostView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        data = request.POST
        user = request.user
        content = data.get('content')
        parent_id = data.get('parent_id', -1)

        map = {}
        if content == '':
            map['result'] = '内容不能为空'
            return Response(map)

        if len(content) > 5000:
            map['result'] = "内容长度不能超过5000个字符"
            return Response(map)

        freshNews = FreshNews.objects.create(user=user, content=content)

        if parent_id != -1:
            parent = FreshNews.objects.get(id=parent_id)
            freshNews.parent_id = parent.get_root().id
            freshNews.reply_to = parent.user

        freshNews.save()
        map['result'] = 'success'
        return Response(map)

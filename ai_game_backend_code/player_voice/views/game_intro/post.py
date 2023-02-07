from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player_voice.models.game_intro import GameIntro

class PostView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        data = request.POST
        user = request.user

        if not user.is_superuser:
            return Response({
                'result': "你没有权限发布网站说明"
            })
        title = data.get('title', "")
        content = data.get('content', "")
        is_post = data.get('isPost', False)

        gameIntro = GameIntro.objects.create(user=user, title=title, content=content, is_post=is_post)
        gameIntro.save()

        return Response({
            'result': 'success',
            'id': gameIntro.id,
        })

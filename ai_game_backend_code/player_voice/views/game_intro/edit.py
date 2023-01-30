from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player_voice.models.game_intro import GameIntro

class EditView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        data = request.POST
        user = request.user

        if not user.is_superuser:
            return Response({
                'result': "你没有权限修改网站说明"
            })
        gameIntroId = data.get('id', -1)
        gameIntro = GameIntro.objects.filter(id=gameIntroId)

        if gameIntro.exists():
            gameIntro = gameIntro.first()
        else:
            return Response({
                'result': "参数错误"
            })

        title = data.get('title', "")
        content = data.get('content', "")
        is_post = data.get('isPost', False)

        gameIntro.title = title
        gameIntro.content = content
        gameIntro.is_post = is_post
        gameIntro.save()

        return Response({
            'result': 'success'
        })

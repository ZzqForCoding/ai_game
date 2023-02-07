from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player_voice.models.game_intro import GameIntro

class RemoveView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        if not user.is_superuser:
            return Response({
                'result': "你没有权限删除网站说明"
            })
        gameIntroId = request.POST.get('id', -1)
        gameIntro = GameIntro.objects.filter(id=gameIntroId)

        if gameIntro.exists():
            gameIntro = gameIntro.first()
        else:
            return Response({
                'result': "参数错误"
            })

        gameIntro.delete()

        return Response({
            'result': 'success'
        })

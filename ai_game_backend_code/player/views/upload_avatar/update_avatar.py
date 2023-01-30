from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player

class UpdateAvatarView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        data = request.POST

        player = Player.objects.get(user=user)
        player.photo = data['imgUrl']
        player.save()

        return Response({
            'result': "success"
        })

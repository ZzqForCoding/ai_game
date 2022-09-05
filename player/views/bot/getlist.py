from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from player.models.bot import Bot

class GetListView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        user = request.user

        bots = Bot.objects.filter(user=user)

        resp = []
        for bot in bots:
            resp.append({
                'id': bot.id,
                'game': bot.game.name,
                'title': bot.title,
                'description': bot.description,
                'content': bot.content,
                'language': bot.language,
                'createtime': bot.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                'modifytime': bot.modifytime.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return Response(resp)

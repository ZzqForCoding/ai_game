from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from player.models.bot import Bot
from game.models.game import Game

class AddView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        data = request.POST
        user = request.user

        game_id = int(data['game_id'])
        title = data['title']
        description = data['description']
        content = data['content']

        map = {}
        if game_id == 0:
            map['result'] = '请选择游戏'
            return Response(map)

        if title == "":
            map['result'] = '标题不能为空'
            return Response(map)

        if len(title) > 100:
            map['result'] = '标题长度不能大于100'
            return Response(map)

        if description == "":
            description = "这个用户很懒，什么也没留下~"

        if len(description) > 300:
            map['result'] = 'Bot描述的长度不能大于300'
            return Response(map)

        if content == "":
            map['result'] = '代码不能为空'
            return Response(map)

        if len(content) > 10000:
            map['result'] = '代码长度不能超过10000'
            return Response(map)

        game = Game.objects.get(id=game_id)
        bot = Bot.objects.create(user=user, game=game, title=title, description = description, content = content)
        bot.save()
        map['result'] = 'success'

        return Response(map)

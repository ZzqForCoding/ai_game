from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot

class UpdateView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        data = request.POST

        bot_id = data['bot_id']
        title = data['title']
        description = data['description']
        language = data['language']
        content = data['content']

        map = {}
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

        if language == "":
            map['result'] = "语言不能为空"
            return Response(map)

        if content == "":
            map['result'] = '代码不能为空'
            return Response(map)

        if len(content) > 10000:
            map['result'] = '代码长度不能超过10000'
            return Response(map)

        bot = Bot.objects.filter(id=bot_id)

        if not bot:
            map['result'] = "Bot不存在或已被删除"
            return Response(map)

        bot = bot[0]
        if bot.user != user:
            map['result'] = '没有权限修改该Bot'
            return Response(map)

        # 若调用filter的update，是直接调用sql，而不经过model层，从而modifyTime不会自动更新。需要使用save
        bot.title = title
        bot.description = description
        bot.language = language
        bot.content = content
        bot.save()

        map['result'] = 'success'
        return Response(map)

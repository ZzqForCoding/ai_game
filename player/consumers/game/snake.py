from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.cache import cache
from django.contrib.auth.models import User
from player.models.player import Player
from player.models.bot import Bot
from player.consumers.game.utils.snake.game import Game

from .thrift.match_client.match.ttypes import Player as PlayerInfo
from .thrift.match_client.match import Match
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# 贪吃蛇游戏的ws逻辑
class MultiPlayerSnakeGame(AsyncWebsocketConsumer):
    users = {}

    # 在匹配界面会启动连接(得带token)
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
            self.room_name = None
            self.user = user
            self.game_id = 2
            MultiPlayerSnakeGame.users[self.user.id] = self
        else:
            await self.close()

    # 离开匹配界面断开连接
    async def disconnect(self, close_code):
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    #  开始匹配(2.0)
    async def start_match(self, data):
        if cache.get(self.user.id):
            return
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Match.Client(protocol)

        transport.open()

        def db_get_player():
            return Player.objects.get(user=self.user)

        player = await database_sync_to_async(db_get_player)()

        player_info = PlayerInfo(self.user.id, self.user.username,
                player.photo, player.rating, self.channel_name, int(data['operate']), int(data['botId']), self.game_id)

        client.add_player(player_info, "")
        cache.set(self.user.id, True, 3600)

        transport.close()

    async def stop_match(self, data):
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Match.Client(protocol)

        transport.open()

        def db_get_player():
            return Player.objects.get(user=self.user)

        player = await database_sync_to_async(db_get_player)()

        player_info = PlayerInfo(self.user.id, self.user.username,
                player.photo, player.rating, self.channel_name, int(data['operate']), int(data['botId']), self.game_id)
        client.remove_player(player_info, "")
        cache.delete_pattern(self.user.id)

        transport.close()

    # 移动
    async def move(self, direction):
        if MultiPlayerSnakeGame.users[self.user.id].game.playerA.id == self.user.id:
            if MultiPlayerSnakeGame.users[self.user.id].game.playerA.botId == -1:
                self.game.setNextStepA(direction, "", "", "")
        elif MultiPlayerSnakeGame.users[self.user.id].game.playerB.id == self.user.id:
            if MultiPlayerSnakeGame.users[self.user.id].game.playerB.botId == -1:
                self.game.setNextStepB(direction, "", "", "")

    # 辅助函数：发送给当前房间玩家信息
    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

    async def receive_bot_move(self, data):
        dir = data['result']
        try:
            dir = int(dir)
            if dir < 0 or dir > 3:
                return
        except:
            print("illegal: ", dir)
            return

        if MultiPlayerSnakeGame.users[self.user.id].game.playerA.id == data['user_id']:
            self.game.setNextStepA(int(data['result']), data['compile'], data['output'], data['result'])
        elif MultiPlayerSnakeGame.users[self.user.id].game.playerB.id == data['user_id']:
            self.game.setNextStepB(int(data['result']), data['compile'], data['output'], data['result'])

    async def send_message(self, data):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': "group_send_event",
                'event': "pk_message",
                'msg': {
                    'username': data['username'],
                    'photo': data['photo'],
                    'text': data['text'],
                }
            }
        )

    async def start_snake_game(self, data):
        self.room_name = data['room_name']
        if self.user.id == data['a_id']:
            a_id = data['a_id']
            a_username = data['a_username']
            a_photo = data['a_photo']
            b_id = data['b_id']
            b_username = data['b_username']
            b_photo = data['b_photo']
            room_name = data['room_name']

            def db_get_bot(id):
                return Bot.objects.get(id=id)

            botA = None
            if data['a_operate'] == 0:
                botA = await database_sync_to_async(db_get_bot)(int(data['a_bot_id']))

            botB = None
            if data['b_operate'] == 0:
                botB = await database_sync_to_async(db_get_bot)(int(data['b_bot_id']))

            # 创建地图
            game = Game(13, 14, 20, a_id, botA, b_id, botB, room_name)
            game.createMap()
            # 一局游戏一个线程
            game.start()
            MultiPlayerSnakeGame.users[a_id].game = game
            MultiPlayerSnakeGame.users[b_id].game = game
            # 返回给玩家的信息
            resp = {
                'a_id': game.playerA.id,
                'a_language': "" if botA == None else botA.language,
                'a_is_robot': True if botA != None else False,
                'b_id': game.playerB.id,
                'b_language': "" if botB == None else botB.language,
                'b_is_robot': True if botB != None else False,
                'map': game.getG()
            }
            # 广播给当前房间的所有玩家
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': "group_send_event",
                    'event': "start_game",
                    'username': a_username,
                    'photo': a_photo,
                    'game': resp
                }
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': "group_send_event",
                    'event': "start_game",
                    'username': b_username,
                    'photo': b_photo,
                    'game': resp
                }
            )

    # 前端发送的信息
    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == 'start_match':
            await self.start_match(data)
        elif event == 'stop_match':
            await self.stop_match(data)
        elif event == "move":
            await self.move(data['direction'])
        elif event == "pk_message":
            await self.send_message(data)

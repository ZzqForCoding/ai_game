from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.cache import cache
from django.contrib.auth.models import User
from player.consumers.game.utils.snake.game import Game

# 贪吃蛇游戏的ws逻辑
class MultiPlayerGame(AsyncWebsocketConsumer):
    users = {}

    # 在匹配界面会启动连接(得带token)
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
            self.user = user
            MultiPlayerGame.users[self.user.id] = self
            print('accept')
        else:
            await self.close()

    # 离开匹配界面断开连接
    async def disconnect(self, close_code):
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # 开始匹配
    async def start_match(self, data):
        print('start_match')
        self.room_name = None
        # 找房间
        start = 0
        for i in range(start, 100000000):
            name = "room-%d" % (i)
            if not cache.has_key(name) or len(cache.get(name)) < 2:
                self.room_name = name
                break

        # 爆满则不能匹配
        if not self.room_name:
            return

        # 找到了房间，但是此房间未创建则存到redis里
        if not cache.has_key(self.room_name):
            cache.set(self.room_name, [], 3600)

        # 将房间里已有的玩家告诉给当前玩家
        for player in cache.get(self.room_name):
            await self.send(text_data=json.dumps({
                'event': "start_match",
                'username': player['username'],
                'photo': player['photo']
            }))

        # 将房间加入django channels维护的channel layers中
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        # 获取redis中房间已有玩家
        players = cache.get(self.room_name)
        # 加入当前玩家
        players.append({
            'username': data['username'],
            'photo': data['photo']
        })
        # 将玩家存入redis中
        cache.set(self.room_name, players, 3600)
        # consumer中访问数据库需要调用函数
        def db_get_user(username):
            return User.objects.get(username=username)
        # 当当前房间人数 >= 2则匹配成功
        if len(players) >= 2:
            # 因为贪吃蛇游戏一局两个人，获取两名玩家
            a = await database_sync_to_async(db_get_user)(players[0]['username'])
            b = await database_sync_to_async(db_get_user)(players[1]['username'])
            # 创建地图
            game = Game(13, 14, 20, a.id, b.id, self.room_name)
            game.createMap()
            # 一局游戏一个线程
            game.start()
            MultiPlayerGame.users[a.id].game = game
            MultiPlayerGame.users[b.id].game = game
            # 返回给玩家的信息
            resp = {
                'a_id': game.playerA.id,
                'a_sx': game.playerA.sx,
                'a_sy': game.playerA.sy,
                'b_id': game.playerB.id,
                'b_sx': game.playerB.sx,
                'b_sy': game.playerB.sy,
                'map': game.getG()
            }
            # 广播给当前房间的所有1玩家
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': "group_send_event",
                    'event': "start_match",
                    'username': data['username'],
                    'photo': data['photo'],
                    'game': resp
                }
            )

    # 停止匹配
    async def stop_match(self, data):
        print('stop_match')
        player = {
            'username': data['username'],
            'photo': data['photo']
        }
        start = 0
        for i in range(start, 100000000):
            room_name = "room-%d" % (i)
            if cache.get(room_name) != None and len(cache.get(room_name)) < 2:
                players = cache.get(room_name)
                if player in players:
                    players.remove(player)
                    cache.set(room_name, players)
                    # 清除channel layer中的房间
                    await self.channel_layer.group_discard(room_name, self.channel_name)
                    break

    # 移动
    async def move(self, direction):
        print(self.user.id, direction)
        if MultiPlayerGame.users[self.user.id].game.playerA.id == self.user.id:
            self.game.setNextStepA(direction)
        elif MultiPlayerGame.users[self.user.id].game.playerB.id == self.user.id:
            self.game.setNextStepB(direction)

    # 辅助函数：发送给当前房间玩家信息
    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

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

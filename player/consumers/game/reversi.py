from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.cache import cache
from django.contrib.auth.models import User
from player.models.player import Player
from player.models.bot import Bot
from player.consumers.game.utils.cell import Cell
from player.consumers.game.utils.reversi.game import Game

from .thrift.match_client.match.ttypes import Player as PlayerInfo
from .thrift.match_client.match import Match
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class MultiPlayerReversiGame(AsyncWebsocketConsumer):
    users = {}

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
            self.room_name = None
            self.user = user
            self.game_id = 3
            MultiPlayerReversiGame.users[self.user.id] = self
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

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

    async def start_reversi_game(self, data):
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

            game = Game(8, 8, a_id, botA, b_id, botB, room_name)
            game.start()
            MultiPlayerReversiGame.users[a_id].game = game
            MultiPlayerReversiGame.users[b_id].game = game

            resp = {
                'a_id': game.playerA.id,
                'b_id': game.playerB.id,
                'current_round': game.playerA.id
            }

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

    async def next_round(self, cell):
        if MultiPlayerReversiGame.users[self.user.id].game.playerA.id == self.user.id and MultiPlayerReversiGame.users[self.user.id].game.currentRound == self.user.id:
            self.game.setNextCellA(cell)
        elif MultiPlayerReversiGame.users[self.user.id].game.playerB.id == self.user.id and MultiPlayerReversiGame.users[self.user.id].game.currentRound == self.user.id:
            self.game.setNextCellB(cell)

    async def toggle_round(self):
        self.game.setToggleRound()

    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == 'start_match':
            await self.start_match(data)
        elif event == 'stop_match':
            await self.stop_match(data)
        elif event == 'pk_message':
            await self.send_message(data)
        elif event == 'next_round':
            await self.next_round(Cell(data['x'], data['y']))
        elif event == 'toggle_round':
            await self.toggle_round()

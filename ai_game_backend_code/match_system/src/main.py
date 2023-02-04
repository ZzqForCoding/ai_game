import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])

from match_service import Match
from match_service.ttypes import Player

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from queue import Queue
from time import sleep
from threading import Thread

from ai_game_platform.asgi import channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

queue = Queue()     # 消息队列

class Operate:
    def __init__(self, type, player):
        self.type = type
        self.player = player

class Pool:
    def __init__(self):
        self.players = []
        self.wt = []

    def add_player(self, player):
        self.players.append(player)
        self.wt.append(0)
        gameCnt = cache.get('game_cnt', 0)
        if gameCnt >= 5:
            async_to_sync(channel_layer.group_send) (
                "matching-player-%d" % player.id,
                {
                    'type': "group_send_event",
                    'event': "prompt",
                    'prompt': "由于当前平台资源不足, 正在进行>=5场游戏，请耐心等待...",
                }
            )

    def remove_player(self, player):
        for i in range(len(self.players)):
            if self.players[i].id == player.id:
                del self.players[i]
                del self.wt[i]
                print("删除%d成功" % i)
                break

    def check_match(self, i, j):
        playerA = self.players[i]
        playerB = self.players[j]
        if playerA.game_id != playerB.game_id: return False
        # 防止相同玩家匹配在一起
        if playerA.id == playerB.id:
            return False
        dt = abs(playerA.rating - playerB.rating)
        waitingtime = self.wt[i] if self.wt[i] < self.wt[j] else self.wt[j]
        return dt <= waitingtime * 50

    def match_success(self, ps):
        print("Match Success: %s %s" % (ps[0].username, ps[1].username))
        room_name = "room-%s-%s" % (ps[0].id, ps[1].id)
        type = ""
        if ps[0].game_id == 1:
            type = "start_gobang_game"
            cache.set('gobang_matching_players', cache.get('gobang_matching_players', 0) - len(ps))
        elif ps[0].game_id == 2:
            type = "start_snake_game"
            cache.set('snake_matching_players', cache.get('snake_matching_players', 0) - len(ps))
        elif ps[0].game_id == 3:
            type = "start_reversi_game"
            cache.set('reversi_matching_players', cache.get('reversi_matching_players', 0) - len(ps))
        players = []
        for p in ps:
            async_to_sync(channel_layer.group_discard)("matching-player-%d" % p.id, p.channel_name)
            async_to_sync(channel_layer.group_add)(room_name, p.channel_name)
            players.append({
                'username': p.username,
                'photo': p.photo,
            })
        cache.set(room_name, players, 3600)     # 有效时间: 一小时
        async_to_sync(channel_layer.group_send) (
            room_name,
            {
                'type': type,
                'room_name': room_name,
                'a_id': ps[0].id,
                'a_username': ps[0].username,
                'a_photo': ps[0].photo,
                'a_operate': ps[0].operate,
                'a_bot_id': ps[0].bot_id,
                'b_id': ps[1].id,
                'b_username': ps[1].username,
                'b_photo': ps[1].photo,
                'b_operate': ps[1].operate,
                'b_bot_id': ps[1].bot_id
            }
        )


    def increase_waiting_time(self):
        for i in range(len(self.wt)):
            self.wt[i] += 1

    def match(self):
        if cache.get('game_cnt', 0) >= 5: return

        while len(self.players) > 1:
            flag = False
            for i in range(len(self.players)):
                for j in range(i + 1, len(self.players)):
                    if self.check_match(i, j):
                        playerA = self.players[i]
                        playerB = self.players[j]
                        self.match_success([playerA, playerB])
                        self.players = self.players[:i] + self.players[i + 1:j] + self.players[j + 1:]
                        self.wt = self.wt[:i] + self.wt[i + 1:j] + self.wt[j + 1:]
                        flag = True
                        break
                if flag: break
            if not flag: break
            if cache.get('game_cnt', 0) >= 5: break
        self.increase_waiting_time()

class MatchHandler:
    def add_player(self, player):
        print("Add Player: %s %d" % (player.username, player.rating))
        op = Operate("add", player)
        queue.put(op)
        return 0

    def remove_player(self, player):
        print("Remove Player: %s %d" % (player.username, player.rating));
        op = Operate("remove", player)
        queue.put(op)
        return 0

def get_operate_from_queue():
    try:
        return queue.get_nowait()
    except:
        return None

def worker():
    pool = Pool()
    while True:
        op = get_operate_from_queue()
        if op:
            if op.type == "add":
                pool.add_player(op.player)
            else:
                pool.remove_player(op.player)
        else:
            pool.match()
            sleep(1)

if __name__ == '__main__':
    handler = MatchHandler()
    processor = Match.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    Thread(target=worker, daemon=True).start()      # 开一个线程

    print('Starting the server...')
    server.serve()
    print('done.')

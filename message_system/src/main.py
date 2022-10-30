import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])

from message_server.message import Message

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from ai_game_platform.asgi import channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache
from player.consumers.game.utils.snake.game import Game

class MessageHandler:
    def response(self, info):
        info = eval(info)
        if info['type'] == "match":
            ps = info['players']
            room_name = "room-%s-%s" % (ps[0]['id'], ps[1]['id'])
            type = ""
            if info['game_id'] == 1:
                type = "start_gobang_game"
            elif info['game_id'] == 2:
                type = "start_snake_game"
            elif info['game_id'] == 3:
                type = "start_reversi_game"
            players = []
            for p in ps:
                async_to_sync(channel_layer.group_add)(room_name, p['channel_name'])
                players.append({
                    'username': p['username'],
                    'photo': p['photo']
                })
            cache.set(room_name, players, 3600)

            async_to_sync(channel_layer.group_send) (
                room_name,
                {
                    'type': type,
                    'room_name': room_name,
                    'a_id': ps[0]['id'],
                    'a_username': ps[0]['username'],
                    'a_photo': ps[0]['photo'],
                    'a_operate': ps[0]['operate'],
                    'a_bot_id': ps[0]['bot_id'],
                    'b_id': ps[1]['id'],
                    'b_username': ps[1]['username'],
                    'b_photo': ps[1]['photo'],
                    'b_operate': ps[1]['operate'],
                    'b_bot_id': ps[1]['bot_id'],
                }
            )
        elif info['type'] == "bot_move":
            async_to_sync(channel_layer.group_send) (
                info['room_name'],
                {
                    'type': "receive_bot_move",
                    'user_id': info["user_id"],
                    'compile': info["compile"],
                    'output': info["output"],
                    'result': info["result"],
                    'status': info["status"],
                }
            )

        return 0

if __name__ == '__main__':
    handler = MessageHandler()
    processor = Message.Processor(handler)
    transport = TSocket.TServerSocket(host='172.17.0.3', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting Message server...')
    server.serve()

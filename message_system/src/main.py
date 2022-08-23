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
                    'type': "start_snake_game",
                    'room_name': room_name,
                    'a_id': ps[0]['id'],
                    'a_username': ps[0]['username'],
                    'a_photo': ps[0]['photo'],
                    'b_id': ps[1]['id'],
                    'b_username': ps[1]['username'],
                    'b_photo': ps[1]['photo']
                }
            )

        return 0

if __name__ == '__main__':
    handler = MessageHandler()
    processor = Message.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')

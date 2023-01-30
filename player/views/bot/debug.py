from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from player.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot
from player.models.player import Player

from player.consumers.game.thrift.code_running_client.code_running_service import CodeRunning
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import uuid
import json

class DebugView(APIView):
    permission_classes = ([OneUserLogin])

    def post(self, request):
        user = request.user
        data = request.POST

        id = str(uuid.uuid1())
        code = data['code'].strip()
        lang = data['lang'].strip()
        data = data['data'].strip()

        player = Player.objects.get(user=user)
        if lang == 'cpp':
            player.cpp_code_compile_cnt += 1
        elif lang == 'java':
            player.java_code_compile_cnt += 1
        elif lang == 'python':
            player.py_code_compile_cnt += 1

        try:
            # estab connect
            # Make socket
            ransport = TSocket.TSocket('backend', 15671)
            # Buffering is critical. Raw sockets are very slow
            transport = TTransport.TBufferedTransport(transport)
            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            # Create a client to use the protocol encoder
            client = CodeRunning.Client(protocol)
            # Connect!
            transport.open()
            # 开启容器
            client.start_container(id, code, lang)
            # 编译
            compileInfo = json.loads(client.compile(id))
            resp = {}
            if compileInfo['returncode'] == 0:
                # 运行
                client.prepare_data(id, data)
                runInfo = json.loads(client.run(id))
                if runInfo['returncode'] == 0:
                    if lang == 'cpp':
                        player.cpp_code_compile_success_cnt += 1
                    elif lang == 'java':
                        player.java_code_compile_success_cnt += 1
                    elif lang == 'python':
                        player.py_code_compile_success_cnt += 1

                    resp['status'] = "Finished"
                    resp['output'] = runInfo['output']
                    resp['time'] = runInfo['time']
                else:
                    resp['status'] = runInfo['status']
                    resp['desp'] = runInfo['desp']
            else:
                resp['status'] = compileInfo['status']
                resp['output'] = compileInfo['desp']
            return Response(resp)
        except Exception as e:
            return Response({
                'status': "Internal Error",
                'output': str(e)
            })
        finally:
            player.save()
            # 关闭容器
            client.stop_container(id)
            transport.close()


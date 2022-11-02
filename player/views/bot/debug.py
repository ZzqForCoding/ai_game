from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.bot import Bot

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
        data = request.POST

        id = str(uuid.uuid1())
        code = data['code'].strip()
        lang = data['lang'].strip()
        data = data['data'].strip()
        try:
            # estab connect
            # Make socket
            transport = TSocket.TSocket('120.76.157.21', 20104)
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
            # 关闭容器
            client.stop_container(id)
            transport.close()


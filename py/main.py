from code_running import CodeRunning
from code_running.ttypes import Bot

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import docker

class CodeRunningHandler:
    def add_bot_code(self, bot, info):
        client = docker.from_env()
        container = client.containers.get('6ed0654416c4');
        a = container.exec_run(b"/bin/bash -c 'echo '" + bot.botCode  + "'  > /tmp/code.cpp'")
        print(a)
        return 0

if __name__ == '__main__':
    handler = CodeRunningHandler()
    processor = CodeRunning.Processor(handler)
    transport = TSocket.TServerSocket(host='172.17.0.2', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(
        processor, transport, tfactory, pfactory)
    print('Starting the server...')
    server.serve()

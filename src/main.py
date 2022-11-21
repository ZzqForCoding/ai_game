from code_running_service import CodeRunning
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from sandbox import Sandbox

class CodeRunningHandler:
    def start_container(self, uuid, code, lang):
        if Sandbox.bots.get(uuid) == None:
            Sandbox.bots[uuid] = Sandbox(uuid, code, lang)
        return 0

    def stop_container(self, uuid):
        sandbox = Sandbox.bots.get(uuid)
        if sandbox is not None:
            sandbox.stop()
            del Sandbox.bots[uuid]
        return 0

    def compile(self, uuid):
        sandbox = Sandbox.bots.get(uuid)
        if sandbox is not None:
            result = sandbox.compile()
            if result != 'ok':
                return result
        return ""

    def prepare_data(self, uuid, data):
        sandbox = Sandbox.bots.get(uuid)
        if sandbox is not None:
            sandbox.prepare_data(data)
        return 0

    def run(self, uuid):
        output = None
        sandbox = Sandbox.bots.get(uuid)
        if sandbox is not None:
            output = sandbox.run().strip()
        return output

if __name__ == '__main__':
    handler = CodeRunningHandler()
    processor = CodeRunning.Processor(handler)
    transport = TSocket.TServerSocket(host='172.17.0.2', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')

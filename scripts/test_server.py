import socket
from typing import List

from src.tej_protoc import protocol
from src.tej_protoc.callbacks import ResponseCallback
from src.tej_protoc.file import File

from src.tej_protoc.server import TPServer


class MessageCallback(ResponseCallback):
    def connected(self, client: socket.socket):
        print('Client connected')
        protocol.send(client, protocol.BytesBuilder().set_message('Hello'.encode()).bytes())

    def received(self, files: List[File], message_data: bytes):
        print('Message:', message_data.decode())
        self.client.send(protocol.BytesBuilder().set_message(message_data).bytes())


print('Server is running...')
server = TPServer('localhost', 8000, MessageCallback)
server.listen(run_background=True)

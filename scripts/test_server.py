import os
import socket
import sys
from typing import List

from tej_protoc import protocol
from tej_protoc.callbacks import ResponseCallback
from tej_protoc.file import File

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.server import TPServer


class MessageCallback(ResponseCallback):
    def connected(self, client: socket.socket):
        print('Client connected')

    def received(self, files: List[File], message_data: bytes):
        print('Message:', message_data.decode())
        self.client.send(protocol.BytesBuilder().set_message(message_data).bytes())


print('Server is running...')
server = TPServer('localhost', 8000, MessageCallback)
server.listen(run_background=True)

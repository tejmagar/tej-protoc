import socket
from typing import List

from tej_protoc import callbacks, protocol
from tej_protoc.client import TPClient
from tej_protoc.file import File


class ClientCallback(callbacks.ResponseCallback):
    def connected(self, client: socket.socket):
        print('connected')
        data = protocol.BytesBuilder().add_file('file.txt', b'1' * 1024 * 1024).bytes()
        for e in range(10):
            self.send(data)

    def received(self, files: List[File], message_data: bytes):
        pass


server = TPClient('127.0.0.1', 8001, ClientCallback, timeout=3)
server.listen()

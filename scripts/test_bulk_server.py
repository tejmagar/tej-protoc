from typing import List

from tej_protoc import callbacks
from tej_protoc.file import File
from tej_protoc.server import TPServer


class ServerCallback(callbacks.ResponseCallback):
    def received(self, files: List[File], message_data: bytes):
        print('---- Received in client ----')
        print('Custom status: ', self.custom_status)

        for file in files:
            print(file.name)

        if message_data:
            print('Message: ', message_data.decode())
        print('---------------------------------')


print('Running server at 127.0.0.1:8001')
server = TPServer('127.0.0.1', 8001, ServerCallback, timeout=3)
server.listen()

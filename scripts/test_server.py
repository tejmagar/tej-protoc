import socket

from typing import List

from tej_protoc.callbacks import ResponseCallback
from tej_protoc.exceptions import ConnectionClosed
from tej_protoc.file import File

from tej_protoc.server import TPServer
from tej_protoc.ping import protocol, Ping


class MessageCallback(ResponseCallback):
    ping = None

    def connected(self, client: socket.socket):
        print('Client connected')
        builder = protocol.BytesBuilder(20)
        builder.add_file('a.txt', b'10' * 1000)
        builder.add_file('b.txt', b'10' * 1000)
        builder.set_message('Hey'.encode()).bytes()
        protocol.send(client, builder.bytes())
        ping = Ping(self.client, 4)
        ping.start()

    def received(self, files: List[File], message_data: bytes):
        if message_data:
            print('Message:', message_data.decode())

        if files:
            print('Received file')

    def disconnected(self):
        print('Client disconnected')


print('Server is running...')
server = TPServer('localhost', 8000, MessageCallback)
server.listen()

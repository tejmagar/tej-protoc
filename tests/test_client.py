import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.client import Client
from src.tej_protoc import protocol


class ClientCallback(protocol.Callback):
    def start(self, client):
        print('Connected to server...')

    def receive(self, files, message):
        print('---- Received in client ----')
        for file in files:
            print(file.name)

        print('Message: ', message.decode())
        print('---------------------------------')

        builder = protocol.BytesBuilder()
        builder.add_file('hello.txt', b'randombytes')
        builder.add_file('hello.txt', b'randombytes')
        builder.set_message(b'Hello')
        self.client.send(builder.bytes())


try:
    client = Client('localhost', 8000, ClientCallback)
    client.listen(True)
except Exception as e:
    print('error', e)

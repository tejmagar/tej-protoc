import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.client import Client
from src.tej_protoc import protocol


class ClientCallback(protocol.Callback):
    def start(self):
        print('Connected to server...')
        builder = protocol.BytesBuilder()
        builder.set_message(b'Hello')
        self.client.send(builder.bytes())

    def receive(self, files, message):
        print('---- Received in client ----')
        for file in files:
            print(file.name)

        print('Message: ', message.decode())
        print('---------------------------------')


try:
    client = Client('localhost', 8000, ClientCallback)
    client.listen(True)
except Exception as e:
    print('error', e)

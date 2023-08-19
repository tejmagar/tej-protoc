import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.client import Client
from src.tej_protoc import protocol


class CustomCallback(protocol.SendCallback):
    def __init__(self):
        self.total_sent = 0

    def progress(self, sent_bytes, total_bytes):
        self.total_sent += sent_bytes
        print(f'Sending ===> {self.total_sent} / {total_bytes}')


builder = protocol.BytesBuilder()
builder.add_file('a.txt', b'a' * int(1000 * 1024 * 1024))
builder.set_message(b'Hello')
data = builder.bytes()


class ClientCallback(protocol.Callback):
    def start(self):
        print('Connected to server...')

        for _ in range(2):
            print('sending')
            import time
            start = time.time()
            self.client.send(data)
            end = time.time()
            print('Completed in: ', end - start)
            print('\n')

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

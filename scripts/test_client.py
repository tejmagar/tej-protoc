import os
import socket
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.client import TPClient
from src.tej_protoc import protocol


class ClientCallback(protocol.ResponseCallback):
    def connected(self, client: socket.socket):
        print('Connected to server...')

    def received(self, files, message):
        print('---- Received in client ----')
        for file in files:
            print(file.name)

        print('Message: ', message.decode())
        print('---------------------------------')


def test_client():
    try:
        client = TPClient('localhost', 8000, ClientCallback)
        client.listen()
    except Exception as e:
        print('error', e)


test_client()

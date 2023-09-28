from typing import List
import socket

from tej_protoc.file import File


class ResponseCallback:
    client: socket.socket = None
    custom_status: int = 0
    protocol_version: int = 0

    def connected(self, client: socket.socket):
        pass

    def received(self, files: List[File], message_data: bytes):
        pass

    def disconnected(self):
        pass

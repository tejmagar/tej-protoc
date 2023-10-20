import socket
import threading
import time
from time import sleep
from typing import Optional

from tej_protoc import callbacks, protocol
from tej_protoc.exceptions import ConnectionClosed
from tej_protoc.logger import Log
from tej_protoc.status import StatusCode


class Ping:

    def __init__(self, client: socket.socket, ping_sleep: float):
        self.client = client
        self.ping_sleep: float = ping_sleep
        self.socket_timeout: int = 3

        self.__ping_bytes__ = protocol.BytesBuilder(StatusCode.PING).bytes()

    def __ping__(self):
        """
        Ping will be started in separate thread
        """

        while True:
            try:
                protocol.send(self.client, self.__ping_bytes__, self.socket_timeout)
            except (socket.error, ConnectionClosed):
                break  # Break loop if ping fails

            sleep(self.ping_sleep)

    def start(self):
        """ Sends periodic ping bytes """

        thread = threading.Thread(target=self.__ping__)
        thread.daemon = True
        thread.start()

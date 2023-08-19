import select
import socket
import threading
from typing import Type, Optional

from . import protocol
from .protocol import FrameReader


class Client:
    def __init__(self, host: str, port: int, callback_class: Type[protocol.Callback], **kwargs):
        self.__host = host
        self.__port = port
        self.__callback_class = callback_class
        self.__is_running = True

        self.__run_background = kwargs.get('run_background', False)
        self.__is_daemon = kwargs.get('daemon', False)
        self.__client__: Optional[socket.socket] = None

        self.buffer_size = None
        self.__init_client()

    def __init_client(self):
        self.__client__ = socket.socket()
        self.__client__.connect((self.__host, self.__port))

    def __listen(self):
        callback = self.__callback_class(self.__client__)
        callback.start()

        frame_reader = FrameReader(self.buffer_size)

        while self.__is_running:
            readable, _, _ = select.select([self.__client__], [], [], 0.00000001)

            if self.__client__ in readable:
                protocol.read(self.__client__, callback, frame_reader)

            if not self.__is_running:
                self.__client__.close()
                break

    def listen(self, run_background: bool = False, is_daemon: bool = False):
        self.__run_background = run_background
        self.__is_daemon = is_daemon

        if run_background:
            thread = threading.Thread(target=self.__listen)
            thread.daemon = is_daemon
            thread.start()
        else:
            self.__listen()

    def disconnect(self):
        self.__is_running = False

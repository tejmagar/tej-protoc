import socket
import threading
from typing import Type, Optional

from . import protocol
from .callbacks import ResponseCallback
from .exceptions import ConnectionClosed
from .logger import Log
from .protocol import FrameReader


class TPClient:
    def __init__(self, host: str, port: int, callback_class: Type[ResponseCallback]):
        self.__client__: Optional[socket.socket] = socket.create_connection((host, port))
        self.__callback_class__: Type[ResponseCallback] = callback_class
        self.frame_reader: FrameReader = FrameReader()

    def __listen__(self):
        """ Reads incoming client messages and files. """

        callback = self.__callback_class__()
        callback.client = self.__client__
        callback.connected(self.__client__)

        while True:
            try:
                protocol.read(self.__client__, callback, self.frame_reader)
            except ConnectionClosed as e:
                if type(e) == ConnectionClosed:
                    Log.debug('TPClient', f'Connection closed')

                else:
                    Log.error('TPClient', e)

                break  # Stop listening incoming files and messages

        self.__client__ = None
        callback.disconnected()

    def listen(self, **kwargs):
        """
        Pass run_background=True to run in background and is_daemon=True to set background thread as daemon thread.
        """

        run_background = kwargs.get('run_background', False)
        is_daemon = kwargs.get('is_daemon', False)

        if run_background:
            thread = threading.Thread(target=self.__listen__)
            thread.daemon = is_daemon
            thread.start()

        else:
            self.__listen__()

    def get_client(self):
        return self.__client__

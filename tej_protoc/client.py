import socket
import traceback
import threading
from typing import Type, Optional

from .callbacks import ResponseCallback
from .exceptions import ConnectionClosed
from .logger import Log
from .protocol import TPFrameReader


class TPClient:
    def __init__(self, host: str, port: int, callback_class: Type[ResponseCallback], timeout: int = None):
        self.__client__: Optional[socket.socket] = socket.create_connection((host, port))
        self.__callback_class__: Type[ResponseCallback] = callback_class
        self.timeout = timeout
        self.tp_frame_reader: TPFrameReader = TPFrameReader(timeout)

    def __listen__(self):
        """ Reads incoming client messages and files. """

        callback = self.__callback_class__()
        callback.socket_timeout = self.timeout
        callback.client = self.__client__
        callback.connected(self.__client__)

        last_exception = None

        while True:
            try:
                self.tp_frame_reader.read(self.__client__, callback)
            except Exception as error:
                if isinstance(error, ConnectionClosed):
                    Log.debug('TPClient', f'Connection closed')

                else:
                    last_exception = error
                    Log.error('TPClient', 'Error occurred')

                break  # Stop listening incoming files and messages

        self.__client__.close()
        self.__client__ = None
        callback.disconnected()

        if last_exception:
            raise last_exception

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

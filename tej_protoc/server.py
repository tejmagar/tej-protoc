from time import sleep
from typing import Any, Type

import socket
import threading
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, FIRST_EXCEPTION

from .callbacks import ResponseCallback
from .exceptions import ConnectionClosed
from .logger import Log
from .protocol import TPFrameReader


class TPServer:
    def __init__(self, host: str, port: int, callback_class: Type[ResponseCallback], timeout: int = None):
        self.__server__: socket.socket = socket.create_server((host, port), reuse_port=True)
        self.__callback_class__: Type[ResponseCallback] = callback_class
        self.timeout = timeout
        self.tp_frame_reader: TPFrameReader = TPFrameReader(timeout)

    def add_sock_opt(self, *args, **kwargs):
        self.__server__.setsockopt(*args, **kwargs)

    def __event__(self, callback):
        pass

    def __handle_events__(self, client: socket.socket, address: tuple[str, int]) -> None:
        """ Handles individual client event. """
        callback: ResponseCallback = self.__callback_class__()
        callback.socket_timeout = self.timeout
        callback.client = client
        callback.connected(client)

        while True:
            try:
                self.tp_frame_reader.read(client, callback)

            except (socket.error, Exception) as error:
                # Do necessary cleanups
                client.close()
                callback.disconnected()

                if isinstance(error, ConnectionClosed) or isinstance(error, socket.error):
                    Log.debug('TPServer', f'Connection closed {address[0]}:{address[1]}')

                else:
                    raise error

                break

    def __serve__(self) -> None:
        """ Accepts and serves clients. """

        while True:
            client, address = self.__server__.accept()

            # Handle each individual clients in separate thread
            thread = threading.Thread(target=self.__handle_events__, args=(client, address))
            thread.start()

    def listen(self, **kwargs: Any) -> None:
        """ Start listening incoming connections. """

        run_background = kwargs.get('run_background', False)
        is_daemon = kwargs.get('is_daemon', False)

        if run_background:
            thread = threading.Thread(target=self.__serve__)
            thread.daemon = is_daemon
            thread.start()

        else:
            self.__serve__()

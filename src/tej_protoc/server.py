from typing import Any, Type

import socket
import threading

from . import protocol
from .callbacks import ResponseCallback
from .exceptions import ConnectionClosed
from .logger import Log
from .protocol import FrameReader


class TPServer:
    def __init__(self, host: str, port: int, callback_class: Type[ResponseCallback]):
        self.__server__: socket.socket = socket.create_server((host, port), reuse_port=True)
        self.__callback_class__: Type[ResponseCallback] = callback_class
        self.frame_reader: FrameReader = FrameReader()

    def __handle_events__(self, client: socket.socket, address: tuple[str, int]) -> None:
        """Handles individual client event. """

        callback = self.__callback_class__()
        callback.client = client
        callback.connected(client)

        while True:
            try:
                protocol.read(client, callback, self.frame_reader)
            except ConnectionClosed as e:
                if type(e) == ConnectionClosed:
                    Log.debug('TPServer', f'Connection closed {address[0]}:{address[1]}')

                else:
                    Log.error('TPServer', e)
                break

        callback.disconnected()

    def __serve__(self) -> None:
        """ Accepts and serves clients """

        while True:
            client, address = self.__server__.accept()

            # Handle each individual clients
            self.__handle_events__(client, address)

    def listen(self, **kwargs: Any) -> None:
        """ Starting listening incoming connections. """

        run_background = kwargs.get('run_background', False)
        is_daemon = kwargs.get('is_daemon', False)

        if run_background:
            thread = threading.Thread(target=self.__serve__)
            thread.daemon = is_daemon
            thread.start()

        else:
            self.__serve__()

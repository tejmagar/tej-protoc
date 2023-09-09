from typing import Tuple, Any, Type

import importlib
import subprocess
import socket
import threading

from . import protocol
from .logger import Log
from .protocol import FrameReader


class Server:
    def __init__(self, host: str, port: int, callback_class: Type[protocol.Callback], **kwargs):
        self.server = kwargs.get('sock')
        self.__host = host
        self.__port = port

        self.__log = kwargs.get('log', False)
        self.__callback_class = callback_class

        self.__run_background = False
        self.__is_daemon = False

        self.__ngrok_auth_token = None
        self.__ngrok_url = None
        self.__ngrok_tunnel_created = False

        self.kwargs = kwargs
        self.max_buffer_size = None
        self.__init_server()

    def __init_server(self):
        self.__server = self.server

        if not self.__server:
            self.__server = socket.create_server((self.__host, self.__port), reuse_port=True)
            self.__server.listen()

    def __log_event(self, message: Any):
        if self.__log:
            Log.info(tag='Server', message=message)

    def __handle_client(self, client: socket.socket, address: Tuple[Any], callback_class: Type[protocol.Callback]):
        self.__log_event(f'Client connected: {address}')

        callback = callback_class(client)
        callback.start()

        frame_reader = FrameReader(self.max_buffer_size)

        while True:
            try:
                protocol.read(client, callback, frame_reader)

            except Exception as e:
                self.__log_event(e)
                break

        client.close()
        callback.close()
        del callback
        self.__log_event('Connection closed')

    def tunnel_ngrok(self, auth_token):
        self.__ngrok_auth_token = auth_token
        self.__ngrok_tunnel_created = True

        try:
            importlib.import_module('pyngrok')
        except ImportError:
            print('Installing pyngrok...')
            subprocess.run('pip install pyngrok'.split(' '))

        from pyngrok import ngrok

        ngrok.set_auth_token(auth_token)
        self.__log_event('Connecting to ngrok...')

        ssh_tunnel = ngrok.connect(self.__port, "tcp")
        self.__log_event(f'Ngrok proxy is running at {ssh_tunnel.public_url}')

        self.__ngrok_url = ssh_tunnel.public_url
        return self.__ngrok_url

    def __stop_ngrok_tunnel(self):
        if self.__ngrok_url:
            from pyngrok import ngrok

            ngrok.disconnect(self.__ngrok_url)
            self.__log_event('Stopping ngrok tunnel...')

        self.__ngrok_url = None

    def stop_ngrok_tunnel(self):
        self.__ngrok_tunnel_created = False
        self.__stop_ngrok_tunnel()

    def get_ngrok_url(self):
        return self.__ngrok_url

    def __serve(self):
        while True:
            client, address = self.__server.accept()

            # Create new thread for each client
            thread = threading.Thread(target=self.__handle_client, args=(client, address, self.__callback_class))
            thread.start()

    def start(self, run_background: bool = False, is_daemon: bool = False):
        self.__run_background = run_background
        self.__is_daemon = is_daemon
        self.__log_event(f'Server is running at {self.__host}:{self.__port}')

        if run_background:
            thread = threading.Thread(target=self.__serve)
            thread.daemon = is_daemon
            thread.start()
        else:
            self.__serve()


def __repr__(self):
    return self.__class__.__name__

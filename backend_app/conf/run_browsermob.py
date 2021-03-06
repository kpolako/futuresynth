from browsermobproxy import Server
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../browsermob-proxy-2.1.4/bin/browsermob-proxy')


class ProxyManager:
    __BMP = filename

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        print('start proxy server')
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": "true"})
        print('start proxy client')
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server

from browsermobproxy import Server
from selenium import webdriver
import os, time

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../virtualenvs/app/Lib/site-packages/browsermobproxy/browsermob-proxy-2.1.4/bin/browsermob-proxy')

class ProxyManager:
    __BMP = filename

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": "true"})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server


def run_selenium(url):
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("options={'captureContent': True}")
    print(client.proxy)

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    # print(client.har)
    print(json.dumps(client.har))

    server.stop()
import threading
from gevent.pywsgi import WSGIServer

import API_manager


def runFlask():
    http_server = WSGIServer(('127.0.0.1', 5000), API_manager.exportedMainApp)
    http_server.serve_forever()

def main():
    runFlask()


main()

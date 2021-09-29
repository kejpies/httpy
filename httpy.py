#!/usr/bin python3
# Copyright 2020-2021 Konrad Sekuła
from http.server import HTTPServer

from RequestHandler import RequestHandler


def run():
    print('httpy is starting...')
    server_address = ('127.0.0.1', 7001)
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        print('done!')
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()


if __name__ == '__main__':
    run()

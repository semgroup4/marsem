#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from serial import Serial
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import stream.stream as stream

stream_controller = stream.Stream()

class Car(object):

    def __init__(self, *args, **kwargs):
        self.serial = Serial(*args, **kwargs)

    def forward(self):
        self.serial.write(b'f')

    def backward(self):
        self.serial.write(b'b')

    def left(self):
        self.serial.write(b'l')

    def right(self):
        self.serial.write(b'r')


car = Car('/dev/ttyACM0', 115200)

sleep(2)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class RequestHandler(BaseHTTPRequestHandler):

    log_file = open('marsem.log', 'w')

    urls = {
        'control': r'^/$',
        'stream': r'^/stream/$'
    }

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        result = urlparse(self.path)
        path = result.path
        query = {}

        for key, value in parse_qs(result.query).items():
            if len(value) == 1:
                value = value[0]
                try:
                    value = json.loads(value)
                except ValueError:
                    pass
            query[key] = value

        for method, regex in self.urls.items():
            if re.match(regex, path):
                data = getattr(self, method)(query)
                self.wfile.write(json.dumps(data).encode())

    def control(self, query):
        action = query.get('action')
        if action:
            action = getattr(car, action, None)
            if action:
                action()

        return {}


    def stream(self, stream, query):
        param = query.get('stream')
        if param.lower() == 'true':
            stream = stream.Stream()
            stream.start()
            return {"message": "Stream started"}
        else:
            stream.stop_controller()
            stream.join()
            return {"message": "Stream ended"}  

    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))


if __name__ == '__main__':
    run(handler_class=RequestHandler)

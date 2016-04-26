#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from serial import Serial
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


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

    urls = {
        'control': r'^/$',
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


run(handler_class=RequestHandler)

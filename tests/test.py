#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import stream

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class RequestHandler(BaseHTTPRequestHandler):

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
            pass
        print("Empty response")
        return {}


    def stream(self, query):
        param = query.get('stream')
        if param.lower() == 'true':
            return {"message": "Stream started"}
        else:
            return {"message": "Stream ended"}                

    def picture_controller(self, query):
        if stream_controller.running:
            self.send_error(503, 
                            message="Camera is busy", 
                            explain="The camera is currently busy with streaming")
            return
        return picture_controller.control()
            


    

run(handler_class=RequestHandler)

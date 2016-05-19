#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import stream
import camera

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class StreamController():
    """ Controls the thread for raspivid and netcat """
    stream = None
    running = False

    def control(self, t):
        if t:
            if self.stream != None:
                if self.stream.isAlive():
                    return {"status": "stream is already running"}
                else:
                    self.stream = streams.Stream()
            else:
                self.stream = streams.Stream()
            self.stream.start()
            self.running = Truex
            return {"status": "stream started"}
        else:
            self.stream.stop()
            self.stream.join()
            self.running = False
            return {"status": "stream ended"}        

class PictureController():
    "Blocks the main thread until the camera has taken an image"

    camera = None

    def control(self):
        p = None
        with open("test.jpg", "rb") as picture:
            p = picture.read()
        return p


picture_controller = PictureController()
stream_controller = StreamController()

class RequestHandler(BaseHTTPRequestHandler):

    urls = {
        'control': r'^/$',
        'stream': r'^/stream/$',
        'picture_controller': r'^/picture/$',
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
        else:
            picture = picture_controller.control()
            self.wfile.write(picture)
            return ""

            


    

run(handler_class=RequestHandler)

#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from serial import Serial
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import stream as streams
import camera as camera

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

time.sleep(2)

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
                    return {"running": True}
                else:
                    self.stream = streams.Stream()
            else:
                self.stream = streams.Stream()
            self.stream.start()
            return {"running": True}
        else:
            self.stream.stop()
            self.stream.join()
            return {"running": False}        

class PictureController():
    "Blocks the main thread until the camera has taken an image"

    camera = None

    def control(self):
            self.camera = camera.Camera()
            return self.camera.take_picture()



stream_controller = StreamController()
picture_controller = PictureController()

class RequestHandler(BaseHTTPRequestHandler):

    log_file = open('marsem.log', 'w')
    stream = None
    protocol_version = 'HTTP/1.1'

    urls = {
        'control': r'^/$',
        'stream_controller': r'^/stream/$',
        'picture_controller': r'^/picture/$',
        'status_controller': r'^/status/$',
    }

    def do_GET(self):
        result = urlparse(self.path)
        path = result.path
        query = {}
        data = None
        t = None
        e = None
        ret = None

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
                data,t,e = getattr(self, method)(query)
                ret = data
        if e:
            self.send_error(e[0],message=e[1], explain=e[2])
            self.end_headers()
        else:
            if data and t:
                self.send_response(200)
                self.send_header('Content-Type', t)
                if t == 'application/json':
                    ret = json.dumps(data).encode()
                self.send_header('Content-Length', len(ret))
                self.end_headers()                
                self.wfile.write(ret)
                return



    def control(self, query):
        action = query.get('action')
        if action:
            action = getattr(car, action, None)
            if action:
                action()
        return ({}, 'application/json', None)


    def stream_controller(self, query):
        param = query.get('stream')
        if param.lower() == 'true':
            return (stream_controller.control(True), 'application/json', None)
        else:
            return (stream_controller.control(False), 'application/json', None)

    
    """ Takes a picture with the raspberry camera, returns a binary of the image. """
    def picture_controller(self, query):
        if stream_controller.running:
            return ({}, 'application/json', (503, "Camera is busy", "The camera is currently busy with streaming"))
        else:
            picture = picture_controller.control()
            return (picture, 'image/jpeg', None)
            
            
    def status_controller(self, query):
        statuses = {
            "stream": stream_controller.running,
            "server": True,
        }
        return (statues, 'application/json', None)
                

    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))


if __name__ == '__main__':
    run(handler_class=RequestHandler)

#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class RequestHandler(BaseHTTPRequestHandler):

    urls = {
        'index': r'^/$',
        'test1': r'^/test1$',
        'test2': r'^/test2$',
    }

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
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
                getattr(self, method)(query)

    def index(self, query):
        self.wfile.write("""
            <h1>Marsem</h1>

            <ul>
                <li><a href="/test1">Test 1</a></li>
                <li><a href="/test2">Test 2</a></li>
            </ul>

            <h2>Query</h2>
            <pre>{}</pre>
        """.format(query).encode())

    def test1(self, query):
        self.wfile.write("""
            <h1>Marsem</h1>
            <h2>Test1</h2>
        """.encode())

    def test2(self, query):
        self.wfile.write("""
            <h1>Marsem</h1>
            <h2>Test2</h2>
        """.encode())


run(handler_class=RequestHandler)

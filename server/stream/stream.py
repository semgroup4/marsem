#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, STDOUT
import threading
import time

TIMEOUT = 0.5

class Stream(threading.Thread):
    def __init__(self, options=["-t", "0", "-w", "640", "-h", "480", "-hf", "-fps", "20", "-o", "-"]):
        threading.Thread.__init__(self)
        self.raspi = ["raspivid"] + options
        self.nc = ["nc","-k","-l","2222"]
        self.running = False

    def run(self):
        raspi = Popen(self.raspi, stdout=PIPE)
        serve = Popen(self.nc, stdin=raspi.stdout)
        self.running = True
        while(self.running and (raspi.poll() and serve.poll()) is None):
            continue
        self.running = False
        serve.kill()
        raspi.kill()
        

    def stop_controller(self):
        self.running = False

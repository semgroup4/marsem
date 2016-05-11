#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, STDOUT
import threading
import time

class Stream(threading.Thread):
    def __init__(self, options=["-t", "0", "-w", "640", "-h", "480", "-vf", "-hf", "-fps", "20", "-o", "-"]):
        threading.Thread.__init__(self)
        self.raspi = ["raspivid"] + options
        self.nc = ["nc","-l","2222"]
        self.running = False

    def run(self):
        raspi = Popen(self.raspi, stdout=PIPE)
        serve = Popen(self.nc, stdin=raspi.stdout)
        self.running = True
        while(self.running):
            time.sleep(0.3)
        if serve.poll() == None : serve.kill()
        if raspi.poll() == None : raspi.kill()
        

    def stop(self):
        self.running = False

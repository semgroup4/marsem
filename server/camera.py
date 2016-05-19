from subprocess import Popen, PIPE


class Camera():
    def __init__(self, options=["-vf", "-hf", "-e", "jpg", "-q", "80", "-h", "480", "-w", "640", "-o", "-"]):
        self.camera = ["raspistill"] + options

    def take_picture(self):
        with Popen(self.camera, stdout=PIPE) as picture:
            p = picture.stdout.read()
            picture.kill()
            return p

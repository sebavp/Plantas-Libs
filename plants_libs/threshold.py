# -*- coding: utf-8 -*
from sys import argv

from PIL import Image

from timeit import timeit

class Threshold(object):
    def __init__(self, image):
        self.image = Image.open(image)

    def __del__(self):
        del self.image

    @timeit
    def process(self):
        pixels = self.image.load()
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                if pixels[x,y] >= (150,150,150):
                    pixels[x,y] = (0,0,0)
                else:
                    pixels[x,y] = (255,255,255)
        return self.image

if __name__ == '__main__':
    im = Threshold(argv[1])
    im.process()
            


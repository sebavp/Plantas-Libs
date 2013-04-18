# -*- coding: utf-8 -*
from sys import argv
from math import exp, pow

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
        beta = (0.5-0.16,0.19-0.7)
        beta0 = -0.5 * (0.25 + (0.19*0.19)-(0.16*0.16)-0.49)
        scale = 1000.0
        sat_threshold = 300
        val_threshold = 300
        hist_sat = [0]*1001
        hist_val = [0]*1001
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                
                v = float(max(pixels[x,y]))
                saturation = (float(max(pixels[x,y])-min(pixels[x,y]))/v,v/255.0)
                hist_sat[int(saturation[0]*int(scale))] +=1
                hist_val[int(saturation[1]*int(scale))] +=1
        mu1 = (float(hist_sat[:sat_threshold].index(max(hist_sat[:sat_threshold])))/scale,
            float(hist_val[val_threshold:].index(max(hist_val[val_threshold:])) + val_threshold)/scale)
        mu2 = (float(hist_sat[sat_threshold:].index(max(hist_sat[sat_threshold:]))+sat_threshold)/scale,
            float(hist_val[:val_threshold].index(max(hist_val[:val_threshold])))/scale)
        beta = (mu2[0] - mu1[0],mu2[1]-mu1[1])
        beta0 = -0.5 * (pow(mu2[0],2) + pow(mu2[1],2) - pow(mu1[0],2)-pow(mu1[1],2))
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                v = float(max(pixels[x,y]))
                saturation = (float(max(pixels[x,y])-min(pixels[x,y]))/v,v/255.0)
                pz1 = 1/(1+exp(beta0 + beta[0]*saturation[0] + beta[1]*saturation[1]))
                if pz1 > 0.5:
                    pixels[x,y] = (0,0,0)
                else:
                    pixels[x,y] = (255,255,255)
        #debugging
        #self.image.show()
        return self.image

if __name__ == '__main__':
    im = Threshold(argv[1])
    im.process()
            


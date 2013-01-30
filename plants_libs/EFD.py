# -*- coding: utf-8 -*
from math import floor, pi, cos, sin, sqrt, pow
from sys import argv

from PIL.ImageFilter import CONTOUR, SHARPEN, EDGE_ENHANCE, SMOOTH
from PIL import Image, ImageDraw
from cv2 import imread, cvtColor, threshold, findContours, COLOR_BGR2GRAY, RETR_TREE
from cv import CreateImageHeader, SetData, GetMat, IPL_DEPTH_8U, CV_CHAIN_APPROX_NONE
from numpy import asarray

from timeit import timeit


class EFD(object):
    @timeit
    def __init__(self, image, ndescriptors, scale):
        self.image = CreateImageHeader(image.size, IPL_DEPTH_8U, 3)
        SetData(self.image, image.tostring())
        self.ndescriptors = ndescriptors
        self.scale = scale
        self.m = 2*ndescriptors

    @timeit
    def get_curve(self):
        im = asarray(GetMat(self.image))
        im = cvtColor(im, COLOR_BGR2GRAY)
        # ret, im = threshold(im, 127,255, 0)
        contours, hierarchy = findContours(im, RETR_TREE, CV_CHAIN_APPROX_NONE)

        
            
        xy=[]
        # for xys in contours:
        for pos in contours[0]:
            xy.append(tuple([int(coord) for coord in pos[0]]))
        
        xy_ = []
        step = len(xy)/self.m
        for i in range(self.m):
            xy_.append(xy[i*step])
        # # Debugging
        # im_ = Image.new('RGB', (4000,3000), (255,255,255))
        # pixs = im_.load()
        # draw = ImageDraw.Draw(im_)
        # for pos in range(len(xy_)):
        #     draw.line((xy_[pos-1][0],xy_[pos-1][1]+600,xy_[pos][0],xy_[pos][1]+600), fill=128)

        # im_.show()
        # # Debugging end
        return xy_

       

    @timeit
    def fourier_coefficients(self):
        xy = self.get_curve()
        x = [c[0] for c in xy]
        y = [c[1] for c in xy]
        
        t = 2*pi/self.m
        two_over_m = 2.0/self.m
        
        ax = [two_over_m*sum([x[i]*cos((k+1)*t*i) for i in range(self.m)]) for k in range(self.ndescriptors)]
        bx = [two_over_m*sum([x[i]*sin((k+1)*t*i) for i in range(self.m)]) for k in range(self.ndescriptors)]
        ay = [two_over_m*sum([y[i]*cos((k+1)*t*i) for i in range(self.m)]) for k in range(self.ndescriptors)]
        by = [two_over_m*sum([y[i]*sin((k+1)*t*i) for i in range(self.m)]) for k in range(self.ndescriptors)]
        coeffs = [sqrt((pow(ax[k],2) + pow(ay[k],2))/(pow(ax[0],2)+pow(ay[0],2))) + sqrt((pow(bx[k],2) + pow(by[k],2))/(pow(bx[0],2)+pow(by[0],2))) for k in range(self.ndescriptors)[:-1]]
        self.coeffs = coeffs
        return coeffs, ax, ay, bx, by


    def reconstruct(self):
        coeffs, ax, ay, bx, by = self.fourier_coefficients()
        x = y = [0]*1000
        t = 2*pi/self.m
        x = [ax[0]/2.0 + sum([ax[k]*cos((k+1)*t*i) + bx[k]*sin((k+1)*t*i) for k in range(self.ndescriptors)]) for i in range(1000)]
        y = [ay[0]/2.0 + sum([ay[k]*cos((k+1)*t*i) + by[k]*sin((k+1)*t*i) for k in range(self.ndescriptors)]) for i in range(1000)]
        # for i in range(self.m):
        #     x[i] = ax[0]/2.0
        #     y[i] = ay[0]/2.0
            
        #     for k in range(len(self.coeffs))[1:]:
        #         p = t*k*i
        #         x[i] += ax[k]*cos(p) + bx[k]*sin(p)
        #         y[i] += ay[k]*cos(p) + by[k]*sin(p)
        im = Image.new('RGB',(1500,1500),(255,255,255))
        draw = ImageDraw.Draw(im)
        pixels = im.load()
        for i in range(1000)[1:]:
            xi = x[i] + 650
            yi = y[i] + 750
            draw.line((x[i-1]+650, y[i-1] + 750, xi, yi), fill=128)
        im.show()

if __name__ == '__main__':
    # im = imread(argv[1])
    from plants_libs.threshold import Threshold
    efd = EFD(Threshold(argv[1]).process(), 300, 1)
    # efd.fourier_coefficients()
    efd.reconstruct()
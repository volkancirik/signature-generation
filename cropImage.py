#!/usr/bin/env python
import numpy as np
import sys
from math import ceil
from PIL import Image

def readImage():
    output = []
    k = 1
    im = Image.open(sys.argv[1])
    fname = sys.argv[1].split('-')[0]

    w,h =  im.size
    wincrease = (w-120*4 - 3)*1.00/4
    hincrease = (h-100*4 - 3)*1.00/4

    hsize = 100
    wsize = 120
    wpoint = 1
    hpoint = 1
    range2 = np.arange(wpoint,(wincrease+wsize)*3+wpoint+1,wincrease+wsize)
    range1 = np.arange(hpoint,(hincrease+hsize)*3+hpoint+1,hincrease+hsize)

    print range1
    print range2
    for r2 in range2:
        for r1 in range1:
            r1 = int(r1)
            r2 = int(r2)
            box = (r2,r1,r2+wsize,r1+hsize)
            cropped = im.crop(box)
            cropped.save(fname+str(k)+'.sign',"JPEG")
            k = k+1
readImage()

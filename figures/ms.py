# -*- coding: utf-8 -*-

from skimage import io
from skimage import exposure
from skimage import transform
from skimage.color import rgb2gray
import os

samples = {}
fileformat = '.jpg'
keyword = "microstr"

with open("sample_codes.txt") as f:
    for line in f:
        (key, val) = line.split(',')
        samples[int(key)] = val[:-1]

for file in os.listdir(os.getcwd()):
    if file.startswith(keyword):
        image = io.imread(file)

        image = image[0:1000, 0:2048]
        image = transform.rotate(image, 180)
        gray = rgb2gray(image)

        img_adapteq = exposure.equalize_adapthist(image, clip_limit=0.03)
        img_adapteq_gray = exposure.equalize_adapthist(gray, clip_limit=0.03)

        code = int(file[9])
        newfile = keyword + '_' + samples[code] + fileformat

        io.imsave('pre_adapt_'+newfile, img_adapteq)
        io.imsave('pre_adapt_gray_'+newfile, img_adapteq_gray)

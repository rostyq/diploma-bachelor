# -*- coding: utf-8 -*-

from skimage import io
from skimage import exposure
from skimage import transform
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
        code = int(file[9])
        image = io.imread(file)
        image = transform.rotate(image, -90)
        image = image[950:1200, 900:1300]
        img_adapteq = exposure.equalize_adapthist(image, clip_limit=0.03)
        newfile = 'pr_pr_'+keyword+'_'+samples[code]+fileformat
        io.imsave(newfile, img_adapteq)


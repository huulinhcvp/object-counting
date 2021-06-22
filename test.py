#!/usr/bin/python3

# Copyright 2021 Ha Huu Linh, hahuulinh1999@gmail.com


import cv2 as cv
import numpy as np
from counter import CounterGrainsOfRice
from processing import ImageProcessing
from PIL import Image

path = 'inputs/original.png'

src_img = cv.imread(path, cv.IMREAD_GRAYSCALE) # load input images
cv.imshow("grayscale image", src_img)
kernel = np.ones((5,5),np.uint8) # kernel for morphological operators

# image processing
process = ImageProcessing(kernel, src_img)

## get result - depend on input image
src_img, out_img = process.normal_denoise()
# src_img, out_img = process.black_white_process()
# src_img, out_img = process.periodic_denoise()
# src_img, out_img = process.real_world_object_counting()

# cv.imshow("threshold image", out_img)

# counter program
counter = CounterGrainsOfRice(out_img)


# method1 - counting connected components in binary image
out1_img, num_grains_of_rice = counter.connectedComponents()
print("[ connected components ] num objects: ", num_grains_of_rice)
cv.imshow("connected components", out1_img)

# method2 - counting num of contours in binary image
out2_img, num_of_contours = counter.numOfContours(src_img)
print("[ contours ] num objects: ", num_of_contours)
cv.imshow("contours", out2_img)


# wait for key press
cv.waitKey(0)
cv.destroyAllWindows()

#!/usr/bin/python3

# Copyright 2021 Ha Huu Linh, hahuulinh1999@gmail.com


import cv2 as cv
import numpy as np

from processing import ImageProcessing
from PIL import Image

path = '../inputs/objets1.jpg'

src_img = cv.imread(path) # load input images
cv.imshow("original image", src_img)
kernel = np.ones((5,5),np.uint8) # kernel for morphological operators

# image processing
process = ImageProcessing(kernel, src_img)

## get result - depend on input image
# output_img, num_of_objects = process.normal_denoise()
# output_img, num_of_objects = process.black_white_process()
# output_img, num_of_objects = process.periodic_denoise()
output_img, num_of_objects = process.real_world_object_counting()

cv.imshow("output", output_img)


# wait for key press
cv.waitKey(0)
cv.destroyAllWindows()

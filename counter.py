import cv2 as cv
import numpy as np


class CounterGrainsOfRice:
    """
        expose 2 method for counting grains of rice
    """
    def __init__(self, binary_img):

        self.binary_img = binary_img # clean binary image
    

    def connectedComponents(self):

        """
            counts and marks number of distinct foreground objects
        """

        new_img = self.binary_img.copy() # for marks in input img

        label_count = 0 # object counters
        rows, cols = new_img.shape # height, width of image

        # loop through all pixels
        for j in range(rows):
            for i in range(cols):
                pixel = new_img[j, i]

                if 255 == pixel:
                    label_count += 1
                    cv.floodFill(new_img, None, (i, j), label_count)

        return new_img, label_count
    

    def numOfContours(self, original_img, mini_object=False):
        print(mini_object)

        """
            Computes polygonal contour boundary of foreground objects
        """

        contours, _ = cv.findContours(self.binary_img, cv.RETR_EXTERNAL,  cv.CHAIN_APPROX_SIMPLE)
        
        res = len(contours)
        
        if mini_object:
            n = res
            res_contours = []
            
            i = 0
            while i < n:
                tmp = len(contours[i])
                if tmp < 5:
                    res -= 1
                    i+=1
                    continue
                res_contours.append(contours[i])
                i += 1

            cv.drawContours(original_img, res_contours, -1, (0, 0, 255), 2)
        else:
            cv.drawContours(original_img, contours, -1, (0, 255, 0), 2)

        return original_img, res


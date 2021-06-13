import cv2 as cv
import numpy as np


class ImageProcessing:

    def __init__(self, kernel, src_img):
        self.kernel = kernel
        self.src_img = src_img

    def periodic_denoise(self):

        self.src_img = cv.morphologyEx(self.src_img, cv.MORPH_OPEN, self.kernel)

        cols = np.array([sum(self.src_img[:, i]) for i in range(self.src_img.shape[1])])
        rows = np.array([sum(self.src_img[j, :]) for j in range(self.src_img.shape[1])])

        mid_cols = max(cols)
        mid_rows = max(rows)

        j = 0
        while j < 461:

            tmp = sum(self.src_img[:, j])

            if (mid_cols > tmp):
                border = mid_cols - tmp
                inc = border // 461
                        
                self.src_img[:, j] = self.src_img[:, j] + inc

            j += 1

        i = 0
        while i < 461:

            tmp = sum(self.src_img[i, :])
            if (mid_rows > tmp):
                border = mid_rows - tmp
                inc = border // 461
                
                self.src_img[i, :] = self.src_img[i, :] + inc

            i += 1

        self.src_img = cv.medianBlur(self.src_img, 3)

        _, threshold_img = cv.threshold(self.src_img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        return self.src_img, threshold_img


    def normal_denoise(self):

        self.src_img = cv.medianBlur(self.src_img, 3)

        # local adaptive thresholding - convert source img to binary img
        # apply for original image and normal noise image
        threshold_img = cv.adaptiveThreshold (self.src_img, 255.0, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 51, -22)

        # erode image - denoise forgegrounds in binary img
        erode_img = cv.erode(threshold_img, self.kernel, iterations=1)

        return self.src_img, erode_img


    def black_white_process(self):

        # binary thresholding
        # applied for black-white image
        _, threshold_img = cv.threshold(self.src_img, 0.1, 255, cv.THRESH_BINARY)

        return self.src_img, threshold_img


    def real_world_object_counting(self):

        # gamma correction with y = 1.2
        gamma = np.array(255 * (self.src_img / 255) ** 1.2 , dtype='uint8')

        # local adaptive thresholding
        thresh = cv.adaptiveThreshold(gamma, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 255, 19)
        thresh = cv.bitwise_not(thresh)

        # dilatation + erosion
        kernel = np.ones((15,15), np.uint8)
        img_dilation = cv.dilate(thresh, kernel, iterations=1)
        img_erode = cv.erode(img_dilation,kernel, iterations=1)

        img_erode = cv.medianBlur(img_erode, 7)

        return self.src_img, img_erode







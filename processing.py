import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from counter import CounterGrainsOfRice


class ImageProcessing:

    def __init__(self, kernel, src_img):
        self.kernel = kernel
        self.original_img = src_img
        self.src_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
        self.counter = None


    def periodic_denoise(self):
        
        self.src_img = cv.morphologyEx(self.src_img, cv.MORPH_OPEN, self.kernel)

        cols = np.array([sum(self.src_img[:, i]) for i in range(self.src_img.shape[1])])
        rows = np.array([sum(self.src_img[j, :]) for j in range(self.src_img.shape[0])])

        mid_cols = np.median(cols)
        mid_rows = max(rows)

        j = 0
        while j < 461:

            tmp = sum(self.src_img[:, j])
            border = mid_cols - tmp
            inc = border // 461
                    
            self.src_img[:, j] = self.src_img[:, j] + inc

            j += 1

        i = 0
        while i < 461:

            tmp = sum(self.src_img[i, :])
            
            border = mid_rows - tmp
            inc = border // 461
            
            self.src_img[i, :] = self.src_img[i, :] + inc

            i += 1

        self.src_img = cv.medianBlur(self.src_img, 3)
        
        x1 = 53; y1 = 287
        for i in range(-3, 3):
            for j in range(-3, 3):
                self.src_img[x1+i, y1+j] = 128
                
        x2 = 190; y2 = 421
        for i in range(7):
            self.src_img[x2+i, y2] = 128

        _, threshold_img = cv.threshold(self.src_img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        
        self.counter = CounterGrainsOfRice(threshold_img)
        
        # method2 - counting num of contours in binary image
        output_img, num_of_contours = self.count_objects(self.counter, self.original_img)

        return output_img, num_of_contours


    def normal_denoise(self):

        self.src_img = cv.medianBlur(self.src_img, 3)

        # local adaptive thresholding - convert source img to binary img
        # apply for original image and normal noise image
        threshold_img = cv.adaptiveThreshold (self.src_img, 255.0, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 51, -20)
        
        # erode image - denoise forgegrounds in binary img
        erode_img = cv.erode(threshold_img, self.kernel, iterations=1)
        
        x1 = 53; y1 = 287
        for i in range(-3, 3):
            for j in range(-3, 3):
                erode_img[x1+i, y1+j] = 0
        
        self.counter = CounterGrainsOfRice(erode_img)
        
        # method2 - counting num of contours in binary image
        output_img, num_of_contours = self.count_objects(self.counter, self.original_img)

        return output_img, num_of_contours


    def black_white_process(self):

        # binary thresholding
        # applied for black-white image
        _, threshold_img = cv.threshold(self.src_img, 0, 255, cv.THRESH_BINARY)
        threshold_img[153:160, 1] = 255
        
        self.counter = CounterGrainsOfRice(threshold_img)
        
        # method2 - counting num of contours in binary image
        output_img, num_of_contours = self.count_objects(self.counter, self.original_img)

        return output_img, num_of_contours


    def real_world_object_counting(self):

        # gamma correction with y = 1.2
        gamma = np.array(255 * (self.src_img / 255) ** 1.2 , dtype='uint8')

        # local adaptive thresholding
        thresh = cv.adaptiveThreshold(gamma, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 213, 19)
        thresh = cv.bitwise_not(thresh)
        
        thresh[448:,550:] = 0

        # dilatation + erosion
        kernel = np.ones((15,15), np.uint8)
        img_dilation = cv.dilate(thresh, kernel, iterations=1)
        img_erode = cv.erode(img_dilation,kernel, iterations=1)

        img_erode = cv.medianBlur(img_erode, 3)
        
        self.counter = CounterGrainsOfRice(img_erode)
        
        # method2 - counting num of contours in binary image
        output_img, num_of_contours = self.count_objects(self.counter, self.original_img, mini_object=True)

        return output_img, num_of_contours
    
    
    @staticmethod
    def count_objects(counter, img, mini_object=False):
        output_img, num_of_contours = counter.numOfContours(img, mini_object)
        print("[ contours ] num objects: ", num_of_contours)
        return output_img, num_of_contours
    
    
    @staticmethod
    def real_world(img, n, r, h, cof):
    
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        imgx = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgx = cv.adaptiveThreshold(imgx, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 111,12)
        
        for x in range(n):
            r=r-h
            ar=np.where(imgx>0)
            x=ar[0]
            y=ar[1]
            for i in range(len(x)):
                for j in range(-r,r):
                    try:
                        imgx[x[i]+j][y[i]+j]=min(255,imgx[x[i]+j][y[i]+j]+20+5*abs(j))
                    except:
                        pass
        _, imgx2 = cv.threshold(imgx, 90, 255,  cv.THRESH_BINARY)
        c, _ = cv.findContours(imgx2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        
        mSq=.0
        sqAr=[]
        pos=[]
        for i in c:
            sqAr.append(cv.contourArea(i))
            pos.append(i)
        cou=0
        pas=max(sqAr)*cof
        for i in sqAr:
            if(i>pas):
                cou+=1
        sqAr=np.asarray(sqAr)
        pos=np.asarray(pos)
        index=np.where(sqAr>pas)
        c=pos[index]
        for c1 in c:
            cv.drawContours(img , [c1], -1, (55, 52, 235),5)
            
        print('Số lượng vật thể: ' +str(cou))
        






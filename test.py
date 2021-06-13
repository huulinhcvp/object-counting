import numpy as np
import cv2
import numpy.fft as fp
from matplotlib import pyplot as plt


img = cv2.imread("obj2.png", cv2.IMREAD_GRAYSCALE)

kernel = np.ones((5,5),np.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


# gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
cv2.imshow("morphology Ex", img)


cols = np.array([sum(img[:, i]) for i in range(img.shape[1])])
rows = np.array([sum(img[j, :]) for j in range(img.shape[1])])

# mid_cols = int(np.median(cols))
# mid_rows = int(np.median(rows))

mid_cols = max(cols)
mid_rows = max(rows)

j = 0
while j < 461:

    tmp = sum(img[:, j])

    if (mid_cols > tmp):
        border = mid_cols - tmp
        inc = border // 461
                
        img[:, j] = img[:, j] + inc

    j += 1

i = 0
while i < 461:

    tmp = sum(img[i, :])
    if (mid_rows > tmp):
        border = mid_rows - tmp
        inc = border // 461
        
        img[i, :] = img[i, :] + inc

    i += 1

img = cv2.medianBlur(img, 3)
# img = cv2.equalizeHist(img)

cv2.imshow("new img", img)
cv2.waitKey(20000)
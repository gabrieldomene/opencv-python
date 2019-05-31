import numpy as np
import cv2
import matplotlib.pyplot as plt
from random import randint
import time

def nothing(x):
    pass

st = time.time()
# img = cv2.imread('coin.jpg', 0)
cv2.namedWindow('coins')

# small = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
# # img_blur = cv2.medianBlur(img, 3)

# # Create trackbars

cv2.createTrackbar('PARAM1', 'coins', 1, 255, nothing)
cv2.createTrackbar('PARAM2', 'coins', 1, 255, nothing)
cv2.createTrackbar('Blur', 'coins', 0, 10, nothing)
# # create switch for ON/OFF functionality
# # switch = '0 : OFF \n1 : ON'
# # cv2.createTrackbar(switch, 'canny-coins',0,1,nothing)

# while(1):
#     th1 = cv2.getTrackbarPos('TH1', 'canny-coins')
#     th2 = cv2.getTrackbarPos('TH2', 'canny-coins')
#     blur = cv2.getTrackbarPos('Blur', 'canny-coins')
#     if((blur %2) == 0):
#         blur += 1
#     else:
#         pass

#     median = cv2.medianBlur(small, 5)
#     edges = cv2.Canny(median, 153, 19)
    

#     cv2.imshow('canny-coins', edges)

#     cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#     circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10)

#     # circles = np.uint16(np.around(circles))
#     # for i in circles[0,:]:
#     #     # draw the outer circle
#     #     cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
#     #     # draw the center of the circle
#     #     cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

#     cv2.imshow('detected circles',img)

#     k = cv2.waitKey(1) & 0xFF
#     if (k == 27):
#         break

# while(1):
img = cv2.imread('coins.png', 1)
img_orig = img.copy()

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



# param1 = cv2.getTrackbarPos('PARAM1', 'coins')
# param2 = cv2.getTrackbarPos('PARAM2', 'coins')
# blur = cv2.getTrackbarPos('Blur', 'coins')
# if((blur % 2) == 0):
#     blur += 1
# else:
#     pass
img = cv2.medianBlur(img, 7)

all_circ = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=200, param2=15, minRadius=40, maxRadius=70)
all_circ_rounded = np.uint16(np.around(all_circ))
print(all_circ_rounded)
count = 0
for i in all_circ_rounded[0, :]:
    cv2.circle(img_orig, (i[0], i[1]), i[2],((randint(0,255), randint(0, 255), randint(0, 255))),5)
    cv2.circle(img_orig, (i[0], i[1]), 2, (0, 0, 0), 2)
for i in all_circ_rounded[0, :]:
    cv2.putText(img_orig, 'Coin ' +str(count), (i[0] - 0, i[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    count += 1

# cv2.imshow('gray', img)

cv2.imshow('original', img_orig)
k = cv2.waitKey(1) & 0xFF
# if (k == 27):
#     break
cv2.waitKey(0)
print('{} seconds' .format(time.time() - st))
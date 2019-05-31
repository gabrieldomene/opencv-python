import cv2
import numpy as np
import random as rng

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Resize')
cv2.createTrackbar('Threshold', 'Resize', 1, 255, nothing)

cv2.createTrackbar('Blur', 'Resize', 1, 255, nothing)

while(1):
    _, frame = cap.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    th1 = cv2.getTrackbarPos('Threshold', 'Resize')
    blr1 = cv2.getTrackbarPos('Blur', 'Resize')

    if (blr1%2 == 0):
        blr1 += 1

    blur = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    retval, thresh = cv2.threshold(blur, 123, 255, 1)



    # res_thresh = cv2.resize(thresh, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    # res = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    # res_gray = cv2.resize(gray_frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    # res_blur = cv2.resize(blur,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)


    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    minperimeter = 150
    maxperimeter = 800
    nobjects = 0
    subImageList = []
    for i in range(len(contours)):
        cnt = contours[i]
        perimeter = cv2.arcLength(cnt, True)
        # print(perimeter)
        if(perimeter >= minperimeter and perimeter <= maxperimeter):
            nobjects += 1
            color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
            # Encontrar o início e fim das imagens de contorno
            x, y, w, h = cv2.boundingRect(cnt)
            # print('X={} Y={} W={} H={}'.format(x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            crop_img = frame[y:y+h, x:x+w].copy()
            # cv2.getRectSubPix(frame, cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2), x, y)
            crop_resized = cv2.resize(crop_img, (50, 50), 0, 0, cv2.INTER_NEAREST)
            cv2.drawContours(frame, [cnt], 0, color, 3)
            cv2.imshow('Resized', crop_resized)
            cv2.waitKey(100)
            subImageList.append(crop_resized)

            # print('Antes do filtro {}       Depois do filtro {}' .format(len(contours), nobjects))
    print('Number of objects=[{}]       After filtering=[{}]'.format(len(contours), len(subImageList)))


    # cv2.imshow('Gray', gray_frame)
    cv2.imshow('Thresh', thresh)
    cv2.imshow('Resize', frame)
    # cv2.imshow('Blur', blur)

    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

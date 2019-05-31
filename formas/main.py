import cv2
import numpy as np
from random import randint

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Output')

cv2.createTrackbar('Threshold', 'Output', 1, 255, nothing)
while(1):

    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # THRESHOLD RETORNA TUPLA

    th1 = cv2.getTrackbarPos('Threshold', 'Output')
    retval, thresh = cv2.threshold(gray, th1, 255, 0)

    # retval, thresh2 = cv2.threshold(gray, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    cv2.imshow('Output', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
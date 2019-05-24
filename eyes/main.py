import cv2
import numpy as np
import random as rng

def nothing(x):
    pass

cap = cv2.VideoCapture('eyes.mp4')
cv2.namedWindow('Original')

# cv2.createTrackbar('Threshold', 'Original', 1, 255, nothing)
# cv2.createTrackbar('Blur', 'Original', 1, 255, nothing)
font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):

    _, frame = cap.read()
    w, h, c = frame.shape
    new_w = int(w/2)
    new_h = int(h/2)
    
    small = cv2.resize(frame, (new_h, new_w))
    gray_frame = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    value_blur = cv2.getTrackbarPos('Blur', 'Original')
    th1 = cv2.getTrackbarPos('Threshold', 'Original')

    # print('Shape={}' .format(frame.shape))
    # print('Small shape={}' .format(small.shape))
    # print('Width={}' .format(w))
    # print('New width={}' .format(new_w))
    # print('Heigth={}' .format(h))
    # print('New height={}\n' .format(new_h))

    if (value_blur % 2 == 0):
        value_blur += 1

    blur = cv2.GaussianBlur(gray_frame, (15, 15), 0)
    retval, thresh = cv2.threshold(blur, 22, 255, 1)

    # Circulo da íris
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


     # Get the moments
    # mu = [None]*len(contours)
    # for i in range(len(contours)):
    #     area = cv2.contourArea(contours[i])
    #     mu[i] = cv2.moments(contours[i])
    #     cx = int(mu[i]['m10']/(mu[i]['m00']+1e-5))
    #     cy = int(mu[i]['m01']/(mu[i]['m00']+1e-5))
    #     if(area > 150 and cx < w*3/4):
    #         # Quadrantes 
    #         # (-, +) Direita cima
    #         # (+, +) Esquerda cima
    #         # (-, -) Direita baixo
    #         # (+, -) Equerda baixo
    #         if(cx < int(w/2) and cy > int(h/2)):
    #             # Está olhando direita baixo
    #             cv2.putText(small,'<-- Down',(cx,cy), font, 4,(255,255,255),0,cv2.LINE_AA)  
    #             # cv2.circle(small, (cx, cy), 25, (0,0,255), 1)

    #             cv2.drawContours(small, contours, -1, (0, 255, 0), 2)
    #         elif(cx < int(w/2) and cy < int(h/2)):
    #             # Está olhando direita cima
    #             cv2.putText(small,'<-- Up',(cx,cy), font, 4,(255,255,255),0,cv2.LINE_AA)  
    #             # cv2.circle(small, (cx, cy), 25, (0,255,0), 1)

    #             cv2.drawContours(small, contours, -1, (0, 255, 0), 2)
    #         elif(cx > int(w/2) and cy < int(h/2)):
    #             # Está olhando Esquerda cima
    #             cv2.putText(small,'--> Up',(cx,cy), font, 4,(255,255,255),0,cv2.LINE_AA)  
    #             # cv2.circle(small, (cx, cy), 25, (255,0,0), 1)

    #             cv2.drawContours(small, contours, -1, (0, 255, 0), 2)
    #         elif(cx > int(w/2) and cy > int(h/2)):
    #             # Está olhando direita cima
    #             cv2.putText(small,'--> Down',(cx,cy), font, 4,(255,255,255),0,cv2.LINE_AA)  
    #             # cv2.circle(small, (cx, cy), 50, (255,128,255), 1)

    #             cv2.drawContours(small, contours, -1, (0, 255, 0), 2)

    all_circ = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 50, param1=70, param2=15, minRadius=20, maxRadius=80)
    # cv2.line(small, (0, w), (0, 0), (255, 255, 255), 1)

    # cv2.line(small,(0,int(h/2)), (int(w), int(h/2)),(255,0,0),5)
    cv2.line(small, (0, int(h/8)), (int(w), int(h/8)), (255, 255, 255), 1)
    cv2.line(small, (int(new_w), 0), (int(new_w), int(h)), (255, 255, 255), 1)
    if all_circ is not None:
        circles = np.uint16(np.around(all_circ))
        
        for i in circles[0,:]:
            # print('X={}' .format(x))
            # print('Y={}' .format(y))
            # draw the outer circle
            cv2.circle(small,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(small,(i[0],i[1]),2,(0,0,255),3)

            cx, cy, r = np.uint16(np.around(all_circ[0][0]))
            print('X={}' .format(new_w))
            print('Y={}' .format(new_h))
            print('CX={}'.format(cx))
            print('CY={}\n'.format(cy))

            cv2.putText(small, str(cx)+' '+str(cy),(50, 50) ,font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(small, str(new_w)+' '+str(new_h),(50, 150) ,font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if((cx < int(new_w)) and (cy < int(new_h/4))):
                # Está olhando direita cima
                cv2.putText(small,'<-- CIMA!',(cx+70,cy+70), font, 1, (0,255,0), 2, cv2.LINE_AA)
            elif((cx > int(new_w)) and (cy < int(new_h/4))):
                # Está olhando Esquerda cima
                cv2.putText(small,'--> CIMA!',(cx+70,cy+70), font, 1, (0,255,0), 2, cv2.LINE_AA)
            elif((cx < int(new_w)) and (cy > int(new_h/4))):
                # Está olhando direita baixo
                cv2.putText(small,'<-- BAIXO!',(cx+70,cy+70), font, 1, (0,255,0), 2, cv2.LINE_AA)
            elif((cx > int(new_w)) and (cy > int(new_h/4))):
                # Está olhando esquerda baixo
                cv2.putText(small,'--> BAIXO!',(cx+70,cy+70), font, 1, (0,255, 0), 2, cv2.LINE_AA)
                
    cv2.imshow('Original', small)
    # cv2.imshow('Thresh', thresh)
    # cv2.imshow('Blur', blur)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
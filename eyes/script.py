import cv2
import numpy as np

cap = cv2.VideoCapture("eyes.mp4")

x_max = int(cap.get(3))
y_max = int(cap.get(4))

#out = cv2.VideoWriter('saida.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (x_max,y_max))

while(True):

    ExisteFrame, frame = cap.read()


    if(ExisteFrame == False):
        cap.release()
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray_frame1 = cv2.GaussianBlur(gray_frame, (35, 35), 0)
    gray_frame1 = cv2.GaussianBlur(gray_frame, (35, 35), 0)
    #[[[661.80005 231.00002  68.24   ]]]
    # detect circles in the image
    #circles = cv2.HoughCircles(gray_frame1, cv2.HOUGH_GRADIENT, 1.2, 300, param1=20, param2=62, minRadius=110, maxRadius=138)
    circles = cv2.HoughCircles(gray_frame1, cv2.HOUGH_GRADIENT, 1.2, 300, param1=20, param2=62, minRadius=110, maxRadius=138)
    print(circles)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(frame, (x, y), r, (0, 0, 255), 3)
            cv2.putText(frame, str(x)+' '+str(y)+' '+str(r),  (x-100, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                        lineType=cv2.LINE_AA)

            cv2.line(frame, (x, 0), (x, y_max), (255, 255, 255), 1)
            cv2.line(frame, (int(x_max/2), 0), (int(x_max/2), int(y_max)), (0, 255, 0), 3)
            cv2.line(frame, (int(x_max / 2) + 50, 0), (int(x_max / 2) + 50, int(y_max)), (255, 0, 0), 3)
            cv2.line(frame, (int(x_max / 2) - 50, 0), (int(x_max / 2 - 50), int(y_max)), (255, 0, 0), 3)

            if ((x > (int(x_max/2) + 50))):
                # colocar um texto na imagem
               cv2.putText(frame, "RIGHT", (x-50, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                            lineType=cv2.LINE_AA)
            elif (x < (int(x_max/2) - 50)):
                # colocar um texto na imagem
               cv2.putText(frame, "LEFT", (x-50, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                            lineType=cv2.LINE_AA)
            elif (x >= (int(x_max/2)-50) & x <= (x_max/2+50)):
                # colocar um texto na imagem
                cv2.putText(frame, "CENTER", (x-50, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                            lineType=cv2.LINE_AA)




    cv2.imshow("Original", frame)
    cv2.imshow("Original-Gray", gray_frame1)

  #  out.write(frame)

    key = cv2.waitKey(30)
    if(key == 27):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()
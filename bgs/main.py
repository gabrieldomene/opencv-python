'''BGS DETECTION'''
import cv2
import numpy as np

def nothing():
    '''Nothing'''

def compute_bgs(frames):
    '''Compute bgs model for use in subtraction'''
    # base_frames = frames
    x, y, z = frames[0].shape
    background = np.zeros((x, y, z), dtype=int)
    # print('X={}, Y={}, Z={}' .format(x, y, z))
    # Shape => height x width x qtde (480, 640, 3), 480 linhas por 640 colunas por 3 pixel rgb
    # frame = [480][640][3]

    for frame in frames:
        background = np.add(frame, background)

    return np.divide(background, len(frames)).astype(np.uint8)

def main():
    '''Main function'''

    cap = cv2.VideoCapture('video.mp4')

    # Creating windows
    # cv2.namedWindow('Background Model')
    cv2.namedWindow('Original')

    list_frames = []
    i = 0

    cv2.createTrackbar('Threshold', 'Original', 1, 255, nothing)
    # while cap.isOpened():
    while True:
        i += 1
        k = 20
        _, frame = cap.read()
        if i <= k:
            list_frames.append(frame.copy())
        else:
            # print('JA JUNTOU {} FRAMES' .format(k))
            # Caso ja tiver 20 frames, calcular o bg médio, dar pop na lista e adicionar novo frame
            # print('Calculando bg . . .')
            bg_model = compute_bgs(list_frames)
            del list_frames[0]
            # print('Removendo um frame, len=[{}]' .format(len(list_frames)))
            list_frames.append(frame.copy())
            # print('Adicionando novo frame, len=[{}]' .format(len(list_frames)))

            # Subtraction of the frame by the model
            subtract = cv2.subtract(frame, bg_model)
            subtract = cv2.cvtColor(subtract, cv2.COLOR_BGR2GRAY)
            # th1 = cv2.getTrackbarPos('Threshold', 'Original')
            _, thresh = cv2.threshold(subtract, 22, 255, 0)
            cv2.imshow('Threshold', thresh)
            # Morphological transformations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

            subtract = cv2.dilate(thresh, kernel, iterations=2)
            subtract = cv2.erode(subtract, kernel, iterations=1)

            # Find contours
            contours, _ = cv2.findContours(subtract, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            for counter, cnt in enumerate(contours, 1):
                area = cv2.contourArea(cnt)
                if area >= 500:
                    cv2.drawContours(frame, [cnt], -1, (255, 255, 0), 3)
            
            cv2.imshow('BG model', bg_model)
            cv2.imshow('Result sub', subtract)
            cv2.imshow('Original', frame)
            # Terminate program
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

    cv2.destroyAllWindows()
    cap.release()



if __name__ == "__main__":
    main()

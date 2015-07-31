#Cut the region which has a specific range of HSV value colors
#HSV color representation is currently the best to segmentate color
#Use HSV.cpp and compcv.sh to find out which range you are willing to get

import cv2
import numpy as np
import sys


argv = sys.argv[0:];
argc = len(argv);

#camera argument - char '0' is 48 in ASCII
camera = ord(argv[1])-48;

cap = cv2.VideoCapture(camera)

cam_fps = 20
cam_width = 1200
cam_heigth = 200

#frames per second (1)
cap.set(1, cam_fps)
#width - comprimento (3)
cap.set(3, cam_width);
#heigth - largura (4)
cap.set(4, cam_heigth);


# Take each frame
ret, frame = cap.read()

while(ret != None):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    # # define range of red color in HSV
    # lower_red = np.array([0, 100, 100]);
    # upper_red = np.array([10, 255, 255]);
    # # define range of yellow color in HSV
    # lower_yellow = np.array([20, 100, 100]);
    # upper_yellow = np.array([30, 255, 255]);


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # # Threshold the HSV image to get only red colors
    # mask = cv2.inRange(hsv, lower_red, upper_red)
    # # Threshold the HSV image to get only yellow colors
    # mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND (mask original image) get the region of interest
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
    # Take each frame
    ret, frame = cap.read()
cap.release()
cv2.destroyAllWindows()
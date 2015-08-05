#Cut the region which has a specific range of HSV value colors
#Regulate the trackbar to get the desired HSV values and edges results
#Then copy-paste these values into parameters

import cv2
import numpy as np
import sys

# Definitions of RED and YELLOW cases to search for
RED = 0;
YELLOW = 1;

#--------------------------------#
# Function to be used at trackbars
def nothing(x):
    pass
#--------------------------------#

#Receive and count quantity of arguments
argv = sys.argv[0:];
argc = len(argv);

#camera argument - char '0' is 48 in ASCII
camera = ord(argv[1])-48;

if (argc < 1):
    print '\nMissing arguments. Need 2 but has', argc+1;
    print 'Try "python teste.py <camera>"\n';
    quit();

color = RED;

cap = cv2.VideoCapture(camera);

cam_fps = 1;
cam_width = 400;
cam_heigth = 200;

#configure cam properties to reduce computing pixels
#frames per second (1)
cap.set(1, cam_fps)
#width - comprimento (3)
cap.set(3, cam_width);
#heigth - largura (4)
cap.set(4, cam_heigth);

# Take frame
ret, frame = cap.read();

# Calibration variables
# Paramenters used in different filters
# NOTE: After calibrating (use calibrate.py from /auxiliar)
#       to get desired values, copy-paste values here
canny_thres1 = 100;
canny_thres2 = 200;
lower_yellow_H = 25;
lower_yellow_S = 100;
lower_yellow_V = 100;
upper_yellow_H = 33;
upper_yellow_S = 255;
upper_yellow_V = 255;
lower_red_H = 0;
lower_red_S = 100;
lower_red_V = 100;
upper_red_H = 10;
upper_red_S = 255;
upper_red_V = 255;

while(ret != None):
    # Convert frame which is in RGB
    # to HSV (frame = a picture at an instant time)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

    # Process only one color at a time
    if (color == RED):
        # define range of red color in HSV. Arrays are as follow [H, S, V]
        lower_HSV = np.array([lower_red_H, lower_red_S, lower_red_V]);
        upper_HSV = np.array([upper_red_H, upper_red_S, upper_red_V]);
    elif (color == YELLOW):
        # # define range of yellow color in HSV
        lower_HSV = np.array([lower_yellow_H, lower_yellow_S, lower_yellow_V]);
        upper_HSV = np.array([upper_yellow_H, upper_yellow_S, upper_yellow_V]);

    # Threshold the HSV image to get only blue colors
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # # Threshold the HSV image to get only desired color
    mask = cv2.inRange(hsv, lower_HSV, upper_HSV)

    #Reduce noise (those small insignificant and non-sense dots)
    kernel = np.ones((3, 3), np.uint8);
    edges = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1);

    #Get the borders
    edges = cv2.Canny( edges, canny_thres1, canny_thres2);

    # Bitwise-AND (mask original image) get the region of interest
    res = cv2.bitwise_and(frame,frame, mask= mask);

    #Show on screen the results
    cv2.imshow('Original frame',frame);
    cv2.imshow('Result',res);

    k = cv2.waitKey(1) & 0xFF;
    if k == 27:     #if ESC key pressed, stop program
        break;
    elif k == 32:    #if SPACEBAR key pressed, change color
        if (color == RED):
            color = YELLOW;
        elif (color == YELLOW):
            color = RED;
    
    # Take each frame
    ret, frame = cap.read();

#Deallocate everything
cap.release();
cv2.destroyAllWindows();
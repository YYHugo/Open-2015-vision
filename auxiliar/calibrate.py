#Cut the region which has a specific range of HSV value colors
#Regulate the trackbar to get the desired HSV values and edges results
#Then copy-paste these values into parameters

import cv2
import numpy as np
import sys

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
# NOTE: After calibrating to get desired values, copy-paste values here
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

#Create trackbars in "Control" window
cv2.namedWindow('Control', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('1st Canny Threshold', 'Control', canny_thres1, 255, nothing)
cv2.createTrackbar('2nd Canny Threshold', 'Control', canny_thres2, 255, nothing)
cv2.namedWindow('Yellow Control', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('lower_yellow_H', 'Yellow Control', lower_yellow_H, 179, nothing)
cv2.createTrackbar('lower_yellow_S', 'Yellow Control', lower_yellow_S, 255, nothing)
cv2.createTrackbar('lower_yellow_V', 'Yellow Control', lower_yellow_V, 255, nothing)
cv2.createTrackbar('upper_yellow_H', 'Yellow Control', upper_yellow_H, 179, nothing)
cv2.createTrackbar('upper_yellow_S', 'Yellow Control', upper_yellow_S, 255, nothing)
cv2.createTrackbar('upper_yellow_V', 'Yellow Control', upper_yellow_V, 255, nothing)
cv2.namedWindow('Red Control', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('lower_red_H', 'Red Control', lower_red_H, 179, nothing)
cv2.createTrackbar('lower_red_S', 'Red Control', lower_red_S, 255, nothing)
cv2.createTrackbar('lower_red_V', 'Red Control', lower_red_V, 255, nothing)
cv2.createTrackbar('upper_red_H', 'Red Control', upper_red_H, 179, nothing)
cv2.createTrackbar('upper_red_S', 'Red Control', upper_red_S, 255, nothing)
cv2.createTrackbar('upper_red_V', 'Red Control', upper_red_V, 255, nothing)


while(ret != None):
    #update and print calibration constants
    canny_thres1 = cv2.getTrackbarPos('1st Canny Threshold', 'Control')
    canny_thres2 = cv2.getTrackbarPos('2nd Canny Threshold', 'Control')
    lower_yellow_H = cv2.getTrackbarPos('lower_yellow_H', 'Yellow Control')
    lower_yellow_S = cv2.getTrackbarPos('lower_yellow_S', 'Yellow Control')
    lower_yellow_V = cv2.getTrackbarPos('lower_yellow_V', 'Yellow Control')
    upper_yellow_H = cv2.getTrackbarPos('upper_yellow_H', 'Yellow Control')
    upper_yellow_S = cv2.getTrackbarPos('upper_yellow_S', 'Yellow Control')
    upper_yellow_V = cv2.getTrackbarPos('upper_yellow_V', 'Yellow Control')
    lower_red_H = cv2.getTrackbarPos('lower_red_H', 'Red Control')
    lower_red_S = cv2.getTrackbarPos('lower_red_S', 'Red Control')
    lower_red_V = cv2.getTrackbarPos('lower_red_V', 'Red Control')
    upper_red_H = cv2.getTrackbarPos('upper_red_H', 'Red Control')
    upper_red_S = cv2.getTrackbarPos('upper_red_S', 'Red Control')
    upper_red_V = cv2.getTrackbarPos('upper_red_V', 'Red Control')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
  
    # define range of blue color in HSV. Arrays are as follow [H, S, V]
    #lower_blue = np.array([110,50,50]);
    #upper_blue = np.array([130,255,255]);
    # # define range of red color in HSV
    lower_red = np.array([lower_red_H, lower_red_S, lower_red_V]);
    upper_red = np.array([upper_red_H, upper_red_S, upper_red_V]);
    # # define range of yellow color in HSV
    lower_yellow = np.array([lower_yellow_H, lower_yellow_S, lower_yellow_V]);
    upper_yellow = np.array([upper_yellow_H, upper_yellow_S, upper_yellow_V]);

    # Threshold the HSV image to get only blue colors
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # # Threshold the HSV image to get only red colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # # Threshold the HSV image to get only yellow colors
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow);

    #Reduce noise (those small insignificant and non-sense dots)
    kernel = np.ones((3, 3), np.uint8);
    edges_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel, iterations=1);
    edges_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel, iterations=1);

    #Get the borders
    edges_yellow = cv2.Canny( edges_yellow, canny_thres1, canny_thres2);
    edges_red = cv2.Canny( edges_red, canny_thres1, canny_thres2);
    
    #Show on screen the results of each process
    cv2.imshow('Original frame',frame);
    cv2.imshow('res_red',res_red);
    cv2.imshow('res_yellow',res_yellow);

    k = cv2.waitKey(1) & 0xFF;
    if k == 27:
        break;
    
    # Take each frame
    ret, frame = cap.read();

#Deallocate everything
cap.release();
cv2.destroyAllWindows();
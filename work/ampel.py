import numpy as np
import cv2

cap = cv2.VideoCapture(0) # Input 0

def checkgreen():
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([45,200,200])
    upper_green = np.array([80,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    no_green = cv2.countNonZero(mask)
    return no_green

    while True:
        checkgreen()
        no_green = checkgreen()
        print('Grüne Pixel: ' + str(no_green))
        
        if no_green > 500:
            go = 1
            break
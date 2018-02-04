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

def checkblue():
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([129,200,200])
    upper_blue = np.array([96,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    no_blue = cv2.countNonZero(mask)
    return no_blue

cap = cv2.VideoCapture(0)
no_blue = 0

while no_blue < 500:
    no_blue = checkblue()
    
aufraeumen()
print("Rennen beendet!")
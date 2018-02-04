import numpy as np
import cv2
cap = cv2.VideoCapture(0) # Input 0

def onenter():
    input("Foto aufnehmen?")

    ret, img = cap.read()
    cv2.imwrite("test.png",img)
    
onenter()
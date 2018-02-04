import numpy as np
import cv2
import os

test = os.listdir()

for item in test:
    if item.endswith(".jpg"):
        os.remove(os.path.join(item))

cap = cv2.VideoCapture(0) # Input 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

input("Foto aufnehmen?")

def onenter():
    i=10
    while i < 200:
        ret, img = cap.read()
        #cv2.imwrite("test"+str(i)+".jpg",img)
        i+=1
        if ret==True:    
            out.write(img)

    print("Fotos aufgenommen")
    cap.release()
    out.release()
    
onenter()
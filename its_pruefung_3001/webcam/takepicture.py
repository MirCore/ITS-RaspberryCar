import numpy as np
import cv2
cap = cv2.VideoCapture(0) # Input 0

cap.set(3, 320.) # Auflösung verändern
cap.set(4, 240.) # Auflösung verändern

input("Foto aufnehmen?")

ret, img = cap.read()
cv2.imwrite("test.png",img)
print(img.size)
print(img.dtype)

del(cap)

img = cv2.imread("test.png")

height = np.size(img, 0)
width = np.size(img, 1)

print("Spalten: ", width)
print("Zeilen:", height)

px = img[100,100]
print(px)

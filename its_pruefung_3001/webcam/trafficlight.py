import cv2             # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
np.set_printoptions(threshold=5, precision=2) # Dies ist nur für dieses Handson wichtig (Anzeige von langen Zahlenkolonnen)

import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern

cap = cv2.VideoCapture(0) # Input 0

def detection():
    ret, img = cap.read()
    return img

img = detection()
width = np.size(img, 1)
print("Spalten:", width)

print("Dimensionen von img: (Höhe, Breite, Farbkanäle)", img.shape)
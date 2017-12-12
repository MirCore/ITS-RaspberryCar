import cv2             #Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     #Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
np.set_printoptions(threshold=5, precision=2) #Dies ist nur für dieses Handson wichtig (Anzeige von langen Zahlenkolonnen)

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

def line(img):
    img_rgb = img[:, :, ::-1] #Umdrehen der Farbkanäle
    img_red = img[:,:,2]  #Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[:,:,1]
    img_blue = img[:,:,0]

    zeile400 = img_red[400, :]
    img_redness = img_red.astype('int16') - (img_green/2+img_blue/2)

    #Schnappen wir uns also mal wieder die Linie in Zeile 400
    zeile400 = img_redness[400, :]

    #Dann wenden wir einen Schwellwert an:
    zeile400_bin = zeile400>60

    #Das Gleiche kann man auch kürzer ausdrücken:
    x = np.arange( zeile400_bin.shape[0] ) #x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
    if zeile400_bin.sum() != 0:
        mittelpunkt = (zeile400_bin*x).sum() / zeile400_bin.sum()
    else:
        mittelpunkt = None
    return mittelpunkt

try:
    while True:
        img = detection()
        mittelpunkt = line(img)
        if mittelpunkt is None:
            mittelpunkt = 999
        rounded = round(mittelpunkt, 1)
        print("Linienmittelpunkt:", rounded," " * int(0.2 * mittelpunkt), "█")
        
except KeyboardInterrupt:
    print("Stopp")
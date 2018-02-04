import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern

from gpiosetup import * 
from aufraeumen import *

import cv2             #Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     #Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
#np.set_printoptions(threshold=5, precision=2) #Dies ist nur für dieses Handson wichtig (Anzeige von langen Zahlenkolonnen)

cap = cv2.VideoCapture(0) # Input 0

def detection():
    ret, img = cap.read() # ret ist ein Bool-Wert. Wird das Bild korrekt eingelesen, ist der Wert TRUE.
    return img

img = detection()
width = np.size(img, 1)
ideal = width/2
print("Spalten:", width)

def linienmitte(img):
    img_rgb = img[:, :, ::-1] #Umdrehen der Farbkanäle
    img_red = img[:,:,2]  #Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[:,:,1]
    img_blue = img[:,:,0]

    img_redness = img_red.astype('int16') - (img_green/2+img_blue/2)
    
    zeile400 = img_redness[400, :]

    zeile400_bin = zeile400>60   # Schwellwert: 60

    x = np.arange( zeile400_bin.shape[0] ) #x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
    if zeile400_bin.sum() != 0:
        mittelpunkt = (zeile400_bin*x).sum() / zeile400_bin.sum()
    else:
        mittelpunkt = None
    return mittelpunkt


######### Auto fahren
value =''
speed = 50

def forward():
    pl.ChangeDutyCycle(speed)
    pr.ChangeDutyCycle(speed)

def links(value):
    pl.ChangeDutyCycle(value*speed)
    pr.ChangeDutyCycle(((1-value)+1)*speed)
    
def rechts(value):
    pl.ChangeDutyCycle(((1-value)+1)*speed)
    pr.ChangeDutyCycle(value*speed)

#######

# Taster:
def main():
    print ("Taster drücken")
    while GPIO.input(GPIO_TASTER) == 1:
        time.sleep(.1)
    print("Start in 3 Sekunden", end="\r")
    time.sleep(3) 
    losfahren()
    pr.start(speed)            # Motor A, speed% Tastverhältnis
    pl.start(speed)            # Motor B, speed% Tastverhältnis


main()    
mittelpunkt = 0

try:
    while True:
        img = detection()
<<<<<<< HEAD
        lastX = mittelpunkt
        mittelpunkt = line(img)
=======
        lastX = x
        x = linienmitte(img)
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44
        
        if mittelpunkt is None:
            mittelpunkt = lastX
            
        rounded = round(mittelpunkt, 1)
        
        if mittelpunkt == ideal:
            forward()
        if mittelpunkt < ideal:
            value = (mittelpunkt / ideal) ** 2
            links(value)
<<<<<<< HEAD
        elif mittelpunkt > ideal:
            value = (ideal / mittelpunkt) ** 2
=======
        elif x > ideal:
            value = ((640-x)/ideal)**2
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44
            rechts(value)
        print("Linienmittelpunkt:", rounded, value, " " * int(0.2 * mittelpunkt), "█")
        
except KeyboardInterrupt:
    print("Stopp")
    aufraeumen()

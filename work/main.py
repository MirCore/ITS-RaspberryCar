import threading  # Modul threads
import cv2  # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np  # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
import math
import time  # Modul time
import statistics
import os

from aufraeumen import aufraeumen, losfahren, bremsen  # Funktion für cleanup() importieren
from setup import *  # GPIO Setup importieren und ausführen
from abstand import distanz  # Funktion für Wandabstand messen importieren

speed = 100  # 1 bis 4 (*25% Tastverhältnis)
linie_found = True

cap = cv2.VideoCapture(0)  # Input 0

# Schauen, ob Ampel grün ist
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

def line(zeileNr1):
    ret, img = cap.read()

    img_red = img[zeileNr1, :, 2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[zeileNr1, :, 1]
    img_blue = img[zeileNr1, :, 0]

    zeile_bin = (img_red.astype('int16') - (img_green / 2 + img_blue / 2)) > 60

    # Mittelpunkt berechnen:
    if zeile_bin.sum() != 0:
        x = np.arange(zeile_bin.shape[0])  # x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
        return (zeile_bin * x).sum() / zeile_bin.sum()
    else:
        return None

def lenken(steer):
    if steer > 2:
        steer = 2
    if steer < 0:
        steer = 0
        
    speedHead = (100 - speed)
        
    if steer == 1:
        pr.ChangeDutyCycle(speed)  #
        pl.ChangeDutyCycle(speed)  #
    elif steer < 1:
        pr.ChangeDutyCycle((((1 - steer) * speedHead + speed))*.75)  #
        pl.ChangeDutyCycle(steer * speed)  #
    elif steer > 1:
        steer = 2 - steer
        pr.ChangeDutyCycle((steer * speed)*.75)  #
        pl.ChangeDutyCycle(((1 - steer) * speedHead + speed))  #
    return

def linienfahren(delay, run_event):
    global speed
    global cap
    global linie_found

    ret, img = cap.read()
    width = np.size(img, 1)
    ideal = width / 2
    mitte = ideal
    steer = 1
    i = 1
    linie_found_counter = 0

    while run_event.is_set():
        if mitte is not None:
            last_mitte = mitte
        mitte = line(100)
        i+=1
        
        if mitte is None and linie_found is True:
            array = [distanz("L") for i in range(10)]
            sensor = statistics.median(array)
            #print(sensor, array)
            if 19 < sensor < 35:
                linie_found_counter -= 1
            print("Linie verloren: ", linie_found_counter)
        elif mitte is not None:
            linie_found_counter += 1
            print("Linie gefunden: ", linie_found_counter)
        if linie_found_counter > 5:
            linie_found = True
            linie_found_counter = 5
        elif linie_found_counter < 0:
            linie_found = False
            linie_found_counter = 0
        
        if linie_found is True: 
            if mitte is None:
                speed = 50
                if last_mitte > ideal:
                    mitte = 640
                else:
                    mitte = 0
            elif width/4 < mitte < width/4*3:
                speed = 100
            else:
                speed = 75

            if mitte == ideal:
                steer = 1
            elif mitte < ideal:
                steer = (mitte/ideal)*.7+.3
            elif mitte > ideal:
                steer = 2-(((width-mitte)/ideal)*.9+.1)

            lenken(steer)
            print(" " * int(mitte/10), "█", " " * int(30 - mitte/10), "x = %.1f cm" % mitte, ";ideal = %.1f" % ideal, ";steer = %.1f" % steer, ";i = ", i)
            print(" " * int(ideal/10), "|")
        else:
            time.sleep(.1)

        time.sleep(delay)
        
def wandfahren(delay, run_event):
    global speed
    global linie_found

    zielDist = 21
    dist = distanz("L")
    steer = 1
    angle = 0
    print("Distanz: ", dist)

    while run_event.is_set():
        if linie_found == False:
            speed = 100
            lastAngle = angle
            lastDist = dist
            lastSteer = steer
            array = [distanz("L") for i in range(10)]
            dist = statistics.median(array)
            #print(dist,array)

            zielAngle = math.degrees(-math.atan((zielDist - dist) / 50))  # Winkel zum ziel-Abstand
            angle = math.degrees(math.atan((lastDist - dist) / 10))  # Vermutlicher Winkel des Autos zur Wand

            if zielAngle == angle:
                steer = 1
            elif angle < zielAngle:
                steer = (((angle + 90) / (zielAngle + 90)) ** 4)
            elif angle > zielAngle:
                steer = 2 - ((((zielAngle + 90) / (angle + 90)) ** 8))

            steer = (lastSteer + steer) / 2
        
            lenken(steer)
            print(" " * int(dist), "█", " " * int(70 - dist), "d = %.1f cm" % dist, ";s = %.2f" % steer)
            print(" " * zielDist, "|")

        time.sleep(delay)

def main():
    global speed 
    
    cap = cv2.VideoCapture(0) # Input 0
    no_green = 0
    print("Warte auf Ampel")
    
    while no_green < 500:
        no_green = checkgreen()        
    
    losfahren()
    pr.start(0)  # Motor A, speed% Tastverhältnis
    pl.start(0)  # Motor B, speed% Tastverhältnis

    run_event = threading.Event()
    run_event.set()

    th1_delay = .01   # sleep dauer der Funktion
    th2_delay = .01  # sleep dauer der Funktion
    th1 = threading.Thread(target=linienfahren, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    th2 = threading.Thread(target=wandfahren, args=(th2_delay, run_event))  # Funktion in einem neuen Thread zuordnen

    th1.start()  # Thread starten
    th2.start()  # Thread starten

    # Warten bis Strg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        print("attempting to close threads. Max wait =", max(th1_delay, th2_delay))  #
        bremsen()
        run_event.clear()
        th1.join()
        print("th1 closed")
        th2.join()
        print("th2 closed")
        aufraeumen()
        print("threads successfully closed")
        
        cap.release()
        
if __name__ == '__main__':
    main()
import threading  # Modul threads
import cv2  # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np  # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
import math
import time  # Modul time
import statistics
import os

from aufraeumen import aufraeumen, losfahren  # Funktion für cleanup() importieren
from setup import *  # GPIO Setup importieren und ausführen
from abstand import distanz  # Funktion für Wandabstand messen importieren

speed = 2  # 1 bis 4 (*25% Tastverhältnis)
line_found = False
line_steer = 1
i=1

test = os.listdir()
for item in test:
    if item.endswith(".jpg"):
        os.remove(os.path.join(item))

np.set_printoptions(threshold=5, precision=2)  # Anzeige von langen Zahlenkolonnen

cap = cv2.VideoCapture(0)  # Input 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

def line(zeileNr1):
    global i
    ret, img = cap.read()
    
    if ret==True:
        out.write(img)

    i+=1

    img_red = img[zeileNr1, :, 2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[zeileNr1, :, 1]
    img_blue = img[zeileNr1, :, 0]

    zeile_bin = (img_red.astype('int16') - (img_green / 2 + img_blue / 2)) > 60

    # Mittelpunkt berechnen:
    if zeile_bin.sum() != 0:
        x = np.arange(zeile_bin.shape[0])  # x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
        mittelpunkt1 = (zeile_bin * x).sum() / zeile_bin.sum()
    else:
        mittelpunkt1 = None
    
    return mittelpunkt1

def lenken(steer):
    speedHead = (100 - speed * 25) / 25
    speedHead = 2
    if steer == 1:
        pr.ChangeDutyCycle(speed * 25)  #
        pl.ChangeDutyCycle(speed * 25)  #
    elif steer < 1:
        pr.ChangeDutyCycle(((1 - steer) * speedHead + speed) * 25)  #
        pl.ChangeDutyCycle(steer * speed * 25)  #
    elif steer > 1:
        steer = 2 - steer
        pr.ChangeDutyCycle(steer * speed * 25)  #
        pl.ChangeDutyCycle(((1 - steer) * speedHead + speed) * 25)  #
    return


def sensor(delay, run_event):
    global line_steer
    global line_found
    global speed
    global cap

    ret, img = cap.read()
    width = np.size(img, 1)
    ideal = width / 2
    mitte = ideal
    line_found = True
    steer = 1

    while run_event.is_set():
        last_mitte = mitte
        mitte = line(100)

        if mitte is None:
            speed = 1.5
            if last_mitte > ideal:
                mitte = 640
            else:
                mitte = 0
        else:
            speed = 2
                
        if mitte == ideal:
            steer = 1
        elif mitte < ideal:
            steer = (math.sqrt(mitte/ideal)**3)*.7+.3
        elif mitte > ideal:
            steer = 2-((math.sqrt((640-mitte)/ideal)**3)*.7+.3)
        
        if steer > 2:
            steer = 2
        if steer < 0:
            steer = 0

        lenken(steer)

        print(" " * int(mitte/4), "█", " " * int(70 - mitte/4), "x = %.1f cm" % mitte, ";ideal = %.1f" % ideal, ";steer = %.1f" % steer, ";i = ", i)
        print(" " * int(ideal/4), "|")


def main():
    global speed
    
    time.sleep(1)

    losfahren()
    pr.start(speed)  # Motor A, speed% Tastverhältnis
    pl.start(speed)  # Motor B, speed% Tastverhältnis

    run_event = threading.Event()
    run_event.set()

    th1_delay = .04  # sleep dauer der Funktion
    th2_delay = .001  # sleep dauer der Funktion
    th3_delay = .02  # sleep dauer der Funktion
    th1 = threading.Thread(target=sensor, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    #th2 = threading.Thread(target=linienfahren, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen

    th1.start()  # Thread starten
    #th2.start()  # Thread starten

    # Warten bis Strg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        print("attempting to close threads. Max wait =", max(th1_delay, th2_delay, th3_delay))  #
        run_event.clear()
        th1.join()
        #th2.join()
        aufraeumen()
        print("threads successfully closed")
        
        cap.release()
        out.release()

if __name__ == '__main__':
    main()

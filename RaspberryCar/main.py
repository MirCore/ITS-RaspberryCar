import threading  # Modul threads
import cv2  # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np  # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
import math
import time  # Modul time
import statistics
<<<<<<< HEAD
=======
import os
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44

from aufraeumen import aufraeumen, losfahren  # Funktion für cleanup() importieren
from setup import *  # GPIO Setup importieren und ausführen
from abstand import distanz  # Funktion für Wandabstand messen importieren

<<<<<<< HEAD
global speed
global line_found
global wall_found
global line_steer
global wall_steer
speed = 2  # 1 bis 4 (*25% Tastverhältnis)
line_found = False
wall_found = False
line_steer = 1
wall_steer = 1
=======
speed = 2  # 1 bis 4 (*25% Tastverhältnis)
line_found = False
line_steer = 1
i=1

test = os.listdir()
for item in test:
    if item.endswith(".jpg"):
        os.remove(os.path.join(item))
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44

np.set_printoptions(threshold=5, precision=2)  # Anzeige von langen Zahlenkolonnen

cap = cv2.VideoCapture(0)  # Input 0

<<<<<<< HEAD

def line(zeileNr1, zeileNr2):
    ret, img = cap.read()

    img_rgb = img[:, :, ::-1]  # Umdrehen der Farbkanäle
    img_red = img[:, :, 2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[:, :, 1]
    img_blue = img[:, :, 0]

    img_redness = img_red.astype('int16') - (img_green / 2 + img_blue / 2)

    # ZeileNr herausnehmen:
    zeile = img_redness[zeileNr1, :]

    # Dann wenden wir einen Schwellwert an:
    zeile_bin = zeile > 60

    # Mittelpunkt berechnen:
    x = np.arange(zeile_bin.shape[0])  # x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
    if zeile_bin.sum() != 0:
        mittelpunkt1 = (zeile_bin * x).sum() / zeile_bin.sum()
    else:
        mittelpunkt1 = None

    return mittelpunkt1, 0


def linienfahren(delay, run_event):
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
        mitte, mitte2 = line(100, 479)

        if mitte is None:
            if last_mitte > ideal:
                mitte = 640
            else:
                mitte = 0
            # steer = 0
        # if mitte is None and last_line_found is False:
        #    mitte = ideal
        #    line_found = False
        # else:
        #    zielAngle = math.degrees(-math.atan((ideal - mitte) / 200))  # Winkel zum ziel-Abstand
        #    angle = math.degrees(math.atan((last_mitte - mitte) / 50))  # Vermutlicher Winkel des Autos zur Wand

        #    if zielAngle == angle:
        #        steer = 1
        #    elif angle < zielAngle:
        #        steer = 2 - (((angle + 90) / (zielAngle + 90)))
        #    elif angle > zielAngle:
        #        steer = ((zielAngle + 90) / (angle + 90))

        if mitte == ideal:
            forward()
        elif mitte < ideal:
            steer = (mitte / ideal) ** 2
        elif mitte < ideal - 70:
            steer = (mitte / ideal) ** 3
        elif mitte > ideal:
            steer = 2 - (ideal / mitte) ** 2
        elif mitte > ideal + 70:
            steer = 2 - (ideal / mitte) ** 3

        if steer > 2:
            steer = 2
        if steer < 0:
            steer = 0

        line_steer = steer

        # print(" " * int(mitte/4), "█", " " * int(70 - mitte/4), "x = %.1f cm" % mitte, ";ideal = %.1f" % ideal, ";a = %.1f°" % angle,";z = %.1f°" % zielAngle)
        # print(" " * int(ideal/4), "|")

        time.sleep(delay)
=======
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

def line(zeileNr1):
    global i
    ret, img = cap.read()
    
    if ret==True:
        out.write(img)

    i+=1
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44

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
<<<<<<< HEAD
    speedHead = 1
=======
    speedHead = 2
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44
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
<<<<<<< HEAD
    global line_found
    global wall_found
    global line_steer
    global wall_steer
    steer = 1

    while run_event.is_set():

        steer = line_steer
        print("linesteer", steer)
=======
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
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44

        lenken(steer)

        print(" " * int(mitte/4), "█", " " * int(70 - mitte/4), "x = %.1f cm" % mitte, ";ideal = %.1f" % ideal, ";steer = %.1f" % steer, ";i = ", i)
        print(" " * int(ideal/4), "|")


def main():
    global speed
<<<<<<< HEAD
    # print ("Taster drücken")
    # while GPIO.input(GPIO_TASTER) == 1:
    #    time.sleep(.1)
    # print("Start in 1 Sekunde", end="\r")
=======
    
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44
    time.sleep(1)

    losfahren()
    pr.start(speed)  # Motor A, speed% Tastverhältnis
    pl.start(speed)  # Motor B, speed% Tastverhältnis

    run_event = threading.Event()
    run_event.set()

    th1_delay = .04  # sleep dauer der Funktion
    th2_delay = .001  # sleep dauer der Funktion
<<<<<<< HEAD
    th1 = threading.Thread(target=sensor, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    th2 = threading.Thread(target=linienfahren, args=(th2_delay, run_event))  # Funktion in einem neuen Thread zuordnen

    th1.start()  # Thread starten
    th2.start()  # Thread starten
=======
    th3_delay = .02  # sleep dauer der Funktion
    th1 = threading.Thread(target=sensor, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    #th2 = threading.Thread(target=linienfahren, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen

    th1.start()  # Thread starten
    #th2.start()  # Thread starten
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44

    # Warten bis Strg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        print("attempting to close threads. Max wait =", max(th1_delay, th2_delay, th3_delay))  #
        run_event.clear()
        th1.join()
<<<<<<< HEAD
        th2.join()
=======
        #th2.join()
>>>>>>> 88df7ba3bdb13469002e3b8c1bab3bc14098cb44
        aufraeumen()
        print("threads successfully closed")
        
        cap.release()
        out.release()

if __name__ == '__main__':
    main()

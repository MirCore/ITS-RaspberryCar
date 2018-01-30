import threading  # Modul threads
import cv2  # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np  # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
import math
import time  # Modul time

from aufraeumen import aufraeumen, losfahren, bremsen  # Funktion für cleanup() importieren
from setup import *  # GPIO Setup importieren und ausführen

cap = cv2.VideoCapture(0)  # Input 0
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 15, (640,480))
ret, img = cap.read()

# Video erstellen
def makevideo(delay, run_event):
    global img, ret, out
    global x, minutes, seconds
    
    minutes = 0
    seconds = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    x = 320
    capture_video = True
    
    while run_event.is_set():
        if ret==True and capture_video == True:
            cv2.line(img,(int(x)-1,70),(int(x)+1,70),(255,0,0),5)
            cv2.putText(img,'{:0>2}:{:05.2f}'.format(int(minutes),seconds),(10,470), font, 2,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(img,"%.0f" % x,(int(x)-30,100), font, 1,(255,255,255),2,cv2.LINE_AA)
            out.write(img)  
            time.sleep(delay)

# Schauen, ob Ampel grün ist
def checkgreen():
    global img, ret
    
    # Take each frame
    ret, img = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([45,200,200])
    upper_green = np.array([80,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    no_green = cv2.countNonZero(mask)
    return no_green

# Schauen, ob Ampel blau ist
def checkblue(delay, run_event):
    global img, ret 
    time.sleep(1)
    
    while run_event.is_set():
        # Convert BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90,100,255])
        upper_blue = np.array([100,255,255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        no_blue = cv2.countNonZero(mask)
        if no_blue > 500:
            print("Blaue Ampel, warte 1,5 sekunden...")
            time.sleep(1.5)
            bremsen()
            print("STOP!!! Rennen fertig")
            run_event.clear()
            
        time.sleep(delay)

# Motoren lenken
def lenken(steer, speed):    
    if steer > 2:
        steer = 2
    elif steer < 0:
        steer = 0
    if speed > 100:
        speed = 100
    elif speed < 0:
        speed = 0
        
    speedHead = (100 - speed)
    
    if speedHead > speed:
        speedHead = speed
        
    if steer == 1:
        pr.ChangeDutyCycle(speed)  #
        pl.ChangeDutyCycle(speed)  #
    elif steer < 1:
        pr.ChangeDutyCycle(((1 - steer) * speedHead + speed))  #
        pl.ChangeDutyCycle(steer * speed)  #
    elif steer > 1:
        steer = 2 - steer
        pr.ChangeDutyCycle((steer * speed))  #
        pl.ChangeDutyCycle(((1 - steer) * speedHead + speed))  #
    return

# Bild machen und auslesen
def line(zeileNr):
    global img, ret
    ret, img = cap.read()

    img_red = img[zeileNr, :, 2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[zeileNr, :, 1]
    img_blue = img[zeileNr, :, 0]

    zeile_bin = (img_red.astype('int16') - (img_green / 2 + img_blue / 2)) > 60

    # Mittelpunkt berechnen:
    if zeile_bin.sum() != 0:
        x = np.arange(zeile_bin.shape[0])  # x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
        return (zeile_bin * x).sum() / zeile_bin.sum()
    else:
        return None

# Linie analysieren
def linienfahren(delay, run_event):
    global cap
    global x, minutes, seconds

    ret, img = cap.read()
    width = np.size(img, 1)
    ideal = width/2
    mitte = ideal
    last_mitte = mitte
    steer = 1
    startzeit = time.time()

    while run_event.is_set():
        last_mitte = mitte
        mitte = line(70)
        
        if mitte is None:
            if last_mitte > ideal:
                mitte = 640
            else:
                mitte = 0
        x = mitte
        
        if mitte == ideal:
            steer = 1
        elif mitte < ideal:
            steer = (mitte/ideal)
            speed = steer*60+40
            steer = steer*.9+.1
        elif mitte > ideal:
            steer = (width-mitte)/ideal
            speed = steer*60+40
            steer = 2-(steer*.9+.1)

        lenken(steer, speed)
        
        hours, rem = divmod(time.time()-startzeit, 3600)
        minutes, seconds = divmod(rem, 60)

        print(" " * int(mitte/10), "█", " " * int(64 - mitte/10), "x = %.1f" % mitte, ";steer = %.1f" % steer, ";speed = %.1f" % speed, ";time = {:0>2}:{:05.2f}".format(int(minutes),seconds))
        print(" " * int(ideal/10), "|")

        time.sleep(delay)

# Programm starten
def main():
    global speed        
    
    losfahren()
    pr.start(0)  # Motor A, speed% Tastverhältnis
    pl.start(0)  # Motor B, speed% Tastverhältnis

    run_event = threading.Event()
    run_event.set()

    th1_delay = .01   # sleep dauer der Funktion
    th2_delay = .01   # sleep dauer der Funktion
    th3_delay = .001  # sleep dauer der Funktion
    th1 = threading.Thread(target=linienfahren, args=(th1_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    th2 = threading.Thread(target=checkblue, args=(th2_delay, run_event))  # Funktion in einem neuen Thread zuordnen
    th3 = threading.Thread(target=makevideo, args=(th3_delay, run_event))  # Funktion in einem neuen Thread zuordnen

    th3.start()  # Thread starten
    
    no_green = 0
    print("Warten auf grüne Ampel")
    
    while no_green < 500:
        no_green = checkgreen()
    
    th1.start()  # Thread starten
    th2.start()  # Thread starten
        
    # Warten bis Strg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        print("attempting to close threads. Max wait =", max(th1_delay, th2_delay, th3_delay))  #
        bremsen()
        run_event.clear()
        th1.join()
        print("Thread 1 closed")
        th2.join()
        print("Thread 2 closed")
        th3.join()
        print("Thread 3 closed")
        aufraeumen()
        print("Threads successfully closed")
        
        cap.release()
        out.release()
        
if __name__ == '__main__':
    main()
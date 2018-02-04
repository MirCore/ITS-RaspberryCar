import threading            # Modul threads
import time                 # Modul time
import math
import statistics
from setup import *           # GPIO Setup importieren und ausführen
from abstand import distanz       # Funktion für Wandabstandmessen importieren
from aufraeumen import aufraeumen,bremsen,losfahren # Funktion für cleanup() importieren

speed = 3      # 1 bis 4 (*25) (% Tastverhältnis)

#
def forward():
    pr.ChangeDutyCycle(speed*25)  # Motor A, 100% Tastverhältnis
    pl.ChangeDutyCycle(speed*25)  # Motor B, 100% Tastverhältnis
    return
#    
def lenken(steer):
    speedHead = (100-speed*25)/25
    if steer < 1:
        pr.ChangeDutyCycle(((1-steer)*speedHead+speed)*25)   # 
        pl.ChangeDutyCycle(steer*speed*25)  # 
    elif steer > 1:
        steer = 2-steer
        pr.ChangeDutyCycle(steer*speed*25)   # 
        pl.ChangeDutyCycle(((1-steer)*speedHead+speed)*25)  # 
    return

def wandfahren(delay, run_event):
    zielAngle = 0
    angle = 0
    zielDist = 30
    steer = 0
    dist = distanz("L")
    lastDist = dist
    vorne = 40 #distanz("R")
    lastVorne = vorne
    lastSteer = 1
    
    print ("Distanz: ", dist)
    
    while run_event.is_set():
        time.sleep(delay)
        
        lastDist = dist
        dist = statistics.median([distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L")])
        lastVorne = vorne
        vorne = 40 #distanz("R")
        lastSteer = steer

        zielAngle = math.degrees(-math.atan((zielDist-dist)/20)) # Winkel zum ziel-Abstand
        angle = math.degrees(math.atan((lastDist-dist)/10))                # Vermutlicher Winkel des Autos zur Wand
        
        if zielAngle == angle:
             steer = 1
        elif angle < zielAngle:
            diffAngle = angle + zielAngle
            if angle < 0 and zielAngle > 0:
                diffAngle = -(angle - zielAngle)
            diffAngle = 1-diffAngle/90
            steer = diffAngle
            steer = ((angle+90)/(zielAngle+90))**speed
            #steer = 0.5
        elif angle > zielAngle:
            diffAngle = angle + zielAngle
            if angle > 0 and zielAngle < 0:
                diffAngle = zielAngle - angle
            diffAngle = 1-diffAngle/90
            steer = diffAngle
            steer = 2-(((zielAngle+90)/(angle+90))**speed)
            #steer = 1.5
        
        if steer > 2:
            steer = 2
        if steer < 0:
            steer = 0
            
        steer = (lastSteer + steer)/2
               
        print(" "*int(dist),"█"," "*int(70-dist),"d = %.1f cm" % dist,";s = %.2f" % steer,";a = %.1f°" % angle,";z = %.1f°" % zielAngle,";d = %.1f°" % diffAngle)
        print(" "*zielDist,"|")
        
        if vorne < 10 and lastVorne < 10:
            bremsen()
            print("Bremsen!")
            return
        elif vorne < 30 and lastVorne < 30:
            lenken(2)
            print("Lenken!")
            time.sleep(.4)
        elif abs(lastDist-dist) < 20:
            lenken(steer)
 
def main():

    
    
    losfahren()
    pr.start(speed)            # Motor A, speed% Tastverhältnis
    pl.start(speed)            # Motor B, speed% Tastverhältnis
    
    run_event = threading.Event()
    run_event.set()
    
    th1_delay = .02 # sleep dauer der Funktion
    th1 = threading.Thread(target = wandfahren, args = (th1_delay,run_event)) # Funkton in einem neuen Thread zuordnen

    th1.start() # Thread starten

    # Warten bis Srtg+C gedrückt wird:
    try:
        time.sleep(1)
                        
    except KeyboardInterrupt:
        print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
        run_event.clear()
        th1.join()
        aufraeumen()
        print ("threads successfully closed")

if __name__ == '__main__':
    main()
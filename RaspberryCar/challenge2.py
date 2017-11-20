import threading            # Modul threads
import time                 # Modul time
import math
from gpiosetup import *           # GPIO Setup importieren und ausführen
from abstand import distanz       # Funktion für Wandabstandmessen importieren
from aufraeumen import aufraeumen,bremsen # Funktion für cleanup() importieren

speed = 50      # Fahrgeschwindigkeit (% Tastverhältnis)

#
def forward():
    pr.ChangeDutyCycle(speed)  # Motor A, 100% Tastverhältnis
    pl.ChangeDutyCycle(speed)  # Motor B, 100% Tastverhältnis
    return
#    
def lenken(steer):
    pr.ChangeDutyCycle((2-steer)*speed)   # Tastverhältnis ändern
    pl.ChangeDutyCycle((steer)*speed)  # Motor B, 100% Tastverhältnis
    return

GPIO.output(IN1, 1)      # Motor A Rechtslauf
GPIO.output(IN2, 0)      # Motor A Rechtslauf
GPIO.output(IN3, 1)      # Motor B Rechtslauf
GPIO.output(IN4, 0)      # Motor B Rechtslauf

def wandfahren(delay, run_event):
    zielAngle = 0
    angle = 0
    zielDist = 30
    dist = distanz("L")
    steer = 0
    lastDist = dist
    
    print ("Distanz: ", dist)
    
    while run_event.is_set():
        time.sleep(delay)
        
        lastDist = (lastDist+dist)/2
        dist = distanz("L")
        vorne = distanz("R")
        
        if vorne < 15:
            bremsen()
            return

        zielAngle = math.degrees(-math.atan((zielDist-dist)/20)) # Winkel zum ziel-Abstand
        angle = math.degrees(math.atan((lastDist-dist)/10))                # Vermutlicher Winkel des Autos zur Wand
        
        if zielAngle == angle:
             steer = 1
        elif angle < zielAngle:
            steer = ((angle+90)/(zielAngle+90))**2
            #steer = 0.5
        elif angle > zielAngle:
            steer = 2-(((zielAngle+90)/(angle+90))**2)
            #steer = 1.5
            
        if steer > 2:
            steer = 2
            
        print(" "*int(dist),"█"," "*int(50-dist),"d = %.1f cm" % dist,";s = %.1f" % steer,";a = %.1f°" % angle,";z = %.1f°" % zielAngle)
        print(" "*zielDist,"|")
        
        if abs(lastDist-dist) < 20:
            lenken(steer)
 
def main():
    
    t = 6
    while t >= 0:
        print ("Start in ",t," sekunden",end="\r")
        t -= 1
        time.sleep(1)
    
    pr.start(speed)            # Motor A, speed% Tastverhältnis
    pl.start(speed)            # Motor B, speed% Tastverhältnis
    
    run_event = threading.Event()
    run_event.set()
    
    th1_delay = .05 # sleep dauer der Funktion
    th1 = threading.Thread(target = wandfahren, args = (th1_delay,run_event)) # Funkton in einem neuen Thread zuordnen

    th1.start() # Thread starten

    # Warten bis Srtg+C gedrückt wird:
    i = 0
    try:
        while 1:
            i += 1
            time.sleep(.01)
            if i == 200000:
                print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
                run_event.clear()
                th1.join()
                bremsen()
                print ("threads successfully closed")
                
    except KeyboardInterrupt:
        print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
        run_event.clear()
        th1.join()
        aufraeumen()
        print ("threads successfully closed")

if __name__ == '__main__':
    main()
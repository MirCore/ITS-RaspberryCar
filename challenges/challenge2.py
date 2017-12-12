import threading            # Modul threads
import time                 # Modul time
import math
from RaspberryCar.gpiosetup import *           # GPIO Setup importieren und ausführen
from RaspberryCar.abstand import distanz       # Funktion für Wandabstandmessen importieren
from RaspberryCar.aufraeumen import aufraeumen,bremsen # Funktion für cleanup() importieren

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
    vorne = 0
    lastVorne = 0
    
    print ("Distanz: ", dist)
    
    while run_event.is_set():
        time.sleep(delay)
        
        lastDist = (lastDist+dist)/2
        dist = distanz("L")
        lastVorne = vorne
        vorne = distanz("R")
        
        zielAngle = math.degrees(-math.atan((zielDist-dist)/20)) # Winkel zum ziel-Abstand
        angle = math.degrees(math.atan((lastDist-dist)/10))      # Vermutlicher Winkel des Autos zur Wand
        
        gefahren = lastDist-dist
        zielabstand = -(zielDist-dist)/10
        
        if gefahren > 5:
            steer = 1
        elif gefahren == zielabstand:
             steer = 1
        elif gefahren < zielabstand:
            #steer = zielabstand-gefahren
            steer = (zielabstand-gefahren)/5
            #steer = 0.5
        elif gefahren > zielabstand:
            #steer = gefahren-zielabstand
            steer = (gefahren-zielabstand)/5
            #steer = 1.5
        
        steer = steer
        if steer > 2:
            steer = 2
        if steer < 0:
            steer = 0
           
        print(" "*int(dist),"█"," "*int(50-dist),"d = %.1f cm" % dist,";s = %.1f" % steer,";g = %.1f" % gefahren,";z = %.1f" % zielabstand)
        print(" "*zielDist,"|")
        
        if vorne < 10:
            bremsen()
            return
        elif vorne < 30 and lastVorne < 30:
            lenken(2)
            time.sleep(.4)
        elif abs(lastDist-dist) < 20:
            lenken(steer)
 
def main():
    
    print ("Taster drücken")
    while GPIO.input(GPIO_TASTER) == 1:
        time.sleep(.1)
    print("Start in 1 Sekunde", end="\r")
    time.sleep(1)
    
    pr.start(speed)            # Motor A, speed% Tastverhältnis
    pl.start(speed)            # Motor B, speed% Tastverhältnis
    
    run_event = threading.Event()
    run_event.set()
    
    th1_delay = .05 # sleep dauer der Funktion
    th1 = threading.Thread(target = wandfahren, args = (th1_delay,run_event)) # Funkton in einem neuen Thread zuordnen

    th1.start() # Thread starten

    # Warten bis Strg+C gedrückt wird:
    i = 0
    try:
        while GPIO.input(GPIO_TASTER) == 1:
            time.sleep(.01)
        print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
        run_event.clear()
        th1.join()
        aufraeumen()
        print ("threads successfully closed")
                
    except KeyboardInterrupt:
        print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
        run_event.clear()
        th1.join()
        aufraeumen()
        print ("threads successfully closed")

if __name__ == '__main__':
    main()
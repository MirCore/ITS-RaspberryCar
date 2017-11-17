import threading            # Modul threads
import time                 # Modul time
from gpiosetup import *           # GPIO Setup importieren und ausführen
from abstand import distanz       # Funktion für Wandabstandmessen importieren
from aufraeumen import aufraeumen # Funktion für cleanup() importieren

speed = 50      # Fahrgeschwindigkeit (% Tastverhältnis)
steerLow  = 0.2 # Fahrgeschwindigkeit Kurve Außenseite
steerHigh = 1.5 # Fahrgeschwindigkeit Kurve Innenseite

#pr.start(speed)            # Motor A, speed% Tastverhältnis
#pl.start(speed)            # Motor B, speed% Tastverhältnis
#
#def forward():
#    pr.ChangeDutyCycle(speed)  # Motor A, 100% Tastverhältnis
#    pl.ChangeDutyCycle(speed)  # Motor B, 100% Tastverhältnis
#    
#def rechts(steerLow, steerHigh):
#    pr.ChangeDutyCycle(steerLow*speed)   # Tastverhältnis ändern
#    pl.ChangeDutyCycle(steerHigh*speed)  # Motor B, 100% Tastverhältnis
#
#def links(steerLow, steerHigh):
#    pr.ChangeDutyCycle(steerHigh*speed)  # Tastverhältnis ändern
#    pl.ChangeDutyCycle(steerLow*speed)   # Motor B, 100% Tastverhältnis
#    
#GPIO.output(IN1, 1)      # Motor A Rechtslauf
#GPIO.output(IN2, 0)      # Motor A Rechtslauf
#GPIO.output(IN3, 1)      # Motor B Rechtslauf
#GPIO.output(IN4, 0)      # Motor B Rechtslauf

anfangsDistanz = distanz("L")
uGrenze = anfangsDistanz - 2
oGrenze = anfangsDistanz + 2

print ("Distanz: ", anfangsDistanz)
print ("U: ", uGrenze)
print ("O ", oGrenze)

def wandfahren(delay, run_event):
    while run_event.is_set():
        time.sleep(delay)

        abstand = distanz("L")
        print ("Gemessene Entfernung Links = %.1f cm" % abstand)  
        abstand = distanz("R")
        print ("Gemessene Entfernung Rechts = %.1f cm" % abstand)  
    
#        if uGrenze <= abstand <= oGrenze:
#            forward()   
#        elif abstand < uGrenze:
#            rechts(.2, 1.5)
#        elif abstand > oGrenze:
#            links(.2, 1.5)
 
def main():
    run_event = threading.Event()
    run_event.set()
    
    th1_delay = 1 # sleep dauer der Funktion
    th1 = threading.Thread(target = wandfahren, args = (th1_delay,run_event)) # Funkton in einem neuen Thread zuordnen

    th1.start() # Thread starten

    # Warten bis Srtg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)
    except KeyboardInterrupt:
        print ("attempting to close threads. Max wait =", max(th1_delay,0)) # Bei mehreren Threads: 0 durch th2_delay erstzen
        run_event.clear()
        th1.join()
        aufraeumen()
        print ("threads successfully closed")

if __name__ == '__main__':
    main()
import threading            # Modul threads
import time                 # Modul time
import math
from random import randint
  
zielDistanz = 30
anfangsDistanz = zielDistanz+randint(10,30)*randint(-1,1)

print ("Distanz: ", anfangsDistanz)

def wandfahren(delay, run_event):
    dist = anfangsDistanz
    unknownAngle = 0
    zielAngle = 0
    angle = 0
    steer = 1
    
    while run_event.is_set():
        time.sleep(delay)
        lastDist = dist
        
#        if zielDistanz == dist:
#             steer = 1
#        elif dist < zielDistanz:
#            steer = dist/zielDistanz
#            #steer = 0.5
#        elif dist > zielDistanz:
#            steer = 2-zielDistanz/dist
#            #steer = 1.5
            
        if zielAngle == angle:
             steer = 1
        elif angle > zielAngle:
            steer = angle/zielAngle
            steer = dist/zielDistanz
            #steer = 0.5
        elif angle < zielAngle:
            steer = dist/zielDistanz
            steer = 2-zielAngle/angle
            #steer = 1.5
            
        drift = 20
        unknownAngle = unknownAngle + 2*(1-steer) + randint(-drift,drift)/10
        dist = dist+math.sin(math.radians(unknownAngle))
        
        zielAngle = math.degrees(-(zielDistanz-dist)/zielDistanz)
        angle = math.degrees(lastDist-dist)
        
        print(" "*int(dist),"█"," "*int(50-dist),"d = %.1f cm" % dist,";s = %.1f" % steer,";ua = %.1f°" % unknownAngle,";a = %.1f°" % angle,";z = %.1f°" % zielAngle)
        print(" "*zielDistanz,"|")

 
def main():
    run_event = threading.Event()
    run_event.set()
    
    th1_delay = .1 # sleep dauer der Funktion
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
        time.sleep(.01)
        print ("threads successfully closed")

if __name__ == '__main__':
    main()
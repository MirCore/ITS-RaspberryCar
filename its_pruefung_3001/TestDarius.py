import math
import time  # Modul time
import os

from aufraeumen import aufraeumen, losfahren, bremsen  # Funktion für cleanup() importieren
from setup import *  # GPIO Setup importieren und ausführen

      

def main():
    
      
    
    losfahren()
    pl.start(20)  # Motor B, speed% Tastverhältnis
    pr.start(20)  # Motor A, speed% Tastverhältnis
    
    #pr.ChangeDutyCycle(speed)
    #pl.ChangeDutyCycle(speed)


    # Warten bis Strg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        bremsen()
        aufraeumen()
        print("hallo lol")
        
        
if __name__ == '__main__':
    main()
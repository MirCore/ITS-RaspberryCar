import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time                 # Modul time
from setup import * 

def distanz(seite):
    if seite == "L":
        GPIO_ECHO = GPIO_ECHO_L
    else:
        GPIO_ECHO = GPIO_ECHO_R
        
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartZeit = time.time()
    StopZeit = time.time()
    
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
        if StartZeit - StopZeit > .1:
            print("ERROR Sensor 1")
            break
            
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
        if StopZeit - StartZeit > .1:
            print("ERROR Sensor 2")
            break
        
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    #time.sleep(.01)
    return distanz
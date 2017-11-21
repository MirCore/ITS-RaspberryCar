import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
import statistics
GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern

# GPIO-Channel festlegen

# GPIO Trigger und Echo festlegen
GPIO_TRIGGER = 21
GPIO_ECHO = 20

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distanz():
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
        
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
        
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2
    return distanz

try:
    while True:
        abstand = statistics.median([distanz(),distanz(),distanz(),distanz(),distanz()])
        print ("Gemessene Entfernung = %.1f cm" % abstand)
        time.sleep(.5)

except KeyboardInterrupt:
    GPIO.cleanup()       # Aufräumen
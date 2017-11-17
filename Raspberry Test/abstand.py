import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern

# GPIO Trigger und Echo festlegen
GPIO_TRIGGER_R = 21
GPIO_ECHO_R = 20
GPIO_TRIGGER_L = 16
GPIO_ECHO_L = 12

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)

def distanz(seite):
    if seite == "L":
        GPIO_TRIGGER = GPIO_TRIGGER_L
        GPIO_ECHO = GPIO_ECHO_L
    else:
        GPIO_TRIGGER = GPIO_TRIGGER_R
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
        
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
        
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2
    return distanz
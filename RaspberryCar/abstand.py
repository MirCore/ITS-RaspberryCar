#import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren

def distanz(seite):
#    if seite == "L":
#        GPIO_TRIGGER = GPIO_TRIGGER_L
#        GPIO_ECHO = GPIO_ECHO_L
#    else:
#        GPIO_TRIGGER = GPIO_TRIGGER_R
#        GPIO_ECHO = GPIO_ECHO_R
#        
#    # setze Trigger auf HIGH
#    GPIO.output(GPIO_TRIGGER, True)
#    
#    # setze Trigger nach 0.01ms aus LOW
#    time.sleep(0.00001)
#    GPIO.output(GPIO_TRIGGER, False)
#    
#    StartZeit = time.time()
#    StopZeit = time.time()
#    
#    # speichere Startzeit
#    while GPIO.input(GPIO_ECHO) == 0:
#        StartZeit = time.time()
#        
#    # speichere Ankunftszeit
#    while GPIO.input(GPIO_ECHO) == 1:
#        StopZeit = time.time()
#        
#    # Zeit Differenz zwischen Start und Ankunft
#    TimeElapsed = StopZeit - StartZeit
#    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
#    # und durch 2 teilen, da hin und zurueck
#    distanz = (TimeElapsed * 34300) / 2
    if seite == "L":
        distanz = 1
    else:
        distanz = 2    
    return distanz
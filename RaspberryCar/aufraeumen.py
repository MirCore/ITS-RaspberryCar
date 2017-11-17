import time                 # Modul time

def aufraeumen():
    ## Erst bremsen dann cleanup
#    GPIO.output(IN1, 0)  # Bremsen
#    GPIO.output(IN2, 0)  # Bremsen
#    GPIO.output(IN3, 0)  # Bremsen
#    GPIO.output(IN4, 0)  # Bremsen
    time.sleep(.1)
#    GPIO.cleanup()       # Aufräumen
    print ("GPIOs aufgeräumt")
import RPi.GPIO as GPIO
import time # Modul time importieren 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
r=18
y=23
g=24

def einled(gpio,t):
    GPIO.output(gpio, True) # Lege 3.3V auf Pin 26 
    time.sleep (t) # Warte 500ms 
    GPIO.output(gpio, False) # Lege 0V auf Pin 26 
    
def zweiled(gpio1,gpio2,t1):
    GPIO.output(gpio1, True) # Lege 3.3V auf Pin 26 
    GPIO.output(gpio2, True) # Lege 0V auf Pin 26 
    time.sleep (t1) # Warte 500ms 
    GPIO.output(gpio1, False) # Lege 0V auf Pin 26
    GPIO.output(gpio2, False) # Lege 3.3V auf Pin 26 

def end():
    GPIO.cleanup() # Aufräumen    
    
einled(r,1)    
zweiled(r,y,1)
einled(g,5)
einled(y,1)
einled(r,5)

end()
import RPi.GPIO as GPIO # GPIO Bibliothek importieren 
import time # Modul time importieren 

def blinken():
    GPIO.setmode(GPIO.BOARD) # Verwende Board−Pinnummern 
    GPIO.setup(26, GPIO.OUT) # Setze Pin 26 (GPIO7) als Ausgang 
    GPIO.output(26, True) # Lege 3.3V auf Pin 26 
    time.sleep (0.5) # Warte 500ms 
    GPIO.output(26, False) # Lege 0V auf Pin 26 
    GPIO.cleanup() # Aufräumen
    time.sleep (1)
    
blinken()    
blinken()    
blinken()    
blinken()    
blinken()    
blinken()    
blinken()    
blinken()    
blinken()
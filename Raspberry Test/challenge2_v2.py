import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
import threading         # time.sleep ersatz
import signal            # keyboard interrupt ersatz
import sys               # Für strg+C

GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern
from abstand import distanz # 
from aufraeumen import *   #

def aufraeumen():
    GPIO.output(IN1, 0)  # Bremsen
    GPIO.output(IN2, 0)  # Bremsen
    GPIO.output(IN3, 0)  # Bremsen
    GPIO.output(IN4, 0)  # Bremsen
    GPIO.cleanup()       # Aufräumen

def signal_handler(signal, frame):
    print ("")
    aufraeumen()       # Aufräumen
    #sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# GPIO-Channel festlegen
# Motor A
ENA = 10   # Enable Motor A
IN1 = 9    # In 1
IN2 = 11   # In 2
# Motor B
ENB = 22  # Enable Motor B
IN3 = 17  # In 3
IN4 = 27  # In 4

# GPIOs als Ausgang setzen
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# GPIO Trigger und Echo festlegen
GPIO_TRIGGER = 21
GPIO_ECHO = 20

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# PWM für Motor A und B
p1 = GPIO.PWM(ENA, 70)  # Motor A, Frequenz = 1000 Hz
p2 = GPIO.PWM(ENB, 70)  # Motor B, Frequenz = 1000 Hz

speed = 50

p1.start(speed)            # Motor A, 100% Tastverhältnis
p2.start(speed)            # Motor B, 100% Tastverhältnis

def forward():
    p1.ChangeDutyCycle(speed)  # Motor A, 100% Tastverhältnis
    p2.ChangeDutyCycle(speed)  # Motor B, 100% Tastverhältnis
    
def rechts():
    p1.ChangeDutyCycle(.2*speed)   # Tastverhältnis ändern
    p2.ChangeDutyCycle(1.5*speed)  # Motor B, 100% Tastverhältnis

def links():
    p1.ChangeDutyCycle(1.5*speed)  # Tastverhältnis ändern
    p2.ChangeDutyCycle(.2*speed)   # Motor B, 100% Tastverhältnis
    
GPIO.output(IN1, 1)      # Motor A Rechtslauf
GPIO.output(IN2, 0)      # Motor A Rechtslauf
GPIO.output(IN3, 1)      # Motor B Rechtslauf
GPIO.output(IN4, 0)      # Motor B Rechtslauf

anfangsDistanz = distanz("L")
uGrenze = anfangsDistanz - 2
oGrenze = anfangsDistanz + 2

print ("Distanz: ", anfangsDistanz)
print ("U: ", uGrenze)
print ("O ", oGrenze)

def wandfahren():
    abstand = distanz("L")
    print ("Gemessene Entfernung Links = %.1f cm" % abstand)  

    if uGrenze <= abstand <= oGrenze:
        forward()   
    elif abstand < uGrenze:
        rechts()
    elif abstand > oGrenze:
        links()
    threading.Timer(0.01, wandfahren).start()
    
wandfahren()
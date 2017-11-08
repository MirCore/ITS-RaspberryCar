import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time  # Modul time importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

# GPIO-Channel festlegen
# Motor A
ENA = 2  # Enable Motor A
IN1 = 3  # In 1
IN2 = 4  # In 2

# Motor B
ENB = 22 # Enable Motor B
IN3 = 17 # In 3
IN4 = 27 # In 4

# GPIOs als Ausgang setzen
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.output(IN1, GPIO.LOW)   # Bremsen
GPIO.output(IN2, GPIO.LOW)   # Bremsen
GPIO.output(IN3, GPIO.LOW)   # Bremsen
GPIO.output(IN4, GPIO.LOW)   # Bremsen

GPIO.cleanup()  # Aufräumen

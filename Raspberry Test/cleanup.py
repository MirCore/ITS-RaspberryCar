import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time  # Modul time importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

# GPIO-Channel festlegen
# Motor A
ENA = 2  # Enable Motor A
IN1 = 3  # In 1
IN2 = 4  # In 2

# Motor B
ENB = 17
IN3 = 27
IN4 = 22

# GPIOs als Ausgang setzen
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.cleanup()  # Aufräumen
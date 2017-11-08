import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time  # Modul time importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

t = input("BCM angeben: ")
t = int(t)

# GPIO-Channel festlegen
# Motor A
ENA = 2  # Enable Motor A

# Motor B
ENB = 22 # Enable Motor B

# GPIOs als Ausgang setzen
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

GPIO.setup(t, GPIO.OUT)

# Enable für Motor A und B anschalten
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(ENB, GPIO.HIGH)


GPIO.output(t, GPIO.HIGH)
time.sleep(1)                # Zeit, die das Auto fährt
GPIO.output(t, GPIO.LOW)
GPIO.cleanup()  # Aufräumen

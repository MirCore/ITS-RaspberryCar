import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time  # Modul time importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

# GPIO-Channel festlegen
# Motor A
ENA = 4  # Enable Motor A
IN1 = 3  # In 1
IN2 = 2  # In 2

# GPIOs als Ausgang setzen
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Enable für Motor A und B anschalten
GPIO.output(ENA, GPIO.HIGH)

t = input("Zeit in Sekunden angeben: ")
t = int(t)

# Funktion: Vorwärtsfahren
def forward(t):
    GPIO.output(IN1, GPIO.LOW)  # Motor A Rechtslauf
    GPIO.output(IN2, GPIO.HIGH)  # Motor A Rechtslauf
    time.sleep(t)                # Zeit, die das Auto fährt
    GPIO.output(IN1, GPIO.LOW)   # Bremsen
    GPIO.output(IN2, GPIO.LOW)   # Bremsen

print ("Auto fährt vorwärts.")
forward(t)  # Funktion ausführen
GPIO.cleanup()  # Aufräumen

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

# Enable für Motor A und B anschalten
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(ENB, GPIO.HIGH)

t = input("Zeit in Sekunden angeben: ")

print t

# Funktion: Vorwärtsfahren
def forward(t):
    GPIO.output(IN1, GPIO.HIGH)  # Motor A Rechtslauf
    GPIO.output(IN2, GPIO.LOW)   # Motor A Rechtslauf
    GPIO.output(IN3, GPIO.LOW)   # Motor B Linkslauf
    GPIO.output(IN4, GPIO.HIGH)  # Motor B Linkslauf
    time.sleep(t)                # Zeit, die das Auto fährt
    GPIO.output(IN1, GPIO.LOW)   # Bremsen
    GPIO.output(IN2, GPIO.LOW)   # Bremsen
    GPIO.output(IN3, GPIO.LOW)   # Bremsen
    GPIO.output(IN4, GPIO.LOW)   # Bremsen

print ("Auto faehrt vorwaerts.")
forward(t)  # Funktion ausführen

GPIO.cleanup()  # Aufräumen

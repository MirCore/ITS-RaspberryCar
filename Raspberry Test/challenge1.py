import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time  # Modul time importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

# GPIO-Channel festlegen
# Motor A
ENA = 4  # Enable Motor A
IN1 = 3  # In 1
IN2 = 2  # In 2

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

# Enable für Motor A und B anschalten
GPIO.output(ENA, True)
GPIO.output(ENB, True)

t = input("Zeit in Sekunden angeben: ")
t = int(t)

# Funktion: Vorwärtsfahren
def forward(t):
    GPIO.output(IN1, False)   # Motor A Rechtslauf
    GPIO.output(IN2, True)  # Motor A Rechtslauf
    GPIO.output(IN3, False)   # Motor B Linkslauf
    GPIO.output(IN4, True)  # Motor B Linkslauf
    time.sleep(t)                # Zeit, die das Auto fährt
    GPIO.output(IN1, True)   # Bremsen
    GPIO.output(IN2, True)   # Bremsen
    GPIO.output(IN3, True)   # Bremsen
    GPIO.output(IN4, True)   # Bremsen

print ("Auto fährt vorwärts.")
forward(t)  # Funktion ausführen
GPIO.cleanup()  # Aufräumen

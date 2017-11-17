import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren
import time              # Modul time importieren
GPIO.setmode(GPIO.BCM)   # Verwende BCM-Pinnummern

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

# Enable für Motor A und B anschalten
GPIO.output(ENA, 1)
GPIO.output(ENB, 1)

# Fahrzeit abfragen
t = input("Zeit in Sekunden angeben: ")
t = int(t)

# Funktion: Vorwärtsfahren
def forward(t):
    GPIO.output(IN1, 1)  # Motor A Rechtslauf
    GPIO.output(IN2, 0)  # Motor A Rechtslauf
    GPIO.output(IN3, 1)  # Motor B Rechtslauf
    GPIO.output(IN4, 0)  # Motor B Rechtslauf   
    time.sleep(t)        # Fahrzeit
    GPIO.output(IN1, 0)  # Bremsen
    GPIO.output(IN2, 0)  # Bremsen
    GPIO.output(IN3, 0)  # Bremsen
    GPIO.output(IN4, 0)  # Bremsen

# Fahrtbeginn
print ("Auto fährt geradeaus für", t, "Sekunden.")
forward(t)      # Funktion ausführen
GPIO.cleanup()  # Aufräumen
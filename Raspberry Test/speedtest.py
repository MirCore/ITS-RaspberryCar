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

# PWM für Motor A und B
p1 = GPIO.PWM(ENA, 1000)  # Motor A, Frequenz = 1000 Hz
p2 = GPIO.PWM(ENB, 1000)  # Motor B, Frequenz = 1000 Hz

p1.start(100)            # Motor A, 100% Tastverhältnis
p2.start(100)            # Motor B, 100% Tastverhältnis

GPIO.output(IN1, 1)      # Motor A Rechtslauf
GPIO.output(IN2, 0)      # Motor A Rechtslauf
GPIO.output(IN3, 1)      # Motor B Rechtslauf
GPIO.output(IN4, 0)      # Motor B Rechtslauf

# Vorwärts fahren
input("Langsamer fahren?")
p1.ChangeDutyCycle(50)   # Tastverhältnis ändern
p2.ChangeDutyCycle(50)   # Tastverhältnis ändern
input("Bremsen?")
GPIO.output(IN1, 0)      # Motor A Bremsen
GPIO.output(IN2, 0)      # Motor A Bremsen
GPIO.output(IN3, 0)      # Motor B Bremsen
GPIO.output(IN4, 0)      # Motor B Bremsen
p1.stop()
p2.stop()
GPIO.cleanup()
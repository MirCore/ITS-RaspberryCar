import RPi.GPIO as GPIO     # GPIO-Bibliothek importieren
GPIO.setmode(GPIO.BCM)      # Verwende BCM-Pinnummern

## GPIO für Motoren
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
pr = GPIO.PWM(ENA, 70)  # Motor A, Frequenz = 70 Hz
pl = GPIO.PWM(ENB, 70)  # Motor B, Frequenz = 70 Hz

GPIO.output(IN1, 0)  # Bremsen
GPIO.output(IN2, 0)  # Bremsen
GPIO.output(IN3, 0)  # Bremsen
GPIO.output(IN4, 0)  # Bremsen

#Taster
GPIO_TASTER = 4
GPIO.setup(GPIO_TASTER, GPIO.IN)

print ("GPIOs setup erfolgreich")
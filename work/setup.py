import RPi.GPIO as GPIO  # GPIO-Bibliothek importieren

GPIO.setmode(GPIO.BCM)  # Verwende BCM-Pinnummern

# GPIO für Motoren
# GPIO-Channel festlegen
# Motor A
ENA = 10  # Enable Motor A
IN1 = 9  # In 1
IN2 = 11  # In 2
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

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# PWM für Motor A und B
pr = GPIO.PWM(ENA, 73)  # Motor A, Frequenz = 70 Hz
pl = GPIO.PWM(ENB, 73)  # Motor B, Frequenz = 70 Hz

# GPIO für Echo
# GPIO Trigger und Echo festlegen
GPIO_ECHO_R = 12
GPIO_TRIGGER = 16
GPIO_ECHO_L = 20

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)

GPIO.output(IN1, 0)  # Bremsen
GPIO.output(IN2, 0)  # Bremsen
GPIO.output(IN3, 0)  # Bremsen
GPIO.output(IN4, 0)  # Bremsen

# Taster
GPIO_TASTER = 4
GPIO.setup(GPIO_TASTER, GPIO.IN)

global speed
global line_found
global wall_found
global line_steer
global wall_steer
speed = 3  # 1 bis 4 (*25% Tastverhältnis)
line_found = False
wall_found = False
line_steer = 1
wall_steer = 1

print("GPIO-Setup erfolgreich")

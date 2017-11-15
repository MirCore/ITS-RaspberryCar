import signal            # keyboard interrupt ersatz
import sys               # Für strg+C

def aufraeumen():
    GPIO.output(IN1, 0)  # Bremsen
    GPIO.output(IN2, 0)  # Bremsen
    GPIO.output(IN3, 0)  # Bremsen
    GPIO.output(IN4, 0)  # Bremsen
    GPIO.cleanup()       # Aufräumen

def signal_handler(signal, frame):
    print ("")
    aufraeumen()       # Aufräumen
    sys.exit(0)
import math
import statistics
import time  # Modul time
from abstand import distanz  # Funktion für Wandabstand messen importieren
from setup import *

def wandfahren(delay, run_event):
    global wall_steer
    global wall_found
    global speed

    zielDist = 30
    dist = distanz("L")
    steer = 1
    print("Distanz: ", dist)

    while run_event.is_set():
        lastDist = dist
        lastSteer = steer
        dist = statistics.median([distanz("L"), distanz("L"), distanz("L"), distanz("L"), distanz("L"), distanz("L")])

        if dist > 60:
            wall_found = False
        else:
            wall_found = True

        zielAngle = math.degrees(-math.atan((zielDist - dist) / 20))  # Winkel zum ziel-Abstand
        angle = math.degrees(math.atan((lastDist - dist) / 10))  # Vermutlicher Winkel des Autos zur Wand

        if zielAngle == angle:
            steer = 1
        elif angle < zielAngle:
            steer = ((angle + 90) / (zielAngle + 90)) ** speed
        elif angle > zielAngle:
            steer = 2 - (((zielAngle + 90) / (angle + 90)) ** speed)

        if steer > 2:
            steer = 2
        if steer < 0:
            steer = 0

        steer = (lastSteer + steer) / 2
        wall_steer = steer

        print(" " * int(dist), "█", " " * int(70 - dist), "d = %.1f cm" % dist, ";s = %.2f" % steer, ";a = %.1f°" % angle,
              ";z = %.1f°" % zielAngle)
        print(" " * zielDist, "|")

        time.sleep(delay)
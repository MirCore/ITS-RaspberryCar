import math
import statistics
from abstand import distanz       # Funktion für Wandabstandmessen importieren
speed = 3
zielAngle = 0
angle = 0
zielDist = 30
steer = 0
dist = distanz("L")
lastDist = dist
lastSteer = 1

print ("Distanz: ", dist)

def wandfahren():
    global dist
    global steer
    
    lastDist = dist
    dist = statistics.median([distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L"),distanz("L")])
    lastSteer = steer

    zielAngle = math.degrees(-math.atan((zielDist-dist)/20)) # Winkel zum ziel-Abstand
    angle = math.degrees(math.atan((lastDist-dist)/10))      # Vermutlicher Winkel des Autos zur Wand
    
    if zielAngle == angle:
         steer = 1
    elif angle < zielAngle:
        steer = ((angle+90)/(zielAngle+90))**speed
    elif angle > zielAngle:
        steer = 2-(((zielAngle+90)/(angle+90))**speed)
    
    if steer > 2:
        steer = 2
    if steer < 0:
        steer = 0
        
    steer = (lastSteer + steer)/2
           
    print(" "*int(dist),"█"," "*int(70-dist),"d = %.1f cm" % dist,";s = %.2f" % steer,";a = %.1f°" % angle,";z = %.1f°" % zielAngle)
    print(" "*zielDist,"|")
    
    return steer
import cv2             # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
np.set_printoptions(threshold=5, precision=2) # Dies ist nur für dieses Handson wichtig (Anzeige von langen Zahlenkolonnen)

cap = cv2.VideoCapture(0) # Input 0

x = 0
ret, img = cap.read()
width = np.size(img, 1)
ideal = width/2

def line(zeileNr):
    ret, img = cap.read()
    
    img_rgb = img[:, :, ::-1] # Umdrehen der Farbkanäle
    img_red = img[:,:,2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[:,:,1]
    img_blue = img[:,:,0]

    zeile = img_red[zeileNr, :]
    img_redness = img_red.astype('int16') - (img_green/2+img_blue/2)

    # ZeileNr herausnehmen:
    zeile = img_redness[zeileNr, :]

    # Dann wenden wir einen Schwellwert an:
    zeile_bin = zeile>60

    # Mittelpunkt berechnen:
    x = np.arange( zeile_bin.shape[0] ) #x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
    if zeile_bin.sum() != 0:
        mittelpunkt = (zeile_bin*x).sum() / zeile_bin.sum()
    else:
        mittelpunkt = None
    return mittelpunkt

def linienfahren():
    global x
    lastX = x
    x = line(400)

    if x is None:
        return None
    
    zielAngle = math.degrees(-math.atan((ideal-x)/20)) # Winkel zum ziel-Abstand
    angle = math.degrees(math.atan((lastX-x)/10))      # Vermutlicher Winkel des Autos zur Wand
    
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

    print(" "*int(x),"█"," "*int(70-x),"x = %.1f cm" % x,";ideal = %.1f" % ideal)
    print(" "*zielDist,"|")
    
    return steer
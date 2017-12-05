import cv2             # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
np.set_printoptions(threshold=5, precision=2) # Dies ist nur für dieses Handson wichtig (Anzeige von langen Zahlenkolonnen)

cap = cv2.VideoCapture(0) # Input 0

def detection():
    ret, img = cap.read()
    return img

x = 0
img = detection()
width = np.size(img, 1)
ideal = width/2
uGrenze = (ideal)-20
oGrenze = (ideal)+20
print("Spalten:", width)

def line(img):
    img_rgb = img[:, :, ::-1] # Umdrehen der Farbkanäle
    img_red = img[:,:,2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[:,:,1]
    img_blue = img[:,:,0]

    zeile400 = img_red[400, :]
    img_redness = img_red.astype('int16') - (img_green/2+img_blue/2)

    # Zeile 400 herausnehmen:
    zeile400 = img_redness[400, :]

    # Dann wenden wir einen Schwellwert an:
    zeile400_bin = zeile400>60

    # Mittelpunkt berechnen:
    x = np.arange( zeile400_bin.shape[0] ) #x=0,1,2 ... N-1 (N=Anzahl von Werten in zeile400_bin)
    if zeile400_bin.sum() != 0:
        mittelpunkt = (zeile400_bin*x).sum() / zeile400_bin.sum()
    else:
        mittelpunkt = None
    return mittelpunkt

def linienfahren():
    global x
    img = detection()
    lastX = x
    x = line(img)

    if x is None:
        return None

    rounded = round(x,1)

    if x == ideal:
        steer = 2
    elif x < ideal:
        steer = (x/ideal)**2
    elif x < ideal-70:
        steer = (x/ideal)**3
    elif x > ideal:
        steer = (ideal/x)**2
        steer = 2-steer
    elif x > ideal+70:
        steer = (ideal/x)**3
        steer = 2-steer
    
    print("Linienmittelpunkt:",rounded, steer, " "*int(0.2*x),"█")
    
    return steer
import cv2  # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np  # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)
import math
import time  # Modul time
from setup import *

np.set_printoptions(threshold=5, precision=2)  # Anzeige von langen Zahlenkolonnen

cap = cv2.VideoCapture(0)  # Input 0

def linie(zeileNr):
    ret, img = cap.read()
    img_red = img[zeileNr, :, 2]  # Alles aus der Dimension Höhe und Breite (:,:) und den Farbkanal 2
    img_green = img[zeileNr, :, 1]
    img_blue = img[zeileNr, :, 0]

    zeile_bin = (img_red.astype('int16') - (img_green / 2 + img_blue / 2)) > 60

    if zeile_bin.sum() != 0:
        mittelpunkt = (zeile_bin * np.arange(zeile_bin.shape[0])).sum() / zeile_bin.sum()
        return mittelpunkt
    else:
        return None

import cv2             # Dies ist die Bildverarbeitungsbibliothek OpenCV
import numpy as np     # Rechnen mit vielen Zahlen in einem Array (z. B. Bilder)

green = np.uint8([[[187,187,252]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print (hsv_green)

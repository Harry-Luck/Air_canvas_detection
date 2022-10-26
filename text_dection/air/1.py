import cv2
import numpy as np
import time
import os
import module as htm

brushThickness = 15
eraserThickness = 100

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for impath  in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]

drawColor = (255, 0, 255)

cap  = cv2.VideoCapture(0)
cap.set(3, 1288)
cap.set(4, 728)

# detector = htm.handDetector(detectionCon = 0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((728, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()    
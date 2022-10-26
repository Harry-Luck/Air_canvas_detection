from ast import While
import cv2
import numpy as np
import time
import os
import module as htm

import pytesseract

brushThickness = 15
eraserThickness = 100

folderPath = "Header"
myList = os.listdir(folderPath)
# print(myList)

overlayList = []
for impath  in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    image = cv2.resize(image, (640, 125))
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]


drawColor = (255, 0, 255)

cap  = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
he_cap = cap.get(3)

we_cap = cap.get(4)

print("hegit",he_cap)
print('width',we_cap)
# btn_he = (he_cap/5)
btn_he = 125
# overlayList = []
# for impath  in myList:
#     image = cv2.imread(f'{folderPath}/{impath}')
#     image = cv2.resize(image, (he_cap, btn_he))
#     overlayList.append(image)
# # print(len(overlayList))
# header = overlayList[0]
btn_we =[0, (we_cap/4), (we_cap*2/4),(we_cap*2/4), (we_cap*2/4), (we_cap*3/4) ]

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((int(he_cap), int(we_cap), 3), np.uint8)
while True:
    success, img = cap.read()
    # img = cv2.imread('4.jpg')
    img[0:125, 0:1280] = header
    img = cv2.flip(img, 1)

    # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
    # img1 = cv2.resize(img, (500, 500))
    # # plate = pytesseract.image_to_string(img1)
    # # print("111111111111111111111", plate)


    # gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # # dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    # cv2.imshow("323rwsfrf3wff",thresh1)
    # contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL,
    #                                              cv2.CHAIN_APPROX_NONE)
    # im2 = thresh1.copy()
    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cropped = thresh1[x:x + w, y:y + h]
    #     cv2.imshow("dseefseff", cropped)
    #     text = pytesseract.image_to_string(cropped)
    #     print("text1111111111111111111",text)
    # print("ddddd")
    img=  detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList)!= 0:
        
        # print(lmList)
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        # print(fingers)
        # If selection mode - two fingers up
        if fingers[1] and fingers[2]:
            xp,yp = 0, 0            
            # print('Selection Mode')
            #checking for the click
            if y1 < btn_he:
                if btn_we[0]<x1<btn_we[1]:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif btn_we[1] <x1<btn_we[2]:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif btn_we[2] <x1<btn_we[3]:
                    header = overlayList[2]
                    drawColor = (0, 0, 0)
                elif btn_we[3] <x1<btn_we[4]:
                    header = overlayList[3]
            cv2.rectangle(img, (x1, y1-15),(x2, y2+25), drawColor, cv2.FILLED)


            pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
            img1 = cv2.resize(img, (300, 300))
            plate = pytesseract.image_to_string(img1, lang='eng')
            print("Text is:", plate)
    
        # If drawing Mode - Index fingers is UP
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print('Drawing Mode')
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    # he =img.shape[0]
    # we = img.shape[1]
    # imgInv = cv2.resize(imgInv, (he, we))
    # imgCanvas = cv2.resize(imgCanvas, (he, we))
    # img = cv2.bitwise_and(img, imgInv)
    # img = cv2.bitwise_or(img, imgCanvas)
    img[0:125, 0:1280]= header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
    # img1 = cv2.resize(imgCanvas, (500, 500))
    # plate = pytesseract.image_to_string(img1 )

    # print("Number plate is:", plate)
    cv2.imshow("image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)
    cv2.waitKey(1) 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()     
 

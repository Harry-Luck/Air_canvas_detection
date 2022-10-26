import numpy as np
import cv2
from collections import deque
import pytesseract
# import imutils
# default called trackbar function
def setValues(x):
    print("")


# Creating the trackbars needed for
# adjusting the marker colour These
# trackbars will be used for setting
# the upper and lower ranges of the
# HSV required for particular colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors",
                   89, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors",
                   255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors",
                   255, 180, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors",
                   36, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors",
                   50, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors",
                   70, 180, setValues)

# # Giving different arrays to handle colour
# # points of different colour These arrays
# # will hold the points of a particular colour
# # in the array which will further be used
# # to draw on canvas
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# # These indexes will be used to mark position
# # of pointers in colour array
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# # The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

# # The colours which will be used as ink for
# # the drawing purpose
colors = [(255, 0, 0), (0, 255, 0),
          (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# # Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)

# Keep looping
while True:

    # Reading the frame from the camera
    ret, frame = cap.read()

    # Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    # frame = cv2.imread('4.jpg')
    framedemo = cv2.imread('22.jpg')
    framedemo = cv2.resize(framedemo, (1000, 1000) )
    # cv2.imshow("frae", frame)
    # frame1 = imutils.resize(frame, width=300 )
    # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
    # plate = pytesseract.image_to_string(frame1)
    # print("Number plate is:", plate)


    # frame = imutils.resize(frame, width=300 )
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Getting the updated positions of the trackbar
    # and setting the HSV values
    u_hue = cv2.getTrackbarPos("Upper Hue",
                               "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation",
                                      "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value",
                                 "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue",
                               "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation",
                                      "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value",
                                 "Color detectors")
    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])

    # # Adding the colour buttons to the live frame
    # # for colour access
    frame = cv2.rectangle(frame, (40, 411), (140, 475),
                          (122, 122, 122), -1)
    frame = cv2.rectangle(frame, (160, 411), (255, 475),
                          colors[0], -1)
    frame = cv2.rectangle(frame, (275, 411), (370, 475),
                          colors[1], -1)
    frame = cv2.rectangle(frame, (390, 411), (485, 475),
                          colors[2], -1)
    frame = cv2.rectangle(frame, (505, 411), (600, 475),
                          colors[3], -1)

    cv2.putText(frame, "CLEAR ALL", (49, 445),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "BLUE", (185, 445),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "GREEN", (298, 445),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "RED", (420, 445),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "YELLOW", (520, 445
                                  ),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (150, 150, 150), 2, cv2.LINE_AA)

    # # Identifying the pointer by making its
    # # mask
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # # # Find contours for the pointer after
    # # # idetifying it
    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # # Ifthe contours are formed
    if len(cnts) > 0:

        # sorting the contours to find biggest
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # Get the radius of the enclosing circle
        # around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Now checking if the user wants to click on
        # any button above the screen
        if center[1] <= 475 and center[1] > 411:

            # Clear Button
            if 40 <= center[0] <= 140:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Yellow
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # # Append the next deques when nothing is
    # # detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the
    # canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):

        for j in range(len(points[i])):

            for k in range(1, len(points[i][j])):

                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    # continue
                    # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

                    # plate = pytesseract.image_to_string(frame, lang='eng')
                    # print("ssffefefsf:", plate)
                    print("12312313")
                else:
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(framedemo, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

    frame1 = cv2.resize(frame, (600, 600) )
    plate = pytesseract.image_to_string(frame1)
    print("Number plate is:", plate)
    cv2.imshow("32", framedemo)
    
    
    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask", Mask)

    # If the 'q' key is pressed then stop the application
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()
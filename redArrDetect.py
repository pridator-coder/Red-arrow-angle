import math
import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
frameBrightness = 100
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, frameBrightness)
myColor = [[127,13, 164, 179, 72, 255]] # this is the lower and upper HSV values for the red colour used

# This is a function that returns the gradient of a line segment passing through the two points passed into it
def getGradient(x1, y1, x4, y4):
    grad = (y1-y4)/(x1-x4)
    return grad
# This function gets the angle from x axis
def getAngle(gradient):
    m1 = 0
    m2 = gradient
    angR = math.atan((m2 - m1) / (1 + (m2 * m1)))
    angD = round(math.degrees(angR))
    ang = (90-angD)
    if ang < 0:
        ang+= 360
    return ang

# This function segments the color of the arrow and detects it
def findColor(frame, myColor):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array(myColor[0][0:3])
    upper_red = np.array(myColor[0][3:6])
    mask = cv2.inRange(imgHSV, lower_red, upper_red)
    # cv2.imshow("Mask", mask)
    getContours(mask)

# This function finds the contours of the img passed in it and then draws it on a separate frame
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # pts = approx
            print(approx)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            # print(objCor)
            cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if objCor == 7:
                # if len(approx[0])==2:
                    x1, y1 = approx[0][0]
                    x2, y2 = approx[3][0]
                    x3, y3 = approx[4][0]
                    x4 = ((x2 + x3)/2)
                    y4 = ((y2 + y3)/2)
                    print(x1, y1, x4, y4)
                    gradient = getGradient(x1, y1, x4, y4)
                    angle = getAngle(gradient)

                    cv2.putText(imgResult, str(angle) , (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)


while True:
    success, frame = cap.read()
    imgResult = frame.copy()
    findColor(frame, myColor)
    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

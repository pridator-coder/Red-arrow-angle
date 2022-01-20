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

# This function segments the color of the arrow and detects it
def findColor(frame, myColor):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                   #This changes the color scheme of the frame from the default BGR to HSV.
    lower_red = np.array(myColor[0][0:3])                                             #This is an array containing the three lower ranges of HSV.
    upper_red = np.array(myColor[0][3:6])                                             #This is an array containing the three upper ranges of HSV.
    mask = cv2.inRange(imgHSV, lower_red, upper_red)                                  #Here I have applied a mask which accepts pixels having HSV values in the range of lower and upper parameters passed into it.
    # cv2.imshow("Mask", mask)
    getContours(mask)                                                                 #This is the function call for forming the contours on the mask where we have segmented some range of pixels.



# This is a function that returns the gradient of a line segment passing through the two points passed into it
def getGradient(x1, y1, x4, y4):
    grad = (y1-y4)/(x1-x4)                                                           #This is the formula for calculating slope
    return grad


# This function gets the angle from y axis
def getAngle(gradient):
    m1 = 0
    m2 = gradient
    angR = math.atan((m2 - m1) / (1 + (m2 * m1)))                                    #This is the formula for getting the angle in radians.
    angD = round(math.degrees(angR))
    ang = (90-angD)
    if ang < 0:
        ang+= 180
    return ang

# This function finds the contours of the img passed in it and then draws it on a copy of the frame
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #This function gets the external contours from the image passed into it and stores it into contours.
    for cnt in contours:
        area = cv2.contourArea(cnt)                                                       #This is a function to calculate the area.
        # print(area)
        peri = cv2.arcLength(cnt, True)                                                   #This finds the length of contour
        # print(peri)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)                                 #This approx the shape it finds to another shape based on the precision value
        # pts = approx
        print(approx)
        objCor = len(approx)                                                              #This finds the length of the approx list, i.e. how many values or corner points it has
        if objCor == 7:
            if area > 3000:
                cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)                      #This draws the contours on the image passed into it, color and thickness values are also specified

                x, y, w, h = cv2.boundingRect(approx)
                # print(objCor)
                cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # if objCor == 7:
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

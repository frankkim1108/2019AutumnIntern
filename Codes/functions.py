import cv2
import math
import numpy as np

def maxAreaContour(imgray):
    ret, thr = cv2.threshold(imgray, 10, 255, 0)
    contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    maxContour = 0
    areaFrontSize = 0
    for cnt in contours:
        areaContours = cv2.contourArea(cnt)
        if areaContours > areaFrontSize:
            areaFrontSize = areaContours
            maxContour = cnt

    return maxContour

def findExtremePoints(contour, imgHeight):
    topMostY = imgHeight
    bottomMostY = 0
    for i in contour:
        if i[0][1] > bottomMostY:
            bottomMostY = i[0][1]
        if i[0][1] < topMostY:
            topMostY = i[0][1]

    return (bottomMostY, topMostY)

def ellipseCircumference(a, b):
    return 2*math.atan(1)*4*math.sqrt((math.pow(a, 2)+math.pow(b, 2))/2)

def pointLength(x,y):
    # length between two points
    return math.sqrt(math.pow(x[0]-y[0], 2)+math.pow(x[1]-y[1], 2))

def pixelHeightCal(length, topY, bottomY):
    return float(length) / (bottomY-topY)

def addGreen(img):
    LUT = []
    for i in range(256):
        LUT.append(i + 1)

    LUT = np.array(LUT, dtype=np.uint8)
    img[:, :, 1] = LUT[img[:, :, 1]]
    return img
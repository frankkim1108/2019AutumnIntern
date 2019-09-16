# import official lib
import cv2
import json
from copy import copy
# import py file in folder
import functions
import grith_waist
import length_back
import grith_chest
import grith_heap
import grith_thigh
import grith_shoulder
import finalfront
import finalside

# from venv import functions


def findPointArr(read_dir, fileName):
    with open(read_dir + fileName, 'r') as f:
        json_data = json.load(f)

    temp = 0
    points = [[]]
    listTemp = []
    for i in json_data["people"][0]["pose_keypoints_2d"]:
        listTemp.append(int(i))
        temp += 1
        if temp is 3:
            points.append(copy(listTemp))
            listTemp.pop()
            listTemp.pop()
            listTemp.pop()
            temp = 0
    del points[0]
    return points

def main():

    newfrontImg = cv2.imread('image/newestfront.jpg')
    finalfront.getfrontcoord(newfrontImg)
    newsideImg = cv2.imread('image/newestside.jpg')
    finalside.getfrontcoord(newsideImg)
    read_dir = './json/'
    frontJson = 'finalfront.json'  # json file of front picture analysis
    sideJson = 'finalside.json'  # json file of front picture analysis
    write_dir = './json/'
    fileName3 = 'result.json'  # json file of result

    # open front, side json & save points
    frontPoint = findPointArr(read_dir, frontJson)
    sidePoint = findPointArr(read_dir, sideJson)

    # image processing
    frontImg = cv2.imread('image/realfinalfront.png', cv2.IMREAD_COLOR)
    frontImgray = cv2.cvtColor(frontImg, cv2.COLOR_BGR2GRAY)
    frontContour = functions.maxAreaContour(frontImgray)

    sideImg = cv2.imread('image/realfinalside.png', cv2.IMREAD_COLOR)
    sideImgray = cv2.cvtColor(sideImg, cv2.COLOR_BGR2GRAY)
    sideContour = functions.maxAreaContour(sideImgray)

    # find human's max y & min y in front, side img
    frontImgWidth , frontImgHeight, _ = frontImg.shape
    sideImgWidth, sideImgHeight, _ = sideImg.shape

    (frontBottomMost, frontTopMost) = functions.findExtremePoints(frontContour, frontImgHeight)
    (sideBottomMost, sideTopMost) = functions.findExtremePoints(sideContour, sideImgHeight)

    # calculate 1pixel : 1cm ratio
    human_height = 165  # this value is random number, it must be input by user
    rate = functions.pixelHeightCal(human_height, frontTopMost, frontBottomMost)

    frontImg = functions.addGreen(frontImg)
    sideImg = functions.addGreen(sideImg)

    cv2.drawContours(frontImg, frontContour, -1, (0, 255, 0), 1)
    cv2.drawContours(sideImg, sideContour, -1, (0, 255, 0), 1)
    im = cv2.resize(frontImg, (800, 1000))
    im2 = cv2.resize(sideImg, (800, 1000))
    # cv2.imshow("checking_front",im)
    # cv2.imshow("chekcing_side", im2)
    # cv2.waitKey(0)
    # point Number information
    # point0 = NOSE                 point1 = CHEST
    # point2 = RIGHT SHOULDER       point3 = RIGHT ARM
    # point4 = RIGHT WRIST          point5 = LEFT SHOULDER
    # point6 = LEFT ARM             point7 = LEFT WRIST
    # point8 = WAIST(PELVIS)        point9 = RIGHT WAIST
    # point10 = RIGHT KNEE          point11 = RIGHT ANKLE
    # point12 = LEFT WAIST          point13 = LEFT KNEE
    # point14 = LEFT ANKLE
    chestPoint_F = frontPoint[1]
    rightShoulderPoint_F = frontPoint[2]
    leftShoulderPoint_F = frontPoint[5]
    waistPoint_F = frontPoint[8]
    rightWaistPoint_F = frontPoint[9]
    rightKneePoint_F = frontPoint[10]

    chestPoint_S = sidePoint[1]
    leftShoulderPoint_S = sidePoint[5]

    # measure functions
    waist = grith_waist.main(frontImg, frontBottomMost, frontTopMost, sideImg, sideBottomMost,
                                         sideTopMost, chestPoint_F, waistPoint_F, chestPoint_S)

    chest = grith_chest.main(frontBottomMost, frontTopMost, frontImg, sideImg, sideBottomMost, sideTopMost,
                                       rightShoulderPoint_F, leftShoulderPoint_F, chestPoint_S, waistPoint_F)
    heap = grith_heap.main(frontImg, frontBottomMost, frontTopMost, sideImg, sideBottomMost, sideTopMost,
                                waistPoint_F)
    shoulder = grith_shoulder.main(frontImg, frontBottomMost, frontTopMost, sideImg, sideBottomMost,
                                                       sideTopMost, leftShoulderPoint_F, rightShoulderPoint_F, leftShoulderPoint_S)
    back = length_back.main(chestPoint_F, waistPoint_F, frontImg)
    thigh = grith_thigh.main(frontImg, frontBottomMost, frontTopMost, sideImg, sideBottomMost,
                                     sideTopMost, waistPoint_F, rightWaistPoint_F, rightKneePoint_F)

    #'shoulderLength': shoulderLength * rate
    # make json output file
    sizeGroup = dict()
    sizeGroup["chest"] = str(chest * rate)
    sizeGroup["waist"] = str(waist * rate)
    sizeGroup["heap"] = str(heap * rate)
    sizeGroup["shoulder Grith"] = str(shoulder*rate)
    sizeGroup["back"] = str(back*rate)
    sizeGroup["thigh"] = str(thigh*rate)

    with open(write_dir + fileName3, 'w') as outfile:
        json.dump(sizeGroup, outfile)

    print(json.dumps(sizeGroup) )


main()
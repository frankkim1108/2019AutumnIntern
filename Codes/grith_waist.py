import functions
import cv2


def main(frontImg, frontBottomY, frontTopY, sideImg, sideBottomY, sideTopY, frontChest, frontPelvis, sideChest):
    # front waist point
    waistFront = [(frontChest[0] + frontPelvis[0]) / 2, (frontPelvis[1] * 240 + frontChest[1] * 50) / 290]
    waistFront[0] = int(waistFront[0])
    waistFront[1] = int(waistFront[1])
    # side waist point
    waistSide = [0, 0]
    waistSide[0] = int(sideChest[0])
    waistSide[1] = int((sideTopY-sideBottomY)*(waistFront[1]-frontTopY)/(frontTopY-frontBottomY)+sideTopY)

    # front waist right & left search
    # move(right,left) from waist point to contour
    waistFrontRight = [waistFront[0], waistFront[1]]
    while not(frontImg[waistFrontRight[1], waistFrontRight[0], 0] == 0 and
              frontImg[waistFrontRight[1], waistFrontRight[0], 1] == 255 and frontImg[waistFrontRight[1], waistFrontRight[0], 2] == 0):
        waistFrontRight[0] += 1

    waistFrontLeft = [waistFront[0],waistFront[1]]
    while not(frontImg[waistFrontLeft[1], waistFrontLeft[0], 0] == 0 and
              frontImg[waistFrontLeft[1], waistFrontLeft[0], 1] == 255 and frontImg[waistFrontLeft[1], waistFrontLeft[0], 2] == 0):
        waistFrontLeft[0] -= 1

    # cv2.circle(frontImg, (waistFrontRight[0], waistFrontRight[1]), 10, (0, 255, 255), -1)
    # cv2.circle(frontImg, (waistFrontLeft[0], waistFrontLeft[1]), 10, (255, 255, 255), -1)

    # side waist right & left search
    # move(right,left) from waist point to contour
    waistSideRight = [waistSide[0], waistSide[1]]
    while not(sideImg[waistSideRight[1], waistSideRight[0], 0] == 0 and
              sideImg[waistSideRight[1], waistSideRight[0], 1] == 255 and sideImg[waistSideRight[1], waistSideRight[0], 2] == 0):
        waistSideRight[0] += 1

    waistSideLeft = [waistSide[0], waistSide[1]]
    while not(sideImg[waistSideLeft[1],waistSideLeft[0],0] == 0 and
              sideImg[waistSideLeft[1],waistSideLeft[0],1] == 255 and sideImg[waistSideLeft[1],waistSideLeft[0],2] == 0):
        waistSideLeft[0] -= 1

    return functions.ellipseCircumference((waistFrontRight[0] - waistFrontLeft[0]) / 2, (waistSideRight[0] - waistSideLeft[0]) / 2)
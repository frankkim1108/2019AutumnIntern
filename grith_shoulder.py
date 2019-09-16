import functions
import cv2

def main(frontImg, frontBottomY, frontTopY, sideImg, sideBottomY, sideTopY, frontLeftShoulder, frontRightShoulder, sideShoulder):
    # left shoulder search
    # move from shoulder point to left by shoulder point to top contour
    frontLeftShoulder = [int(frontLeftShoulder[0]), int(frontLeftShoulder[1])]
    mvTemp = 0
    while not(frontImg[frontLeftShoulder[1]-mvTemp, frontLeftShoulder[0], 0] == 0 and
              frontImg[frontLeftShoulder[1]-mvTemp, frontLeftShoulder[0], 1] == 255 and
              frontImg[frontLeftShoulder[1]-mvTemp, frontLeftShoulder[0], 2] == 0):
        mvTemp += 1
    frontLeftShoulder[0] -= mvTemp

    # right shoulder search
    # same right
    frontRightShoulder = [int(frontRightShoulder[0]), int(frontRightShoulder[1])]
    mvTemp = 0
    while not(frontImg[frontRightShoulder[1]-mvTemp, frontRightShoulder[0], 0] == 0 and
              frontImg[frontRightShoulder[1]-mvTemp, frontRightShoulder[0], 1] == 255 and
              frontImg[frontRightShoulder[1]-mvTemp, frontRightShoulder[0], 2] == 0):
        mvTemp += 1
    frontRightShoulder[0] += mvTemp

    cv2.circle(frontImg, (frontRightShoulder[0], frontRightShoulder[1]), 1, (255,255,255), -1)
    cv2.circle(frontImg, (frontRightShoulder[0], frontRightShoulder[1]), 1, (255, 255, 255), -1)

    # side shoulder search
    sideShoulder = [int(sideShoulder[0]), int((sideTopY-sideBottomY)*(frontRightShoulder[1]-frontTopY)/(frontTopY-frontBottomY)+sideTopY)]

    sideRightShoulder = [sideShoulder[0], sideShoulder[1]]
    while not(sideImg[sideRightShoulder[1], sideRightShoulder[0], 0] == 0 and
              sideImg[sideRightShoulder[1], sideRightShoulder[0], 1] == 255 and sideImg[sideRightShoulder[1], sideRightShoulder[0], 2] == 0):
        sideRightShoulder[0] += 1

    sideLeftShoulder = [sideShoulder[0], sideShoulder[1]]
    while not(sideImg[sideLeftShoulder[1], sideLeftShoulder[0], 0] == 0 and
              sideImg[sideLeftShoulder[1], sideLeftShoulder[0], 1] == 255 and sideImg[sideLeftShoulder[1], sideLeftShoulder[0], 2] == 0):
        sideLeftShoulder[0] -= 1

    return functions.ellipseCircumference((frontRightShoulder[0] - frontLeftShoulder[0]) / 2, (sideRightShoulder[0] - sideLeftShoulder[0]) / 2)
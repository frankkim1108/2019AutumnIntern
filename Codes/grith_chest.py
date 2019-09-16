import functions
import cv2

def main(frontBottomY, frontTopY, frontImg, sideImg, sideBottomY, sideTopY, rightShoulder_f, leftShoulder, rightShoulder_l, waist):
    # sideChest = [0, 0]
    # sideChest[1] = int((sideTopY - sideBottomY) * (rightShoulder_f[1] - frontTopY) / (frontTopY - frontBottomY) + sideTopY)

    ratio = (float(leftShoulder[1] - frontTopY) / float(frontBottomY - frontTopY))
    sideChest = sideTopY + ((sideBottomY - sideTopY) * ratio)
    sideChest = [int(sideChest), int(sideChest)]

    ratio = (float(waist[1] - frontTopY) / float(frontBottomY - frontTopY))
    side_waist = sideTopY + ((sideBottomY - sideTopY) * ratio)
    side_waist = [int(side_waist), int(side_waist)]
    # cv2.circle(sideImg, (rightShoulder_l[0], rightShoulder_l[1]), 5, (255, 255, 255), -1)
    # cv2.circle(sideImg, (sideChest[0],sideChest[1]),5,(255,255,255),-1)
    # cv2.circle(sideImg, (rightShoulder_f[0], rightShoulder_f[1]), 5, (255, 255, 255), -1)

    newPoint = [0, int((sideChest[1]*4+side_waist[1]*1)/5)]

    sideLeftChest = [0, newPoint[1]]
    while not(sideImg[sideLeftChest[1], sideLeftChest[0], 0] == 0 and
              sideImg[sideLeftChest[1], sideLeftChest[0], 1] == 255 and sideImg[sideLeftChest[1], sideLeftChest[0], 2] == 0):
        sideLeftChest[0] = sideLeftChest[0]+1

    sideRightChest = [sideLeftChest[0] + 3, newPoint[1]]
    cv2.waitKey(0)
    while not(sideImg[sideRightChest[1], sideRightChest[0], 0] == 0 and
              sideImg[sideRightChest[1], sideRightChest[0], 1] == 255 and sideImg[sideRightChest[1], sideRightChest[0], 2] == 0):
        sideRightChest[0] = sideRightChest[0] + 1

    # draw etc(line & point)
    cv2.line(frontImg, (leftShoulder[0], leftShoulder[1]), (rightShoulder_f[0], rightShoulder_f[1]), (255, 0, 0), 3)
    cv2.line(sideImg, (sideRightChest[0], sideRightChest[1]), (sideLeftChest[0], sideLeftChest[1]), (255, 0, 0), 3)
    im = cv2.resize(frontImg, (800, 1000))
    im2 = cv2.resize(sideImg, (800, 1000))
    # cv2.imshow("front", im)
    # cv2.imshow("side", im2)
    # cv2.waitKey(0)
    return functions.ellipseCircumference((leftShoulder[0] - rightShoulder_f[0])/2, (sideRightChest[0] - sideLeftChest[0])/2)
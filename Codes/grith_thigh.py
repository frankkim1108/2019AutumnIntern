import functions
import cv2

def main(frontImg, frontBottomY, frontTopY, sideImg, sideBottomY, sideTopY, waist, rightWaist, rightKnee):
    # find picture width(channel don't be used)
    _, width, channel = frontImg.shape

    # new point relation with point9(RIGHT WAIST) & point10(RIGHT KNEE)
    newPoint = [0, int((rightWaist[1]+rightKnee[1]+rightKnee[1]+rightKnee[1])/4)]

    # find thigh legnth in front picture

    waist_temp1 = [0, newPoint[1]]
    while not (frontImg[waist_temp1[1], waist_temp1[0], 0] == 0 and
               frontImg[waist_temp1[1], waist_temp1[0], 1] == 255 and frontImg[waist_temp1[1], waist_temp1[0], 2] == 0):
        waist_temp1[0] = waist_temp1[0] + 1

    waist_temp2 = [waist_temp1[0] + 3, waist_temp1[1]]
    while not (frontImg[waist_temp2[1], waist_temp2[0], 0] == 0 and
               frontImg[waist_temp2[1], waist_temp2[0], 1] == 255 and frontImg[waist_temp2[1], waist_temp2[0], 2] == 0):
        waist_temp2[0] = waist_temp2[0] + 1

    # first, second = [0, newPoint[1]], [0, newPoint[1]]
    # first_check, second_check = False, False
    # for i in range(waist[0]):
    #     if frontImg[newPoint[1], i][1] == 255:
    #         if not first_check:
    #             first[0] = i
    #             first_check = True
    #         elif not second_check:
    #             second[0] = i
    #             second_check = True
    #     elif i is waist[0]:
    #         if not second_check:
    #             second[0] = i
    #             second_check = True

    front_length = waist_temp1[0] - waist_temp2[0]

    # find human top most & bottom most in front legnth
    ratio = (float(newPoint[1] - frontTopY) / float(frontBottomY - frontTopY))

    # new point in side picture
    newPoint_ratio = sideTopY + ((sideBottomY - sideTopY) *ratio)
    newPoint_ratio = [int(newPoint_ratio), int(newPoint_ratio)]

    # find picture width(channel don't be used)
    _, width, channel = sideImg.shape

    # find thigh legnth in side picture
    waist_result = [int(sideBottomY), int(newPoint_ratio[1])]

    waist_temp3 = [0, waist_result[1]]
    while not (sideImg[waist_temp3[1], waist_temp3[0], 0] == 0 and
               sideImg[waist_temp3[1], waist_temp3[0], 1] == 255 and sideImg[waist_temp3[1], waist_temp3[0], 2] == 0):
        waist_temp3[0] = waist_temp3[0] + 1

    waist_temp4 = [waist_temp3[0] + 3, waist_temp3[1]]
    while not (sideImg[waist_temp4[1], waist_temp4[0], 0] == 0 and
               sideImg[waist_temp4[1], waist_temp4[0], 1] == 255 and sideImg[waist_temp4[1], waist_temp4[0], 2] == 0):
        waist_temp4[0] = waist_temp4[0] + 1

    side_length = waist_temp4[0] - waist_temp3[0]

    rightThighLength = functions.ellipseCircumference(front_length / 2, side_length / 2)
    return rightThighLength
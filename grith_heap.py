import functions
import cv2

def main(frontImg, frontBottomY, frontTopY, sideImg, sideBottomY, sideTopY,  waist):
    # find picture width(channel don't be used)
    _, width, channel = frontImg.shape

    # find heap legnth in front picture
    waist_temp1 = [0, waist[1]]
    while not(frontImg[waist_temp1[1], waist_temp1[0], 0] == 0 and
              frontImg[waist_temp1[1], waist_temp1[0], 1] == 255 and frontImg[waist_temp1[1], waist_temp1[0], 2] == 0):
        waist_temp1[0] = waist_temp1[0]+1

    waist_temp2 = [waist_temp1[0] + 3, waist_temp1[1]]
    while not (frontImg[waist_temp2[1], waist_temp2[0], 0] == 0 and
               frontImg[waist_temp2[1], waist_temp2[0], 1] == 255 and frontImg[waist_temp2[1], waist_temp2[0], 2] == 0):
        waist_temp2[0] = waist_temp2[0] + 1

    front_length = waist_temp2[0] - waist_temp1[0]

    ### side picture ###
    ratio = (float(waist[1] - frontTopY) / float(frontBottomY - frontTopY))
    waist_result = sideTopY + (sideBottomY - sideTopY) * ratio

    waist_result = [int(sideBottomY), int(waist_result)]

    waist_temp3 = [0, waist_result[1]]
    while not (sideImg[waist_temp3[1], waist_temp3[0], 0] == 0 and
               sideImg[waist_temp3[1], waist_temp3[0], 1] == 255 and sideImg[waist_temp3[1], waist_temp3[0], 2] == 0):
        waist_temp3[0] = waist_temp3[0] + 1

    waist_temp4 = [waist_temp3[0] + 3, waist_temp3[1]]
    while not (sideImg[waist_temp4[1], waist_temp4[0], 0] == 0 and
               sideImg[waist_temp4[1], waist_temp4[0], 1] == 255 and sideImg[waist_temp4[1], waist_temp4[0], 2] == 0):
        waist_temp4[0] = waist_temp4[0] + 1

    side_length = waist_temp4[0] - waist_temp3[0]

    # calculate heap_grith
    heap_grith = functions.ellipseCircumference(front_length / 2, side_length / 2)

    return heap_grith

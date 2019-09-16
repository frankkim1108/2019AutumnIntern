# From Python
# It requires OpenCV installed for Python
import os
import sys
import cv2
import json
import argparse
import numpy as np
from sys import platform
#from matplotlib import pyplot as plt
from enum import Enum


def getfrontcoord(imgside):

    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('/usr/local/python')
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    basePath = "/home/ele/openpose/"  # openpose git folder location
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default=basePath + "examples/media/COCO_val2014_000000000192.jpg",
                        help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = basePath + "models"
    params["write_json"] = "./json/"  # result to json file

    try:
        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imgName = imgside
        ori = imgName
        print(ori.shape)
        row, col, _ = ori.shape
        img_size = ori.shape[1]
        img_size = 1000
        ori = cv2.resize(ori, dsize=(img_size, int(img_size * row / col)))
        print(ori.shape)
        # ori = cv2.GaussianBlur(ori, (9, 9), 0)
        datum.cvInputData = ori
        opWrapper.emplaceAndPop([datum])
    except Exception as e:
        # print(e)
        sys.exit(-1)

    # openpose process complete

    final = ori
    op_res = datum.cvOutputData
    row, col, _ = ori.shape
    mask = np.zeros(ori.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Step 1
    with open('./json/0_keypoints.json') as data_file:
        res_json = json.load(data_file)

    with open('../humanmeasurement/json/' + "finalside" + '.json', 'w') as outfile:
        json.dump(res_json, outfile)

    # select person which has maximum poseScore
    max = 0
    max_i = 0
    for i in range(len(datum.poseScores)):
        if datum.poseScores[i] > max:
            max = datum.poseScores[i]
            max_i = i

    main_pose = res_json["people"][max_i]["pose_keypoints_2d"]

    # make rectangle so it include entire body... (x_pad and y_pad calculated experimentally)
    max_y = 0
    min_y = 10000
    max_x = 0
    min_x = 10000
    is_zero_component = False
    for i in range(len(main_pose) // 3):
        main_pose[3 * i] = int(main_pose[3 * i])
        main_pose[3 * i + 1] = int(main_pose[3 * i + 1])
        x = int(main_pose[3 * i])
        y = int(main_pose[3 * i + 1])
        if x == 0 or y == 0:
            is_zero_component = True

        if y > max_y:
            max_y = y
        if 0 < y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if 0 < x < min_x:
            min_x = x

    y_pad = (max_y - min_y) // 9
    x_pad = (max_x - min_x) // 3

    max_y = max_y + y_pad // 2
    min_y = min_y - y_pad
    max_x = max_x + x_pad
    min_x = min_x - x_pad

    # marking probably foregoround.... use openpose skeleton -> this marking is experimental
    # if marking work incorretly, marking algorithm should be modified

    Body = {'nose': 0, 'chest': 2, 'left sholder': 4, 'left arm': 6, 'left wrist': 8, 'right sholder': 10,
            'right arm': 12,
            'right wrist': 14,
            'center plevis': 16, 'left pelvis': 18, 'left knee': 20, 'left foot': 22, 'right pelvis': 24,
            'right knee': 26,
            'right foot': 28, }

    tmp_img = op_res.copy()
    cv2.circle(tmp_img, (main_pose[0], main_pose[1] - y_pad // 4), radius=y_pad, color=(255, 255, 255), thickness=-1)
    cv2.rectangle(tmp_img, (main_pose[6] - x_pad, main_pose[7] - y_pad),
                  (main_pose[15] + x_pad, main_pose[43] + y_pad * 2), color=(255, 255, 255), thickness=-1)
    cv2.line(tmp_img, (main_pose[6], main_pose[7]), (main_pose[9], main_pose[10]), color=(255, 255, 255),
             thickness=x_pad)
    cv2.line(tmp_img, (main_pose[15], main_pose[16]), (main_pose[18], main_pose[19]), color=(255, 255, 255),
             thickness=x_pad)
    cv2.line(tmp_img, (main_pose[9], main_pose[10]), (main_pose[12], main_pose[13]), color=(255, 255, 255),
             thickness=x_pad)
    cv2.line(tmp_img, (main_pose[18], main_pose[19]), (main_pose[21], main_pose[22]), color=(255, 255, 255),
             thickness=x_pad)

    cv2.line(op_res, (main_pose[6], main_pose[7]), (main_pose[27], main_pose[28]), color=(255, 255, 255), thickness=5)
    cv2.line(op_res, (main_pose[15], main_pose[16]), (main_pose[36], main_pose[37]), color=(255, 255, 255), thickness=5)

    cv2.line(op_res, (main_pose[6], main_pose[7]), (main_pose[24], main_pose[25]), color=(255, 255, 255), thickness=5)
    cv2.line(op_res, (main_pose[15], main_pose[16]), (main_pose[24], main_pose[25]), color=(255, 255, 255), thickness=5)

    # apply grabcut with rectangle
    rect_img = final.copy()
    cv2.rectangle(rect_img, (min_x, min_y), (max_x, max_y), (0, 0, 255), thickness=10)
    rect = (min_y, min_x, max_y, max_x)
    cv2.grabCut(final, mask, rect, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    rect_res = final
    rect_res = rect_res * mask2[:, :, np.newaxis]

    for i in range(0, row):
        for j in range(0, col):
            if i < min_y or i > max_y or j < min_x or j > max_x:
                mask[i][j] = 0
            elif np.array_equal(ori[i][j], op_res[i][j]):
                mask[i][j] = 2  # probably foreground
            else:
                mask[i][j] = 1  # foreground

    if not is_zero_component:
        for i in range(0, row):
            for j in range(0, col):
                if i < min_y or i > max_y or j < min_x or j > max_x:
                    mask[i][j] = 0
                elif not np.array_equal(ori[i][j], op_res[i][j]):
                    mask[i][j] = 1
                elif np.array_equal(tmp_img[i][j], (255, 255, 255)):
                    mask[i][j] = 2
                else:
                    mask[i][j] = 0

    # apply grabcut with mask
    cv2.grabCut(final, mask, None, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    final = final * mask2[:, :, np.newaxis]

    cv2.imwrite("./image/" + "realfinalside.png", final)
    cv2.imwrite("./image/" + "boneside.png", op_res)






# view results...
# res = ori.copy()
# for i in range(0, row):
#     for j in range(0, col):
#         if np.array_equal(ori[i][j], op_res[i][j]):
#             res[i][j] = [0, 0, 0]
#         else:
#             res[i][j] = [255, 255, 255]
#
# images = [ori, op_res, res, rect_img, rect_res, final]
# titles = ["ori", "op_res","res", "rect_ing", "rect_res", "final"]
#
# for i in range(0, len(images)):
#     plt.subplot(2, 3, i + 1)
#     plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
#     plt.title(titles[i])
#     plt.xticks([])
#     plt.yticks([])
#
# plt.show()

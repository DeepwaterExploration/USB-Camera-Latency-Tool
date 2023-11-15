'''
USB Camera Latency Testing Utility

Description:
    This utility is designed for testing USB camera latency.

Notes:
    - Ensure that the testing is performed on monitors with high refresh rates.
    - Our testing refresh rate is set between 120Hz and 165Hz
    - Lower refresh rates may result in capped measured latency, typically
      capping out around 100ms.
    - We test using MJPEG mode

Author: DeepWater Exploration

Version: 1.0
'''

import cv2
import numpy as np

# -- General Parameters --
# Threshold for camera to detect black/white
BW_THRESHOLD = 60 # Range: 0 -> 255
WIN_SHAPE = (1500, 1500)
blackFrame = np.full(WIN_SHAPE, 0, dtype=np.uint8)
whiteFrame = np.full(WIN_SHAPE, 255, dtype=np.uint8)
WIN_COLOR = { True: whiteFrame, False: blackFrame }


# -- Camera Parameters --
# Camera Index
CAM_IDX = 0
# resolution
WIDTH = 1920
HEIGHT = 1080
MJPG = cv2.VideoWriter_fourcc(*'MJPG')

# -- DEVICE SETUP --
exploreHD = cv2.VideoCapture(CAM_IDX)

# set to MJPEG mode, by default, idx 0 is YUYV
# MJPG needs to be set, before resolution. Pixel format is always selected first
exploreHD.set(cv2.CAP_PROP_FOURCC, MJPG)

exploreHD.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
exploreHD.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# Disable auto exposure
exploreHD.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
exploreHD.set(cv2.CAP_PROP_EXPOSURE, 90)

actual_video_width = exploreHD.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_video_height = exploreHD.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('actual video resolution:{:.0f}x{:.0f}'.format(actual_video_width, actual_video_height))


# Error Check
if ((exploreHD == None) or (not exploreHD.isOpened())):
    print('\nError - could not open video device.\n')
    exit(0)

prevTickCount = cv2.getTickCount()
currFrame, prevFrame = 0, 0
prevBlack = True


while True:
    currFrame += 1

    _, frame = exploreHD.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    currBlack = np.average(img) < BW_THRESHOLD

    if prevBlack != currBlack:
        currTickCount = cv2.getTickCount()

        # {:.3f} - floating-point formatted to three digits after decimal
        print("{:.3f} sec, {:.3f} frames".format(
            ((currTickCount - prevTickCount) / cv2.getTickFrequency()),
            (currFrame - prevFrame)
        ), end='\r')
        
        # update values
        prevBlack = currBlack
        prevTickCount = currTickCount
        prevFrame = currFrame
        
        cv2.imshow('Black/White Latency Testing Window', WIN_COLOR[prevBlack])

    # press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

exploreHD.release()
cv2.destroyAllWindows()
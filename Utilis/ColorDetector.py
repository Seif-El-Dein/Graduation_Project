import cv2
import numpy as np


def DetectLaneColor(Frame):

    FrameHSV = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
    LowerWhite = np.array([0, 0, 125])
    UpperWhite = np.array([172, 111, 255])

    Mask = cv2.inRange(FrameHSV, LowerWhite, UpperWhite)

    return Mask
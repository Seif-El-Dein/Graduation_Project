import cv2
import numpy as np


def Warp(Frame, Points, Height, Width, inverse = False):

    points1 = np.float32(Points)
    points2 = np.float32([[0, 0], [Width, 0], [0, Height], [Width, Height]])

    if inverse:

        WarpMatrix = cv2.getPerspectiveTransform(points2, points1)

    else:

        WarpMatrix = cv2.getPerspectiveTransform(points1, points2)

    WarpedFrame = cv2.warpPerspective(Frame, WarpMatrix, (Width, Height))

    return WarpedFrame
import cv2
import numpy as np

def Nothing(x):
    pass


def InitializeEditor(initialTrackbarValues, widthTarget = 480, heightTarget = 240):

    cv2.namedWindow("Editor")
    cv2.resizeWindow("Editor", 360, 240)

    cv2.createTrackbar("Width Top", "Editor", initialTrackbarValues[0], widthTarget//2, Nothing)
    cv2.createTrackbar("Height Top", "Editor", initialTrackbarValues[1], heightTarget, Nothing)
    cv2.createTrackbar("Width Bottom", "Editor", initialTrackbarValues[2], widthTarget//2, Nothing)
    cv2.createTrackbar("Height Bottom", "Editor", initialTrackbarValues[3], heightTarget, Nothing)


def InitialEditorVals(widthTarget = 480, heightTarget = 240):

    widthTop = cv2.getTrackbarPos("Width Top", "Editor")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Editor")
    heightTop = cv2.getTrackbarPos("Height Top", "Editor")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Editor")

    Points = np.float32([(widthTop, heightTop), (widthTarget-widthTop, heightTop), (widthBottom, heightBottom),
                         (widthTarget-widthBottom, heightBottom)])

    return Points


def DrawPoints(Frame, Points):

    for x in range(0, 4):

        cv2.circle(Frame, (int(Points[x][0]), int(Points[x][1])), 15, (0, 0, 255), cv2.FILLED)

    return Frame
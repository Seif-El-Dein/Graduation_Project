import cv2
import numpy as np
from Utilis import ColorDetector as CD
from Utilis import FrameWarp as FW
from Utilis import TrackBars as T
from Utilis import FindCurve as FC
from Utilis import StackingSimulation as SS


###################### Warp Initialization #####################
EditorValues = [102, 80, 20, 214]
T.InitializeEditor(EditorValues)
################################################################

avgVal = 10
CurveList = []


def Getlane(Frame, Display = False):

    FrameCopy = Frame.copy()
    imgResult = Frame.copy()
    Lane = CD.DetectLaneColor(Frame)

    Height, Width, Channels = Frame.shape
    Points = T.InitialEditorVals()

    WarpedLane = FW.Warp(Lane, Points, Height, Width)
    WarpingPoints = T.DrawPoints(FrameCopy, Points)

    CenterPoint, HistoFrame = FC.GetHistogram(WarpedLane, Display=True, Ratio=0.5, Region=4)
    CurveAveragePoint, HistoFrame = FC.GetHistogram(WarpedLane, Display=True, Ratio=0.9)
    Curve = CurveAveragePoint - CenterPoint

    CurveList.append(Curve)

    if len(CurveList) > avgVal:

        CurveList.pop(0)

    Curve = int(sum(CurveList) / len(CurveList))

    if Display != 0:
        imgInvWarp = FW.Warp(WarpedLane, Points, Height, Width, inverse=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:Height // 3, 0:Width] = 0, 0, 0
        imgLaneColor = np.zeros_like(Frame)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(Curve), (Width // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (Width // 2, midY), (Width // 2 + (Curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((Width // 2 + (Curve * 3)), midY - 25), (Width // 2 + (Curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = Width // 20
            cv2.line(imgResult, (w * x + int(Curve // 50), midY - 10),
                     (w * x + int(Curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if Display == True:
        VideoStacked = SS.stack(0.5, ([Frame, WarpingPoints, WarpedLane],
                                             [HistoFrame, imgLaneColor, imgResult]))
        cv2.imshow('Simulation', VideoStacked)



    Curve = Curve / 100

    if Curve > 1:
        Curve = 1

    elif Curve < -1:
        Curve = -1

    return Curve

if __name__ == '__main__':

    Capture = cv2.VideoCapture('/home/pi/Desktop/ARG-Robot/Resources/Dataset.mp4')

    FrameCounter = 0

    while True:

        FrameCounter +=1

        if Capture.get(cv2.CAP_PROP_FRAME_COUNT) == FrameCounter:  # To repeat video looping.

            Capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            FrameCounter = 0

        success, Frame = Capture.read()
        Frame = cv2.resize(Frame, (480, 240))
        Curve = Getlane(Frame, Display= True)

        if cv2.waitKey(5) == ord('x'):
            break
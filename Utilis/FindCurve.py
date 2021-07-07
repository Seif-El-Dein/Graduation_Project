import numpy as np
import cv2

def GetHistogram(Frame, Ratio = 0.1, Display = False, Region = 1):

    if Region == 1:

        HistoVals = np.sum(Frame, axis=0)     # we sum the columns in our frame.

    else:

        HistoVals = np.sum(Frame[Frame.shape[0] // Region:, :], axis=0)


    #print(HistoVals)
    MaxHistoVals = np.max(HistoVals)
    #print(MaxHistoVals)
    MinHistoVals = Ratio * MaxHistoVals
    IndexArray = np.where(HistoVals >= MinHistoVals)
    BasePoint = int(np.average(IndexArray))
    #print(BasePoint)

    if Display:

        HistoFrame = np.zeros((Frame.shape[0], Frame.shape[1], 3), np.uint8)

        for x, Intensity in enumerate(HistoVals):

            cv2.line(HistoFrame,(x, Frame.shape[0]), (x, Frame.shape[0] - Intensity // (255 * Region)), (255, 0, 0), 1)
            cv2.circle(HistoFrame, (BasePoint, Frame.shape[0]), 20, (0, 255, 255), cv2.FILLED)

        return BasePoint, HistoFrame

    return BasePoint
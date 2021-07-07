import cv2


class Camera():    # Width instruction code, Height instruction code, WidthFrame, HeightFrame = 3, 4, 1280, 960

    def __init__(self, Width_instruction_code, Height_instruction_code, WidthFrame, HeightFrame):

        self.Capture = cv2.VideoCapture(0)
        self.Width_instruction_code = Width_instruction_code
        self.Height_instruction_code = Height_instruction_code
        self.WidthFrame = WidthFrame
        self.HeightFrame = HeightFrame
        self.Capture.set(self.Width_instruction_code, self.WidthFrame)
        self.Capture.set(self.Height_instruction_code, self.HeightFrame)

    def OpenCam(self, Display = False):

        Success, Frame = self.Capture.read()

        if Display:

            cv2.imshow("ARG Robot", Frame)

        return Frame
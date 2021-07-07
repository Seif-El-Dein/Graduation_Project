#!/usr/bin/python3

from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
from PIL import ImageTk, Image
import cv2
import time
from IoT import DHT22_Module
from IoT import CO2_Module
from IoT import LDR_Module
from Modules import Motors_Module as MM
from IoT import MoistureSensor_Module as MS
import Main_functions as MF
import threading

class App():

    def __init__(self, app, Run):

        self.app = app
        self.Run = True
        self.app.title("Smart Agricultural Vehicle")

        self.GUI_Font = tkinter.font.Font(family = 'Helvetica', size = 22, weight = 'bold')
        self.GUI_Font2 = tkinter.font.Font(family = 'Helvetica', size = 20)
        self.GUI_Font3 = tkinter.font.Font(family = 'Helvetica', size = 18)
        self.GUI_Font4 = tkinter.font.Font(family = 'Helvetica', size = 12)

        self.leftFrame = Frame(self.app)
        self.rightFrame = Frame(self.app)
        self.topFrame = Frame(self.app)
        self.botFrame = Frame(self.app)

        self.leftFrame.pack(side = LEFT, expand = 1, fill=BOTH)
        self.rightFrame.pack(side = RIGHT, expand = 1, fill=BOTH)
        self.topFrame.pack(side = TOP, expand = 1, fill=BOTH)
        self.botFrame.pack(side = BOTTOM, expand = 1, fill=BOTH)
        self.img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/ARG-Robot/Resources/RoverIcon2.png"))
        self.panel = Label(self.rightFrame, image = self.img)
        self.panel.pack(side = TOP)

        self.label2 = Label(self.topFrame)
        self.label2.pack(side = TOP)
        self.label2.config(text = "<< Smart Vehicle Camera >> ", font = self.GUI_Font, fg = 'royal blue')

        self.cap = cv2.VideoCapture(0)
        self.Webcam_frame = Frame(self.topFrame)
        self.Webcam_frame.pack(side = TOP)
        self.Webcam = Label(self.Webcam_frame)
        self.Webcam.pack(side = TOP)

        self.checkVal = IntVar()
        self.option = IntVar()


        self.Auto_Button = Button(self.rightFrame ,text = 'Automatic Mode', font = self.GUI_Font, command = self.Automatic, bg = 'bisque', height = 3, width = 15)
        self.Auto_Button.pack(side = TOP)
        self.Manual_Button_on = Button(self.rightFrame ,text = 'Manual Mode   ', font = self.GUI_Font, command = self.Manual, bg = 'bisque', height = 3, width = 15)
        self.Manual_Button_on.pack(side = TOP)
        self.cnt = 0
        self.Cap_Button = Button(self.rightFrame ,text = 'Capture Samples', font = self.GUI_Font, command = self.Cap, bg = 'bisque', height = 3, width = 15)
        self.Cap_Button.pack(side = TOP)



        self.label1 = Label(self.leftFrame)
        self.label1.pack(side = TOP, fill = BOTH)
        self.label1.config(text = "Select Options: ", font = self.GUI_Font, fg = 'royal blue')


        self.Light_Button = Checkbutton(self.leftFrame ,text = 'Turn Lights on      ', font = self.GUI_Font2, variable = self.checkVal, command = self.Turn_Lights, bg = 'whitesmoke', height = 2, width = 15)
        self.Light_Button.pack()
        self.temp_Button = Radiobutton(self.leftFrame ,text = 'Send Temperature    ', font = self.GUI_Font3, variable = self.option, value = 1, command = self.IoT_Temp, bg = 'whitesmoke', height = 4, width = 17)
        self.temp_Button.pack()
        self.humi_Button = Radiobutton(self.leftFrame ,text = 'Send Humidity %     ', font = self.GUI_Font3, variable = self.option, value = 2, command = self.IoT_Humi, bg = 'whitesmoke', height = 4, width = 17)
        self.humi_Button.pack()
        self.CO2_Button = Radiobutton(self.leftFrame ,text = 'Send CO2 Level      ', font = self.GUI_Font3, variable = self.option, value = 3, command = self.IoT_CO2, bg = 'whitesmoke', height = 4, width = 17)
        self.CO2_Button.pack()
        self.soil_Button = Radiobutton(self.leftFrame ,text = 'Send Soil Moisture  ', font = self.GUI_Font3, variable = self.option, value = 4, command = self.IoT_Soil, bg = 'whitesmoke', height = 4, width = 17)
        self.soil_Button.pack()
        self.LDR_Button = Radiobutton(self.leftFrame ,text = 'Send Light Intensity', font = self.GUI_Font3, variable = self.option, value = 5, command = self.IoT_LDR, bg = 'whitesmoke', height = 4, width = 17)
        self.LDR_Button.pack()

        self.Exit_Button = Button(self.rightFrame ,text = 'Close Program', font = self.GUI_Font, command = self.Exit_Program, bg = 'light blue', height = 3, width = 15)
        self.app.protocol("WM_DELETE_WINDOW", self.Exit_Program)
        self.Exit_Button.pack(side = BOTTOM)


        self.text = Text(self.botFrame)
        self.text.insert(INSERT, "Smart Vehilce: Turned ON\n")
        self.text.insert(END, "-------------\n")
        self.text.insert(END, "Waiting for Tasks...\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)
        self.text.tag_add("start", "1.0", "1.24")
        self.text.tag_config("start", background="black", foreground="white")
        self.video_stream()


    def video_stream(self):

        Success, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.Webcam.imgtk = imgtk
        self.Webcam.configure(image=imgtk)
        self.Webcam.after(33, self.video_stream)

    def Turn_Lights(self):

        if self.checkVal.get():

            print(1)

        else:

            print(0)

    def Automatic(self):
        self.text.insert(INSERT, "Automatic Mode: Activated\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)
        threading.Thread(target= MF.Automatic_Mode).start()

    def Manual(self):
        self.text.insert(INSERT, "Manual Mode: Activated\nYou can use your keyboard:\n Use Arrows for movement\n Use (S) for spraying\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)
        threading.Thread(target= MF.Manual_Mode).start()

    def Cap(self):
        self.text.insert(INSERT, "Vehicle is capturing samples..\nStored in Desktop/Samples\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)
        for i in range(3):
            self.cnt += 1
            Success, img = self.cap.read()
            cv2.imwrite('/home/pi/Desktop/Samples/'+str(self.cnt)+'.jpg', img)

    def IoT_Temp(self):

        self.text.insert(INSERT, "Sending Temperature Data\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)

        if self.option.get():

            threading.Thread(target= DHT22_Module.Send_Temp())



    def IoT_Humi(self):

        self.text.insert(INSERT, "Sending Humidity Data\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)

        if self.option.get():

            threading.Thread(target= DHT22_Module.Send_Humi())

    def IoT_CO2(self):

        self.text.insert(INSERT, "Sending CO2 Level\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)

        if self.option.get():

            threading.Thread(target= CO2_Module.Send_CO2())

    def IoT_LDR(self):

        self.text.insert(INSERT, "Sending Light State\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)

        if self.option.get():

            threading.Thread(target= LDR_Module.Send_light_state())

    def IoT_Soil(self):

        self.text.insert(INSERT, "Sending Soil Moisture Data\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)

        if self.option.get():

            threading.Thread(target= MS.Moisture())


    def Empty(self):
        pass

    def Exit_Program(self):

        GPIO.cleanup()
        self.app.destroy()

    def Exit_popup(self):

        self.text.insert(INSERT, "Manual Mode: Deactivated\n")
        self.text.insert(END, "-------------\n")
        self.text.pack(side = TOP, fill = BOTH)
        self.popup.destroy()


def Application():
    Run = True
    Source = Tk()
    app = App(Source, Run)

    Source.mainloop()

if __name__ == "__main__":


    Application()
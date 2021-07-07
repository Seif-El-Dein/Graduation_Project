from Modules import Motors_Module as MM
from Modules import Pump_Module as PM
from IoT import MoistureSensor_Module
from Modules import SampleCap_Module as SM
from Modules import Stepper_Motor_Module as SMM
from RemoteControl_Module import Button
import RPi.GPIO as GPIO
import time
import pygame
import sys
from pygame.locals import *
import threading
################# Objects Initialization ##################
Motors = MM.RoverMotors(12,26,16,13,6,5)
Stepper_Motor = SMM.StepperMotor(23,17,27,22)
###########################################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LeftInfra_Sensor = 7
RightInfra_Sensor = 10
GPIO.setup(LeftInfra_Sensor,GPIO.IN)
GPIO.setup(RightInfra_Sensor,GPIO.IN)

clicked = False
counter = 0

def Check_track():

    if GPIO.input(LeftInfra_Sensor) == 0 and GPIO.input(RightInfra_Sensor) == 0:
        Motors.moveF(x = 35,t=0.1)
    elif GPIO.input(LeftInfra_Sensor) == 1 and GPIO.input(RightInfra_Sensor) == 1:
        Motors.StopMoving()
    elif GPIO.input(LeftInfra_Sensor) == 1 and GPIO.input(RightInfra_Sensor) == 0:
        Motors.moveR(x=90, t=0.1)
    elif GPIO.input(LeftInfra_Sensor) == 0 and GPIO.input(RightInfra_Sensor) == 1:
        Motors.moveL(x=90, t=0.1)

def Automatic_Mode():
    pygame.init()

    screen_width = 440
    screen_height = 250

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Manual Control')

    font = pygame.font.SysFont('Constantia', 15)

    bg = (128, 128, 128)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    pygame.display.init()

    screen.fill(bg)

    Run = True
    key_input = pygame.key.get_pressed()
    distance_cnt = 0
    while Run:
        Stop_Auto = Button(150, 0, 'Up', screen)
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_ESCAPE] or Stop_Auto.draw_button():
            Motors.StopMoving()
            pygame.display.quit()
            sys.exit(0)
        else:
            Check_track()
            if distance_cnt == 500:
                distance_cnt = 0
                Motors.StopMoving()
                time.sleep(1)
                Stepper_Motor.PosRotate()
                for i in range(300):
                    Moisture_read = MoistureSensor_Module.Moisture_stepper()
                Stepper_Motor.NegRotate()
                if Moisture_read:
                    PM.pump_on()
                    PM.pump_off()


def Manual_Mode():
    pygame.init()

    screen_width = 440
    screen_height = 250

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Manual Control')

    font = pygame.font.SysFont('Constantia', 15)

    bg = (128, 128, 128)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    pygame.display.init()

    screen.fill(bg)
    Run = True
    while Run:

        Up = Button(150, 0, 'Up', screen)
        Down = Button(150, 70, 'Down', screen)
        Right = Button(300, 70, 'Right', screen)
        Left = Button(0, 70, 'Left', screen)
        #Close = Button(150, 370, 'Close', screen)
        Spray = Button(150, 150, 'Spray Pesticides', screen)
        #Cap = Button(150, 220, 'Capture Images', screen)
        #Model = Button(150, 290, 'Disease Detection', screen)


        key_input = pygame.key.get_pressed()
        if Right.draw_button() or key_input[pygame.K_RIGHT]:
            Motors.moveR(t = 0.1)


        elif Left.draw_button() or key_input[pygame.K_LEFT]:
            Motors.moveL(t = 0.1)


        elif Down.draw_button() or key_input[pygame.K_DOWN]:
            Motors.moveB(t = 0.1)


        elif Up.draw_button() or key_input[pygame.K_UP]:
            Motors.moveF(t = 0.1)


        elif Spray.draw_button() or key_input[pygame.K_s]:
            print('Spray Pesticides')
            PM.pump_on()
            PM.pump_off()


        else:
            Motors.stop(0.1)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit(0)
        pygame.display.update()
import time
import RPi.GPIO as GPIO

def pump_on():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)

    time.sleep(2)

def pump_off():

    GPIO.setup(4, GPIO.IN)
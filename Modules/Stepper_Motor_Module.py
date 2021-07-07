import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class StepperMotor():

    def __init__(self,out1,out2,out3,out4):
        self.out1 = out1
        self.out2 = out2
        self.out3 = out3
        self.out4 = out4
        GPIO.setup(self.out1,GPIO.OUT)
        GPIO.setup(self.out2,GPIO.OUT)
        GPIO.setup(self.out3,GPIO.OUT)
        GPIO.setup(self.out4,GPIO.OUT)

    def PosRotate(self):
        i = 0
        positive = 0
        negative = 0
        y = 0
        x = 90
        for y in range(x,0,-1):
            if negative==1:
                if i==7:
                    i=0
                else:
                    i=i+1
                y=y+2
                negative=0
            positive=1
            #print((x+1)-y)
            if i==0:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==7:
                i=0
                continue
            i=i+1

    def NegRotate(self):
        i = 0
        positive = 0
        negative = 0
        y = 0
        x = -90
        x = x*-1
        for y in range(x,0,-1):
            if positive==1:
                if i==0:
                    i=7
                else:
                    i=i-1
                y=y+3
                positive=0
            negative=1
            #print((x+1)-y)
            if i==0:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.HIGH)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.HIGH)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:
                GPIO.output(self.out1,GPIO.LOW)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:
                GPIO.output(self.out1,GPIO.HIGH)
                GPIO.output(self.out2,GPIO.LOW)
                GPIO.output(self.out3,GPIO.LOW)
                GPIO.output(self.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==0:
                i=7
                continue
            i=i-1


if __name__ == '__main__':

    out1 = 23
    out2 = 17
    out3 = 27
    out4 = 22

    def main():
        stepper = StepperMotor(out1,out2,out3,out4)
        stepper.PosRotate()
        time.sleep(2)
        stepper.NegRotate()


    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()
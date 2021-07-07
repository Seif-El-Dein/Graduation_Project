import RPi.GPIO as GPIO
import time
from azure.iot.device import IoTHubDeviceClient, Message
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

MSG_TXT = '{{"LightState": {LightState}}}'

CONNECTION_STRING = "HostName=iotc-91e149b2-6681-477d-ba9a-872d121f5ed2.azure-devices.net;DeviceId=1ksyrq4g7bv;SharedAccessKey=8Qh7jFwoS41NUfah9CB8hWDbeywz4j0boSXSSQ1ZdV0="

def iothub_client_init():

        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        return client

def Send_light_state():

    try:

        client = iothub_client_init()
        client.connect()
        LightState = GPIO.input(23)
        msg_txt_formatted = MSG_TXT.format(LightState=LightState)
        message = Message(msg_txt_formatted)
        client.send_message(message)
        client.disconnect()

        time.sleep(3)

    except RuntimeError:

        time.sleep(3)
        Send_light_state()


if __name__ == "__main__":

    while True:

        Send_light_state()
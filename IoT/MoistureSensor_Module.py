import Adafruit_ADS1x15
from azure.iot.device import IoTHubDeviceClient, Message
import time
import sys


adc = Adafruit_ADS1x15.ADS1115()
MSG_TXT = '{{"x": {x}}}'
CONNECTION_STRING = "HostName=iotc-91e149b2-6681-477d-ba9a-872d121f5ed2.azure-devices.net;DeviceId=1ksyrq4g7bv;SharedAccessKey=8Qh7jFwoS41NUfah9CB8hWDbeywz4j0boSXSSQ1ZdV0="

def iothub_client_init():

        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        return client

def Moisture():

    client = iothub_client_init()
    value_ads = round(adc.read_adc(0, gain=2/3, data_rate = 250))
    AirValue = 16300
    WaterValue = 10030
    interval = (AirValue - WaterValue)/3

    if(value_ads > WaterValue and value_ads < (WaterValue + interval)):
        print("Very Wet")
        x = 2
        msg_txt_formatted = MSG_TXT.format(x=x)
        message = Message(msg_txt_formatted)
        client.send_message(message)


    elif(value_ads > (WaterValue + interval) and value_ads < (AirValue - interval)):
        print("Wet")
        x= 1
        msg_txt_formatted = MSG_TXT.format(x=x)
        message = Message(msg_txt_formatted)
        client.send_message(message)


    elif(value_ads < AirValue and value_ads > (AirValue - interval)):
        print("Dry")
        x = 0
        msg_txt_formatted = MSG_TXT.format(x=x)
        message = Message(msg_txt_formatted)
        client.send_message(message)

def Moisture_stepper():

    value_ads = round(adc.read_adc(0, gain=2/3, data_rate = 250))
    AirValue = 16300
    WaterValue = 10030
    interval = (AirValue - WaterValue)/3

    if(value_ads > WaterValue and value_ads < (WaterValue + interval)):
        print("Very Wet")
        x = 0
        return  x

    elif(value_ads > (WaterValue + interval) and value_ads < (AirValue - interval)):
        print("Wet")
        x= 0
        return x

    elif(value_ads < AirValue and value_ads > (AirValue - interval)):
        print("Dry")
        x = 1
        return x

import board
import time
import adafruit_dht
from azure.iot.device import IoTHubDeviceClient, Message
import Adafruit_ADS1x15
import sys


CONNECTION_STRING = "HostName=iotc-91e149b2-6681-477d-ba9a-872d121f5ed2.azure-devices.net;DeviceId=1ksyrq4g7bv;SharedAccessKey=8Qh7jFwoS41NUfah9CB8hWDbeywz4j0boSXSSQ1ZdV0="

dhtDevice = adafruit_dht.DHT22(board.D24, use_pulseio=False)
adc = Adafruit_ADS1x15.ADS1115()

#act as dic that is sent temp. & humidity & co2 ppm to the cloud
MSG_Temp = '{{"temperature": {temperature}}}'
MSG_Humi = '{{"humidity": {humidity}}}'

def iothub_client_init():

        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        return client

def Send_Temp():

    try:
        client = iothub_client_init()
        client.connect()

        temperature = dhtDevice.temperature

        msg_txt_formatted = MSG_Temp.format(temperature=temperature)
        message = Message(msg_txt_formatted)

        if temperature > 30:
            message.custom_properties["temperatureAlert"] = "true"
        else:
            message.custom_properties["temperatureAlert"] = "false"


        print( "Sending message: {}".format(message) )
        client.send_message(message)
        print ( "Message successfully sent" )
        time.sleep(1)
        client.disconnect()



    except RuntimeError:

        print ("Error, Trying to read the sensors again")
        time.sleep(2)
        pass

def Send_Humi():

    try:
        client = iothub_client_init()
        client.connect()

        humidity = dhtDevice.humidity
        msg_txt_formatted = MSG_Humi.format(humidity=humidity)
        message = Message(msg_txt_formatted)

        if humidity > 75 or humidity < 60:
            message.custom_properties["humidityAlert"] = "true"
        else:
            message.custom_properties["humidityAlert"] = "false"


        print( "Sending message: {}".format(message) )
        client.send_message(message)
        print ( "Message successfully sent" )
        time.sleep(1)
        client.disconnect()



    except RuntimeError:

        print ("Error, Trying to read the sensors again")
        time.sleep(2)
        pass

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    Run = 1

    while Run:

        Send_Humi()
        time.sleep(5)
        Send_Temp()
        time.sleep(5)
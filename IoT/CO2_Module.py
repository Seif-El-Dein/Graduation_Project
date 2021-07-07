import adafruit_dht
import time
import sys
import math
import operator
import Adafruit_ADS1x15
import board
from azure.iot.device import IoTHubDeviceClient, Message


dhtDevice = adafruit_dht.DHT22(board.D24, use_pulseio=False)
CONNECTION_STRING = "HostName=iotc-91e149b2-6681-477d-ba9a-872d121f5ed2.azure-devices.net;DeviceId=1ksyrq4g7bv;SharedAccessKey=8Qh7jFwoS41NUfah9CB8hWDbeywz4j0boSXSSQ1ZdV0="

MSG_TXT = '{{"CO2_PPM": {CO2_PPM}}}'

def DHT_Para():

    t = dhtDevice.temperature
    h = dhtDevice.humidity
    return t, h


adc = Adafruit_ADS1x15.ADS1115()


# The load resistance on the board
RLOAD = 10.0
# Calibration resistance at atmospheric CO2 level
RZERO = 76.63
# Parameters for calculating ppm of CO2 from sensor resistance
PARA = 116.6020682
PARB = 2.769034857

# Parameters to model temperature and humidity dependence
CORA = 0.00035
CORB = 0.02718
CORC = 1.39538
CORD = 0.0018
CORE = -0.003333333
CORF = -0.001923077
CORG = 1.130128205

# Atmospheric CO2 level for calibration purposes
ATMOCO2 = 397.13

def iothub_client_init():

        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        return client

def getCorrectionFactor(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG):
	# Linearization of the temperature dependency curve under and above 20 degree C
	# below 20degC: fact = a * t * t - b * t - (h - 33) * d
	# above 20degC: fact = a * t + b * h + c
	# this assumes a linear dependency on humidity
	if t < 20:
		return CORA * t * t - CORB * t + CORC - (h-33.)*CORD
	else:
		return CORE * t + CORF * h + CORG



def getResistance(value_pin,RLOAD):
	return ((1023./value_pin) - 1.)*RLOAD



def getCorrectedResistance(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD):
	return getResistance(value_pin,RLOAD) / getCorrectionFactor(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG)



def getPPM(PARA,RZERO,PARB,value_pin,RLOAD):

	return PARA * math.pow((getResistance(value_pin,RLOAD)/RZERO), -PARB)




def getCorrectedPPM(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD,PARA,RZERO,PARB):
	return PARA * math.pow((getCorrectedResistance(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD)/RZERO), -PARB)



def getRZero(value_pin,RLOAD,ATMOCO2,PARA,PARB):
	return getResistance(value_pin,RLOAD) * math.pow((ATMOCO2/PARA), (1./PARB))



def getCorrectedRZero(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD,ATMOCO2,PARA,PARB):
	return getCorrectedResistance(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD) * math.pow((ATMOCO2/PARA), (1./PARB))



def map(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def Send_CO2():

    client = iothub_client_init()
    client.connect()
    t, h = DHT_Para()
    value_ads = adc.read_adc(3, gain=1)
    value_pin = map((value_ads - 565), 0, 26690, 0, 1023)
    rzero = getRZero(value_pin,RLOAD,ATMOCO2,PARA,PARB)
    correctedRZero = getCorrectedRZero(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD,ATMOCO2,PARA,PARB)
    resistance = getResistance(value_pin,RLOAD)
    resistance = getResistance(value_pin,RLOAD)
    #CO2_PPM = getPPM(PARA,RZERO,PARB,value_pin,RLOAD)
    CO2_PPM = getCorrectedPPM(t,h,CORA,CORB,CORC,CORD,CORE,CORF,CORG,value_pin,RLOAD,PARA,RZERO,PARB)
    msg_txt_formatted = MSG_TXT.format(CO2_PPM=CO2_PPM)
    message = Message(msg_txt_formatted)
    client.send_message(message)
    client.disconnect()
    print("\t PPM: %s" % round(CO2_PPM))
    #sys.exit()




if __name__ == '__main__':

    Send_CO2()
    time.sleep(10)
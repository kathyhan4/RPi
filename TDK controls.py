# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 20:51:56 2016

@author: khan
"""
##import visa
import serial
import time
import math
import numpy

###-------------------Definitions for TDK Lambda
def setAddress(addressvalue=1):
    serTDK.write('ADR ' + str(addressvalue) + '\r\n')

def getIDN():
    serTDK.write('IDN?\r\n')

def setVoltage(voltagevalue=5.0):
    serTDK.write('PV ' + str(voltagevalue) + '\r\n')

def setCurrent(currentvalue=1):
    serTDK.write('PC ' + str(currentvalue) + '\r\n')

def setPort(port='COM4'):
    serTDK.port = port

def setBaudrate(baudratevalue = 57600):
    serTDK.baudrate = baudratevalue

def setOutputOn():
    serTDK.write('OUT ON\r\n')

def setOutputOff():
    serTDK.write('OUT OFF\r\n')

def getVoltage():
    serTDK.readlines(serTDK.inWaiting())
    serTDK.write('MV?\r\n')
    time.sleep(0.01)
    return (serTDK.readlines(serTDK.inWaiting())[0])

def getCurrent():
    serTDK.readlines(serTDK.inWaiting())
    serTDK.write('MC?\r\n')
    time.sleep(0.01)
    return (serTDK.readlines(serTDK.inWaiting())[0])
##---------------------------------------------------------------------

timestamp = time.time()
first_time_seconds = str(math.floor(timestamp))

##Vmin = float(2.8)
VmaxTDK = float(4.2)
CurrentmaxTDK =  float(2.25)

#----------Initialize communication with the Power Supply, TDK Lambda Z100-8--------------
serTDK = serial.Serial()
serTDK.timeout = 1
#print serTDK
setBaudrate()
setPort('COM4')
report_open = serTDK.is_open
TDKAddress = 1

if report_open == True:
    serTDK.close()

serTDK.open()

setAddress(TDKAddress)
#a = getIDN()
#print a
f = getIDN()
print f
setVoltage(VmaxTDK)
setCurrent(CurrentmaxTDK)
setOutputOn()

    #----------Set voltage, read voltage and current on PS, read V on shunt resistor--------------
#setVoltage(VmaxTDK)
time.sleep(2)

##---------------------------------------------------------------------
setOutputOff()

#--------closes serial port so it can be used by other programs and tools later
serTDK.close()

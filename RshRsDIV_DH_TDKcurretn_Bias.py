
import serial
import traceback
import re
#import datetime
import datetime
#import sys
import time
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import ReadTempRh
from matplotlib.font_manager import FontProperties
import math


############### Note: Make sure Keithley is set to Terminator: <LF>, RS-232, and 57600 baud
run_length = float(1000) #time to collect data in hours
time_per_point = float(300.0)/60.0 # time between data pionts in minutes
number_points = int(run_length * 60 / time_per_point)
points_between_LV = 2 # number of timepoints of just current measure
NUMBER_SAMPLES_HV = 0

USER = "Kat"
NOW = str(datetime.datetime.now())

LV_KEITHLEY_PORT = '/dev/ttyUSB0'
PORT_TDK = '/dev/ttyACM0'
ARDUINO_PORT = '/dev/ttyACM1'
KEITHLEY_BAUDRATE= 57600
OPEN_ARDUINO_PORTS = ['2O32O','3O33O','4O34O','5O35O','6O36O','7O37O','8O38O','9O39O','14O40O','15O41O',\
'16O42O','17O43O','18O44O','19O45O','20O46O','21O47O']
CLOSE_ARDUINO_PORTS = ['2C32C','3C33C','4C34C','5C35C','6C36C','7C37C','8C38C','9C39C','14C40C','15C41C',\
'16C42C','17C43C','18C44C','19C45C','20C46C','21C47C']
NUMBER_SAMPLES = 10

### Parameters for high current DIV for Rs measurement
RS_START_CURRENT = str(5)
RS_STOP_CURRENT = str(4)
RS_CURRENT_STEP = str(-1e-1)
RS_VOLTAGE_PROTECTION = str(10)
RS_NUMBER_STEPS = str(11) #21 or fewer
RS_SOURCE_DELAY = str(0.01) # choose 10 ms for this to reduce heating
RS_TIMEOUT = float(RS_NUMBER_STEPS) * float(RS_SOURCE_DELAY) +1.0


### Parameters for low current DIV for Rsh measurement
RSH_START_CURRENT = str(0.00011)
RSH_STOP_CURRENT = str(0.00001)
RSH_CURRENT_STEP = str(-1e-5)
RSH_VOLTAGE_PROTECTION = str(10)
RSH_NUMBER_STEPS = str(11) #21 or fewer
RSH_SOURCE_DELAY = str(0.01) # choose 10 ms for this to reduce heating
RSH_TIMEOUT = float(RS_NUMBER_STEPS) * float(RS_SOURCE_DELAY) +1.0

HV_TIMEOUT = float(1.0)

### Current bias parameters
VmaxTDK = float(80.0)
CurrentmaxTDK =  float(2.25)
TDK_BAUDRATE = 57600
TDK_TIMEOUT = 1.0


print RSH_TIMEOUT

source_delay = 0.01
#serKeithleyHV = serial.Serial()
serTDK = serial.Serial()
serKeithleyLV = serial.Serial()
serArduino = serial.Serial()
first_time_seconds = str('%.0f' % round(time.time(), 1)) #
OutputFileMetaData = '/home/pi/Desktop/RPiData/DH_HV_DIV/RealTimeDIVMeta'
OutputFileLVData = '/home/pi/Desktop/RPiData/DH_HV_DIV/RealTimeDIV_LV'

#ReadTempRh(i=0, first_time_seconds)

####-------------------Definitions for TDK Lambda
#def setAddress(addressvalue=1):
    #serTDK.write('ADR ' + str(addressvalue) + '\r\n')

#def getIDN():
    #serTDK.write('IDN?\r\n')

#def setVoltage(voltagevalue=5.0):
    #serTDK.write('PV ' + str(voltagevalue) + '\r\n')

#def setCurrent(currentvalue=1):
    #serTDK.write('PC ' + str(currentvalue) + '\r\n')

#def setPort(port='COM4'):
    #serTDK.port = port

#def setBaudrate(baudratevalue = 57600):
    #serTDK.baudrate = baudratevalue

#def setOutputOn():
    #serTDK.write('OUT ON\r\n')

#def setOutputOff():
    #serTDK.write('OUT OFF\r\n')

#def getVoltage():
    #serTDK.readlines(serTDK.inWaiting())
    #serTDK.write('MV?\r\n')
    #time.sleep(0.01)
    #return (serTDK.readlines(serTDK.inWaiting())[0])

#def getCurrent():
    #serTDK.readlines(serTDK.inWaiting())
    #serTDK.write('MC?\r\n')
    #time.sleep(0.01)
    #return (serTDK.readlines(serTDK.inWaiting())[0])
    

def DIVRs(RS_VOLTAGE_PROTECTION, RS_START_CURRENT, \
RS_STOP_CURRENT,RS_CURRENT_STEP,RS_NUMBER_STEPS,\
RS_SOURCE_DELAY):
    global serKeithleyLV
    print RS_TIMEOUT
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = KEITHLEY_BAUDRATE
    serKeithleyLV.port = LV_KEITHLEY_PORT
    serKeithleyLV.timeout = RS_TIMEOUT
    
    serKeithleyLV.close()
    serKeithleyLV.open()
    serKeithleyLV.write(':OUTP OFF\n')
    serKeithleyLV.write('*RST\n')
    time.sleep(2)
    serKeithleyLV.write(':ROUT:TERM FRON\n')
    serKeithleyLV.write(':ROUT:TERM?\n')
    terminal = (serKeithleyLV.read(10))
    serKeithleyLV.write(':SENS:FUNC:CONC OFF\n')
    serKeithleyLV.write(':SYST:RSEN ON\n') # chooses 4wire measurement setting
    serKeithleyLV.write(':SOUR:FUNC CURR\n')
    serKeithleyLV.write(":SENS:FUNC 'VOLT:DC'\n")
    serKeithleyLV.write(':SENS:VOLT:PROT '+ RS_VOLTAGE_PROTECTION+'\n')
    serKeithleyLV.write(':SOUR:CURR:STAR '+ RS_START_CURRENT+'\n') # start current
    serKeithleyLV.write(':SOUR:CURR:STOP '+ RS_STOP_CURRENT+'\n') # stop current
    serKeithleyLV.write(':SOUR:CURR:STEP ' + RS_CURRENT_STEP+'\n') #increment
    serKeithleyLV.write(':SOUR:CURR:MODE SWE\n')
    serKeithleyLV.write(':SOUR:SWE:RANG:AUTO 1\n')
    serKeithleyLV.write(':SOUR:SWE:SPAC LIN\n')
    serKeithleyLV.write(':TRIG:COUN ' + RS_NUMBER_STEPS+'\n') # number of points to measure
    serKeithleyLV.write(':SOUR:DEL ' + RS_SOURCE_DELAY+'\n') # source delay in sec
    serKeithleyLV.write(':OUTP ON\n') #starts the sweep
    serKeithleyLV.write(':INIT\n')
    serKeithleyLV.write(':READ?\n') #requests the data from the 2440
    
    # get all of the data out
    a = serKeithleyLV.readline() #super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
    a = a.split(',') #turns this into an array instead of a string with a bunch of commas
    #print a
    # clean up the 2440 and the port (turn off output and close port)
    serKeithleyLV.write(':OUTP OFF\n')
    serKeithleyLV.close() 
    DIVoutput = np.zeros((len(a)/5,3))
    
    #Header = ['Voltage (V)', 'Current (A)', 'Resistance (ohm)']

    for i in range(len(a)/5):
        DIVoutput[i,0] = a[i*5] # voltages
        DIVoutput[i,1] = a[i*5+1] #current
    RS_MIN = 0
    for i in range(len(a)/5-1):   
        DIVoutput[i+1,2] = (DIVoutput[i+1,0] - DIVoutput[i,0]) / (DIVoutput[i+1,1] - DIVoutput[i,1])
    try:
        RS_MIN = min(x for x in DIVoutput[1:-1,2] if x > 0.1)
    except:
        print "no min"
    print RS_MIN
    print DIVoutput
    return DIVoutput, RS_MIN, terminal


def DIVRsh(RSH_VOLTAGE_PROTECTION, RSH_START_CURRENT, \
RSH_STOP_CURRENT,  RSH_CURRENT_STEP,RSH_NUMBER_STEPS,\
RSH_SOURCE_DELAY):
    global serKeithleyLV
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = KEITHLEY_BAUDRATE
    serKeithleyLV.port = LV_KEITHLEY_PORT
    serKeithleyLV.timeout = RSH_TIMEOUT
    print RSH_TIMEOUT

    serKeithleyLV.close()
    serKeithleyLV.open()
    serKeithleyLV.write(':OUTP OFF\n')
    print "try reset"
    time.sleep(0.5)
    serKeithleyLV.write('*RST\n')
    time.sleep(2)
    print "set front terminal"
    serKeithleyLV.write(':ROUT:TERM FRON\n')
    serKeithleyLV.write(':ROUT:TERM?\n')
    terminal = (serKeithleyLV.read(10))
    print "set concurrent off"
    serKeithleyLV.write(':SENS:FUNC:CONC OFF\n')
    serKeithleyLV.write(':SYST:RSEN ON\n') # chooses 4wire measurement setting
    serKeithleyLV.write(':SOUR:FUNC CURR\n')
    serKeithleyLV.write(":SENS:FUNC 'VOLT:DC'\n")
    print "set volt protection"
    time.sleep(1)
    serKeithleyLV.write(':SENS:VOLT:PROT '+ RSH_VOLTAGE_PROTECTION+'\n')
    serKeithleyLV.write(':SOUR:CURR:STAR '+ RSH_START_CURRENT+'\n') # start current
    serKeithleyLV.write(':SOUR:CURR:STOP '+ RSH_STOP_CURRENT+'\n') # stop current
    serKeithleyLV.write(':SOUR:CURR:STEP ' + RSH_CURRENT_STEP+'\n') #increment
    serKeithleyLV.write(':SOUR:CURR:MODE SWE\n')
    serKeithleyLV.write(':SOUR:SWE:RANG:AUTO 1\n')
    serKeithleyLV.write(':SOUR:SWE:SPAC LIN\n')
    serKeithleyLV.write(':TRIG:COUN ' + RSH_NUMBER_STEPS+'\n') # number of points to measure
    serKeithleyLV.write(':SOUR:DEL ' + RSH_SOURCE_DELAY+'\n') # source delay in sec
    serKeithleyLV.write(':OUTP ON\n') #starts the sweep
    serKeithleyLV.write(':INIT\n')
    serKeithleyLV.write(':READ?\n') #requests the data from the 2440
    
    # get all of the data out
    a = serKeithleyLV.readline() #super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
    a = a.split(',') #turns this into an array instead of a string with a bunch of commas
    #print a
    # clean up the 2440 and the port (turn off output and close port)
    serKeithleyLV.write(':OUTP OFF\n')
    serKeithleyLV.close() 
    DIVoutput = np.zeros((len(a)/5,3))
    
    #Header = ['Voltage (V)', 'Current (A)', 'Resistance (ohm)']

    for i in range(len(a)/5):
        DIVoutput[i,0] = a[i*5] # voltages
        DIVoutput[i,1] = a[i*5+1] #current
        
    for i in range(len(a)/5-1):   
        DIVoutput[i+1,2] = (DIVoutput[i+1,0] - DIVoutput[i,0]) / (DIVoutput[i+1,1] - DIVoutput[i,1])
    RSH_MEAN = np.mean(DIVoutput[3:8,2])
    print DIVoutput
    print RSH_MEAN
    return DIVoutput, RSH_MEAN, terminal



def CurrentBias(VmaxTDK, CurrentmaxTDK,PORT_TDK):
    global serTDK

    #----------Initialize communication with the Power Supply, TDK Lambda Z100-8--------------
    serTDK = serial.Serial()
    serTDK.timeout = 1
    #print serTDK
    serTDK.baudrate = KEITHLEY_BAUDRATE
    #setBaudrate()
    serTDK.port = PORT_TDK
    #setPort(PORT_TDK)
    #report_open = isOpen()
    TDKAddress = 1
    try:
        serTDK.close()
    except:
        print "serTDK already closed"
    serTDK.open()
    
    serTDK.write('ADR ' + str(TDKAddress) + '\r\n')
    #a = getIDN()
    #print a
    serTDK.write('IDN?\r\n')
    f = serTDK.readline()
    print f
    serTDK.write('PV ' + str(VmaxTDK) + '\r\n')
    serTDK.write('PC ' + str(CurrentmaxTDK) + '\r\n')
    serTDK.write('OUT ON\r\n')
    
        #----------Set voltage, read voltage and current on PS, read V on shunt resistor--------------
    #setVoltage(VmaxTDK)
    time.sleep(time_per_point*60.0)
    
    ##---------------------------------------------------------------------
    
    serTDK.write('OUT OFF\r\n')
    
    #--------closes serial port so it can be used by other programs and tools later
    serTDK.close()

    

def main():
    ####################
    print "set up arduino port"
    global serArduino
    instring = ""
    serArduino = serial.Serial(
        port=ARDUINO_PORT,
        baudrate=9600,
    )
    #####################
    print "set up TDK and Keithley ports"
    instring = ""
    ##thingsToDo = [1]
    serTDK = serial.Serial()
    serTDK.baudrate = TDK_BAUDRATE
    serTDK.port = PORT_TDK
    serTDK.timeout = TDK_TIMEOUT
    print serTDK.timeout
    
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = KEITHLEY_BAUDRATE
    serKeithleyLV.port = LV_KEITHLEY_PORT
    serKeithleyLV.timeout = HV_TIMEOUT
    print serKeithleyLV.timeout
    
    print "make sure ports are closed"
    try:
        serKeithleyHV.close()
        serArduino.close()
    except:
        print "ports not open"

    LV_output = np.zeros((number_points, 50))
    LV_output = np.zeros((number_points, 50))
    
    ##### do some initial setup stuff
    print "open Keithley and TDK ports"
    serTDK
    serTDK.open()
    serTDK.flushInput()
    serTDK.flushOutput()
    serTDK.write('*RST\n')
    time.sleep(1.0)
    serKeithleyLV
    serKeithleyLV.open()
    serKeithleyLV.flushInput()
    serKeithleyLV.flushOutput()
    serKeithleyLV.write('*RST\n')
    time.sleep(1.0)
    
    print "open arduino port"
    
    serArduino
    try:
        serArduino.close() 
    except:
        print "serArduino already closed"
    serArduino.open() 
    print "Current bias TDK"
    try:
        serTDK.close() 
    except:
        print "serTDK already closed"
    serTDK.open() 

    print "try to get IDN"
    serTDK.write('IDN?\r\n')
    time.sleep(0.1)
    ident = serTDK.read(200)
    print "reading ser"
    time.sleep(0.1)
    print ident
    time.sleep(0.1)
    
    print "LV Keithley"
    print serKeithleyLV.port   
    print "try to get IDN"
    serKeithleyLV.write('*IDN?\n')
    time.sleep(0.5)
    identlv = serKeithleyLV.read(200)
    print "reading ser"
    time.sleep(0.5)
    print identlv
    time.sleep(0.5)
    
    print "flush buffer"
    serTDK.flushInput()
    serTDK.flushOutput()
    
    time.sleep(0.001)
    
    ReadTempRh.WriteToFile("Datetime: "+str(NOW)+"\n"\
    +"DIV Power Supply: "+str(identlv)+"\n"\
    +"HV Bias Power Supply: "+str(ident)+"\n"\
    +"Number of Samples: "+str(NUMBER_SAMPLES)+"\n"\
    +"Time of start: "+str(first_time_seconds)+"\n\n"\
    +"Parameters for high current DIV for Rs measurement \n"\
    +"RS_START_CURRENT: "+str(RS_START_CURRENT)+"\n"\
    +"RS_STOP_CURRENT: "+str(RS_STOP_CURRENT)+"\n"\
    +"RS_CURRENT_STEP: "+str(RS_CURRENT_STEP)+"\n"\
    +"RS_VOLTAGE_PROTECTION: "+str(RS_VOLTAGE_PROTECTION)+"\n"\
    +"RS_NUMBER_STEPS: "+str(RS_NUMBER_STEPS) +"\n"\
    +"RS_SOURCE_DELAY: "+str(RS_SOURCE_DELAY) +"\n"\
    +"RS_TIMEOUT: "+str(RS_TIMEOUT)+"\n\n"\
    +"Parameters for low current DIV for Rsh measurement \n"\
    +"RSH_START_CURRENT: "+str(RSH_START_CURRENT )+"\n"\
    +"RSH_STOP_CURRENT: "+str(RSH_STOP_CURRENT )+"\n"\
    +"RSH_CURRENT_STEP: "+str(RSH_CURRENT_STEP )+"\n"\
    +"RSH_VOLTAGE_PROTECTION: "+str(RSH_VOLTAGE_PROTECTION )+"\n"\
    +"RSH_NUMBER_STEPS: "+str(RSH_NUMBER_STEPS ) +"\n"\
    +"RSH_SOURCE_DELAY: "+str(RSH_SOURCE_DELAY )  +"\n"\
    +"RSH_TIMEOUT: "+str(RSH_TIMEOUT)+"\n\n"\
    +"Current bias parameters \n"\
    +"TDK Current setting: "+str(CurrentmaxTDK)+"\n"\
    +"TDK Voltage limit: "+str(VmaxTDK)+"\n"\
    ,OutputFileMetaData,first_time_seconds)
    
    ReadTempRh.WriteToFile("Timepoint,Epoch Time (seconds), Time (hrs),"+  \
    "Sample Number, Rsh Mean, Rsh StDev, Rs Min, Sample Number, Rsh Mean, Rsh StDev, Rs Min,"+\
    "Sample Number, Rsh Mean, Rsh StDev, Rs Min,Sample Number, Rsh Mean, Rsh StDev, Rs Min,"+\
    "Sample Number, Rsh Mean, Rsh StDev, Rs Min, Sample Number, Rsh Mean, Rsh StDev, Rs Min,"+\
    "Sample Number, Rsh Mean, Rsh StDev, Rs Min, Sample Number, Rsh Mean, Rsh StDev, Rs Min,"+\
    "Sample Number, Rsh Mean, Rsh StDev, Rs Min, Sample Number, Rsh Mean, Rsh StDev, Rs Min,"+\
    #, , , , , , , ,"+\
    #" , , , , , , , , , , , , , "+\
    "\n",OutputFileLVData,first_time_seconds)


    #ReadTempRh.WriteToFile("Timestamp  " + str(first_time_seconds) +"\n"\
    #"IDN  " + str(ident) +"\n"\
    #,OutputFile=OutputFileMetaData,first_time_seconds=first_time_seconds)
    raw_data_Rs = np.zeros((number_points,NUMBER_SAMPLES))
    raw_data_Rsh = np.zeros((number_points,NUMBER_SAMPLES))
    raw_data_HV = np.zeros((number_points,3))
    for i in range(number_points):
        try:
            LV_output[i,0] = i
            LV_output[i,1] = round(time.time(), 0) #
            LV_output[i,2] = (round(time.time(), 0)-float(first_time_seconds))/3600 # time in hrs

            print i

            if i%points_between_LV == 0:
                serTDK.write('OUT OFF\r\n')
                
                for j in range(NUMBER_SAMPLES): 
                    # 4 wire on first port
                    serArduino.write('2O3O4O5O6O7O8O9O14O15O16O17O18O19O20O21O32O33O34O35O36O37O38O39O40O41O42O43O44O45O46O47O')
                    time.sleep(0.1)
                    serArduino.write(CLOSE_ARDUINO_PORTS[j])
                    time.sleep(0.1)
                    DIV_Rsh_output, RSH_MEAN, terminal = DIVRsh(
                    RSH_VOLTAGE_PROTECTION, RSH_START_CURRENT,RSH_STOP_CURRENT, RSH_CURRENT_STEP,RSH_NUMBER_STEPS,RSH_SOURCE_DELAY
                    )
                    time.sleep(0.1)
                    LV_output[i,3+j*4] = j+1
                    LV_output[i,4+j*4] = RSH_MEAN
                    LV_output[i,5+j*4] = np.std(DIV_Rsh_output[1:-1, 2])
                    #raw_data_Rsh[i,0] = DIV_Rsh_output
                    DIV_Rs_output, RS_MIN, terminal = DIVRs(
                    RS_VOLTAGE_PROTECTION, RS_START_CURRENT,RS_STOP_CURRENT,RS_CURRENT_STEP,RS_NUMBER_STEPS,RS_SOURCE_DELAY
                    )
                    time.sleep(0.1)
                    #raw_data_Rs[i,0] = DIV_Rs_output
                    LV_output[i,6+j*4] = RS_MIN
                    serArduino.write(OPEN_ARDUINO_PORTS[j])
                    time.sleep(0.1)
    
            
                ReadTempRh.WriteToFile(str(LV_output[i,0]) + "," + str(LV_output[i,1]) + "," + str(LV_output[i,2]) + "," + str(LV_output[i,3]) + "," + \
                str(LV_output[i,4]) + "," + str(LV_output[i,5]) + "," + str(LV_output[i,6]) + "," + str(LV_output[i,7]) + "," + \
                str(LV_output[i,8]) + "," + str(LV_output[i,9]) + "," + str(LV_output[i,10]) + "," + str(LV_output[i,11]) + "," + \
                str(LV_output[i,12]) + "," + str(LV_output[i,13]) + "," + str(LV_output[i,14]) + "," + str(LV_output[i,15]) + "," + \
                str(LV_output[i,16]) + "," + str(LV_output[i,17]) + "," + str(LV_output[i,18]) + "," + str(LV_output[i,19]) + "," + \
                str(LV_output[i,20]) + "," + str(LV_output[i,21]) + "," + str(LV_output[i,22]) + "," + str(LV_output[i,23]) + "," + \
                str(LV_output[i,24]) + "," + str(LV_output[i,25]) + "," + str(LV_output[i,26]) + "," + str(LV_output[i,27]) + "," + \
                str(LV_output[i,28]) + "," + str(LV_output[i,29]) + "," + str(LV_output[i,30]) + "," + str(LV_output[i,31]) + "," + \
                str(LV_output[i,32]) + "," + str(LV_output[i,33]) + "," + str(LV_output[i,34]) + "," + str(LV_output[i,35]) + "," + \
                str(LV_output[i,36]) + "," + str(LV_output[i,37]) + "," + str(LV_output[i,38]) + "," + str(LV_output[i,39]) + "," + \
                str(LV_output[i,40]) + "," + str(LV_output[i,41]) + "," + str(LV_output[i,42]) + "," + str(LV_output[i,43]) + "," + \
                #str(LV_output[i,44]) + "," + str(LV_output[i,45]) + "," + str(LV_output[i,46]) + "," + str(LV_output[i,47]) + "," + \
                #str(LV_output[i,48]) + "," + str(LV_output[i,49])  + 
                "\n",OutputFileLVData,first_time_seconds)

            else:
                #raw_data_HV[i,0] = float(i)
                #raw_data_HV[i,1] = time.time()
                print "try to set current bias"
                CurrentBias(VmaxTDK, CurrentmaxTDK,PORT_TDK)
                #raw_data_HV = HVBias(HV_CURRENT_PROTECTION,HV_SOURCE_DELAY, HV_BIAS)
                #print raw_data_HV
                ReadTempRhCurrent.getTRHCurrent(i,number_points,first_time_seconds, NUMBER_SAMPLES_HV)
        except:
            print "Exception:"
            traceback.print_exc()
            pass
            break
        #print "done with cycle, getting ready to graph"

        #font = {'family' : 'sans-serif',
        #'weight' : 'bold',
        #'size'   : 10}
        #title_font = {'fontname':'Arial', 'size':'8', 'color':'black', 'weight':'normal','verticalalignment':'bottom'} # Bottom vertical alignment for more space
        #matplotlib.rc('font', **font)
        #fontP = FontProperties()
        #fontP.set_size('xx-small')
        ####### graph Rsh history
        #figure(num=None, figsize=(6, 4), dpi=100, facecolor='w', edgecolor='k')
        #plt.plot(LV_output[0:i,2],LV_output[0:i,4], 'ko', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,8], 'bo', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,12], 'mo', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,16], 'go', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,20], 'k.', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,24], 'b.', linewidth=3.0)
        #ylabel('Rsh (ohms)',**font)
        #plt.ylim([-0.1,max(max(LV_output[:,4]), max(LV_output[:,8]), max(LV_output[:,12]))*2.0])
        #plt.xlim([0,max(LV_output[:,2])*1.5])
        #xlabel('Time (hrs)',**font)
        #title(r'Rsh',**font)
        
        #plt.legend(['Sample 1', 'Sample 2', 'Sample 3','Sample 4', 'Sample 5', 'Sample 6'],loc='upper left')
        #print "saving graph 1"
        ##plt.setp(legend.get_title(),fontsize='xx-small')
        #savefig(OutputFileLVData+first_time_seconds+'_Rsh.png')
        ###plt.show()
        #print "graph 1 saved"
        
        
       ####### graph Rs history
        #figure(num=None, figsize=(6, 4), dpi=100, facecolor='w', edgecolor='k')
        #plt.plot(LV_output[0:i,2],LV_output[0:i,6], 'ko', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,10], 'bo', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,14], 'mo', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,18], 'go', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,22], 'k.', linewidth=3.0)
        #plt.plot(LV_output[0:i,2],LV_output[0:i,26], 'b.', linewidth=3.0)
        #ylabel('Rs (ohms)',**font)
        #plt.ylim([-0.1,max(max(LV_output[:,6]), max(LV_output[:,10]), max(LV_output[:,14]))*2.0])
        #plt.xlim([0,max(LV_output[:,2])*1.5])
        #xlabel('Time (hrs)',**font)
        #title('Rs',**font)
        #plt.legend(['Sample 1', 'Sample 2', 'Sample 3','Sample 4', 'Sample 5', 'Sample 6'], loc='upper left')
        ##plt.setp(legend.get_title(),fontsize='xx-small')
        #print "saving graph 2"
        #savefig(OutputFileLVData+first_time_seconds+'_Rs.png')
        ###plt.show()
        #print "graph 2 saved"


        #time.sleep(time_per_point*60) #Waits for the next time point
        

    
        
    serTDK.close()
    serArduino.close()
    
if __name__ == "__main__":
   main()

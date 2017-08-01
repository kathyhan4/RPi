
import serial
import traceback
import re
import datetime
#import sys
import time
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import Read48Current

############### Note: Make sure Keithley is set to Terminator: <LF>, RS-232, and 57600 baud
run_length = float(20) #time to collect data in hours
time_per_point = float(30.0)/60.0 # time between data pionts in minutes
number_points = int(run_length * 60 / time_per_point)
points_between_LV = 2 # number of timepoints of just 

start_current = str(5)
stop_current = str(4)
current_step = str(-1e-1)
voltage_protection = str(10)
number_steps = str(11) #21 or fewer
number_steps_int = int(number_steps)
source_delay = str(0.01) # choose 10 ms for this to reduce heating
timeout_sec = float(number_steps) * float(source_delay) +1.0
print timeout_sec
number_samples = 3
source_delay = 0.01
serKeithleyHV = serial.Serial()
serKeithleyLV = serial.Serial()
serArduino = serial.Serial()
first_time_seconds = str('%.0f' % round(time.time(), 1)) #
OutputFileMetaData = '/home/pi/Desktop/RPiData/DH_HV_DIV/RealTimeDIVMeta'
OutputFileLVData = '/home/pi/Desktop/RPiData/DH_HV_DIV/RealTimeDIV_LV'

#Read48Current(i=0, first_time_seconds)

def DIVRs(voltage_protection=str(10), start_current=str(5), \
stop_current=str(4),current_step = str(-1e-1),number_steps = str(11),\
number_steps_int = int(number_steps),source_delay = str(0.01)):
    global serKeithleyLV
    print timeout_sec
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = 57600
    serKeithleyLV.port = '/dev/ttyUSB1'
    serKeithleyLV.timeout = timeout_sec
    
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
    serKeithleyLV.write(':SENS:VOLT:PROT '+ voltage_protection+'\n')
    serKeithleyLV.write(':SOUR:CURR:STAR '+ start_current+'\n') # start current
    serKeithleyLV.write(':SOUR:CURR:STOP '+ stop_current+'\n') # stop current
    serKeithleyLV.write(':SOUR:CURR:STEP ' + current_step+'\n') #increment
    serKeithleyLV.write(':SOUR:CURR:MODE SWE\n')
    serKeithleyLV.write(':SOUR:SWE:RANG:AUTO 1\n')
    serKeithleyLV.write(':SOUR:SWE:SPAC LIN\n')
    serKeithleyLV.write(':TRIG:COUN ' + number_steps+'\n') # number of points to measure
    serKeithleyLV.write(':SOUR:DEL ' + source_delay+'\n') # source delay in sec
    serKeithleyLV.write(':OUTP ON\n') #starts the sweep
    serKeithleyLV.write(':INIT\n')
    serKeithleyLV.write(':READ?\n') #requests the data from the 2440
    
    # get all of the data out
    a = serKeithleyLV.readline() #super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
    a = a.split(',') #turns this into an array instead of a string with a bunch of commas
    print a
    
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
    RS_MIN = min(DIVoutput[1:-1,2])
    print RS_MIN
    print DIVoutput
    return DIVoutput, RS_MIN, terminal

def DIVRsh(voltage_protection=str(10), start_current=str(0.00011), \
stop_current=str(0.00001),current_step = str(-1e-5),number_steps = str(11),\
number_steps_int = int(number_steps),source_delay = str(0.01)):
    global serKeithleyLV
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = 57600
    serKeithleyLV.port = '/dev/ttyUSB1'
    serKeithleyLV.timeout = timeout_sec
    print timeout_sec

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
    serKeithleyLV.write(':SENS:VOLT:PROT '+ voltage_protection+'\n')
    serKeithleyLV.write(':SOUR:CURR:STAR '+ start_current+'\n') # start current
    serKeithleyLV.write(':SOUR:CURR:STOP '+ stop_current+'\n') # stop current
    serKeithleyLV.write(':SOUR:CURR:STEP ' + current_step+'\n') #increment
    serKeithleyLV.write(':SOUR:CURR:MODE SWE\n')
    serKeithleyLV.write(':SOUR:SWE:RANG:AUTO 1\n')
    serKeithleyLV.write(':SOUR:SWE:SPAC LIN\n')
    serKeithleyLV.write(':TRIG:COUN ' + number_steps+'\n') # number of points to measure
    serKeithleyLV.write(':SOUR:DEL ' + source_delay+'\n') # source delay in sec
    serKeithleyLV.write(':OUTP ON\n') #starts the sweep
    serKeithleyLV.write(':INIT\n')
    serKeithleyLV.write(':READ?\n') #requests the data from the 2440
    
    # get all of the data out
    a = serKeithleyLV.readline() #super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
    a = a.split(',') #turns this into an array instead of a string with a bunch of commas
    print a
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
    RSH_MEAN = np.mean(DIVoutput[1:-1,2])
    print DIVoutput
    print RSH_MEAN
    return DIVoutput, RSH_MEAN, terminal

def HVBias(current_protection=str(10E-4), \
source_delay = str(0.01), Bias = str(1000)):
    global serKeithleyHV
    serKeithleyHV = serial.Serial()
    serKeithleyHV.baudrate = 57600
    serKeithleyHV.port = '/dev/ttyUSB0'
    serKeithleyHV.timeout = timeout_sec
    print timeout_sec
    serKeithleyHV.close()
    serKeithleyHV.open()
    
    serKeithleyHV.write(':OUTP OFF\n')
    serKeithleyHV.write('*RST\n')
    time.sleep(2)
    serKeithleyHV.write(':ROUT:TERM REAR\n')
    serKeithleyHV.write(':ROUT:TERM?\n')
    terminal = (serKeithleyHV.read(10))
    serKeithleyHV.write(':SYST:RSEN OFF\n') # chooses 4wire measurement setting
    serKeithleyHV.write(':SOUR:FUNC VOLT\n')
    serKeithleyHV.write(':SOUR:VOLT:MODE FIX\n')
    serKeithleyHV.write(':SOUR:VOLT:RANG 1000\n')
    serKeithleyHV.write(':SOUR:VOLT:LEV '+Bias+'\n')
    serKeithleyHV.write(':SENS:CURR:PROT '+ current_protection+'\n')
    serKeithleyHV.write(":SENS:FUNC:CONC ON\n")
    serKeithleyHV.write(":SENS:CURR:RANG:AUTO 1\n")
    serKeithleyHV.write(':SOUR:DEL ' + source_delay+'\n') # source delay in sec
    serKeithleyHV.write(':OUTP ON\n') #starts the sweep

    time.sleep(time_per_point*60.0)
    serKeithleyHV.write(':READ?\n') #requests the data from the 2440
    # get all of the data out
    a = serKeithleyHV.readline() #super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
    a = a.split(',') #turns this into an array instead of a string with a bunch of commas
    print a
    # clean up the 2440 and the port (turn off output and close port)
    serKeithleyHV.write(':OUTP OFF\n')
    serKeithleyHV.close() 
    HVoutput = np.zeros((len(a)/5,3))
    
    #Header = ['Voltage (V)', 'Current (A)', 'Resistance (ohm)']

    for i in range(len(a)/5):
        HVoutput[i,0] = a[i*5] # voltages
        HVoutput[i,1] = a[i*5+1] #current
    print HVoutput
    return HVoutput

def main():
    ####################
    print "set up arduino port"
    instring = ""
    serArduino = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
    )
    #####################
    print "set up Keithley port"
    instring = ""
    ##thingsToDo = [1]
    serKeithleyHV = serial.Serial()
    serKeithleyHV.baudrate = 57600
    serKeithleyHV.port = '/dev/ttyUSB0'
    serKeithleyHV.timeout = 1.0
    print serKeithleyHV.timeout
    
    serKeithleyLV = serial.Serial()
    serKeithleyLV.baudrate = 57600
    serKeithleyLV.port = '/dev/ttyUSB1'
    serKeithleyLV.timeout = 1.0
    print serKeithleyLV.timeout
    
    print "make sure ports are closed"
    try:
        serKeithleyHV.close()
        serArduino.close()
    except:
        print "ports not open"

    LV_output_Rs = np.zeros((number_points, 50))
    LV_output_Rsh = np.zeros((number_points, 50))
    
    ##### do some initial setup stuff
    print "open Keithley ports"
    serKeithleyHV
    serKeithleyHV.open()
    serKeithleyHV.flushInput()
    serKeithleyHV.flushOutput()
    serKeithleyHV.write('*RST\n')
    time.sleep(1.0)
    serKeithleyLV
    serKeithleyLV.open()
    serKeithleyLV.flushInput()
    serKeithleyLV.flushOutput()
    serKeithleyLV.write('*RST\n')
    time.sleep(1.0)
    
    print "open arduino port"
    serArduino
    serArduino.open() 
    print "HV Keithley"
    print serKeithleyHV.port   
    print "try to get IDN"
    serKeithleyHV.write('*IDN?\n')
    time.sleep(0.5)
    ident = serKeithleyHV.read(200)
    print "reading ser"
    time.sleep(0.5)
    print ident
    time.sleep(0.5)
    
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
    serKeithleyHV.flushInput()
    serKeithleyHV.flushOutput()
    
    time.sleep(0.001)

    #Read48Current.WriteToFile("Timestamp  " + str(first_time_seconds) +"\n"\
    #"IDN  " + str(ident) +"\n"\
    #,OutputFile=OutputFileMetaData,first_time_seconds=first_time_seconds)
    raw_data_Rs = np.zeros((number_points,number_samples))
    raw_data_Rsh = np.zeros((number_points,number_samples))
    raw_data_HV = np.zeros((number_points,3))
    for i in range(number_points):
        try:
            LV_output_Rs[i,0] = i
            LV_output_Rs[i,1] = round(time.time(), 0) #
            LV_output_Rsh[i,0] = i
            LV_output_Rsh[i,1] = round(time.time(), 0) #
            print i

            if i%points_between_LV == 0:
                
               # 4 wire on first port
                serArduino.write('2O3O4O5O6O7O8O9O14O15O16O17O18O19O20O21O32O33O34O35O36O37O38O39O40O41O42O43O44O45O46O47O')
                time.sleep(0.5)
                serArduino.write('2C32C')
                time.sleep(0.5)
                DIV_Rsh_output, RSH_MEAN, terminal = DIVRsh()
                time.sleep(0.5)
                #raw_data_Rsh[i,0] = DIV_Rsh_output
                DIV_Rs_output, RS_MIN, terminal = DIVRs()
                time.sleep(0.5)
                #raw_data_Rs[i,0] = DIV_Rs_output
                LV_output_Rsh[i,2] = 1
                #LV_output[i,3] = terminal   
                #LV_output[i,4] = RSH_MEAN
                #LV_output[i,5] = RS_MIN         
                serArduino.write('2O32O')
                time.sleep(0.5)
    
               # 4 wire on second port
                serArduino.write('2O3O4O5O6O7O8O9O14O15O16O17O18O19O20O21O32O33O34O35O36O37O38O39O40O41O42O43O44O45O46O47O')
                time.sleep(0.5)
                serArduino.write('3C33C')
                time.sleep(0.5)
                #DIV_Rsh_output, RSH_MEAN, terminal = DIVRsh()
                #time.sleep(0.5)
                #raw_data_Rsh[i,0] = DIV_Rsh_output
                #DIV_Rs_output, RS_MIN, terminal = DIVRs()
                #time.sleep(0.5)
                #raw_data_Rs[i,0] = DIV_Rs_output
                LV_output_Rsh[i,6] = 2
                #LV_output[i,7] = terminal   
                #LV_output[i,8] = RSH_MEAN
                #LV_output[i,9] = RS_MIN         
                serArduino.write('3O33O')
                time.sleep(0.5)
                
               # 4 wire on third port
                serArduino.write('2O3O4O5O6O7O8O9O14O15O16O17O18O19O20O21O32O33O34O35O36O37O38O39O40O41O42O43O44O45O46O47O')
                time.sleep(0.5)
                serArduino.write('4C34C')
                time.sleep(0.5) 
                #DIV_Rsh_output, RSH_MIN, terminal = DIVRsh()
                #time.sleep(0.5)
                #raw_data_Rsh[i,0] = DIV_Rsh_output
                #DIV_Rs_output, RS_MIN, terminal = DIVRs()
                #time.sleep(0.5)
                #raw_data_Rs[i,0] = DIV_Rs_output
                LV_output_Rsh[i,10] = 3
                #LV_output[i,11] = terminal  
                #LV_output[i,12] = RSH_MIN
                #LV_output[i,13] = RS_MIN            
                serArduino.write('4O34O')
                time.sleep(0.5)

            else:
                #raw_data_HV[i,0] = float(i)
                #raw_data_HV[i,1] = time.time()
                print "try to set and read hv bias"
                raw_data_HV = HVBias()
                print raw_data_HV
                Read48Current.getCURRENT(i,number_points,first_time_seconds)
        except:
            print "Exception:"
            traceback.print_exc()
            pass
            break
        time.sleep(time_per_point*60) #Waits for the next time point
    serKeithleyHV.close()
    serArduino.close()
    
if __name__ == "__main__":
   main()

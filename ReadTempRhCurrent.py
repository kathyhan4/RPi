import sys
sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/Adafruit/Adafruit_I2C")
sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/Adafruit/Adafruit_ADS1x15")

import time
import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import RPi.GPIO as GPIO
#from htu21d import HTU21D

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15

sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/HTU21D")
import HTU21D

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
#Output file
OutputFile = '/home/pi/Desktop/RPiData/DH_HV_DIV/TRH'



ResistanceA = 100000.0 # resistance of shunt in first board
ResistanceB = 100000.0 # resistance of shunt in second board
ResistanceC = 100000.0 # resistance of shunt in third board
ResistanceD = 100000.0 # resistance of shunt in fourth board
ResistanceE = -100000.0 # resistance of shunt in fifth board
ResistanceF = 10000000.0 # resistance of shunt in sixth board

Header = ['timepoint', 'time', 'hours', 'T1 (deg C)', '%RH1', 'T2 (deg C)', '%RH2',\
'I1 (nA)', 'I2 (nA)', 'I3 (nA)', 'I4 (nA)', 'I5 (nA)', 'I6 (nA)',\
'I7 (nA)', 'I8 (nA)', 'I9 (nA)', 'I10(nA)', 'I11(nA)', 'I12(nA)',\
'I13(nA)', 'I14(nA)', 'I15(nA)', 'I16(nA)', 'I17(nA)', 'I18(nA)',\
'I19(nA)', 'I20(nA)', 'I21(nA)', 'I22(nA)', 'I23(nA)', 'I24(nA)',\
'I25(nA)', 'I26(nA)', 'I27(nA)', 'I28(nA)', 'I29(nA)', 'I30(nA)',\
'I31(nA)', 'I32(nA)', 'I33(nA)', 'I34(nA)', 'I35(nA)', 'I36(nA)',\
'I37(nA)', 'I38(nA)', 'I39(nA)', 'I40(nA)', 'I41(nA)', 'I42(nA)',\
'I43(nA)', 'I44(nA)', 'I45(nA)', 'I46(nA)', 'I47(nA)', 'I48(nA)']  

def setgain(ADCaddress, ADCport):

    ADS1115 = 0x01  # 16-bit ADC
    
    gain = 6144

    sps = 32   # 32 samples per second

    adc = ADS1x15(ic=ADS1115,address=ADCaddress)
    
    volts = adc.readADCSingleEnded(ADCport, gain, sps) / 1000   
     
    if volts < 0.256:
        gain = 256
    elif 0.256 <= volts < 0.512:
        gain = 512
    elif 0.512 <= volts < 1.024:
        gain = 1024
    elif 1.024 <= volts < 2.048:
         gain = 2048
    elif 2.048 <= volts < 4.096:
        gain = 4096
    else:
        gain = 6144
    #print gain
    return gain
    
def GetVolts( ADCaddress, ADCport ):
    # ADCaddress is 0x4a for ADR-GND, 0x4b for ADR-VDD, 0x4b for ADR-SDA, 0x4B for ADR-SCL
    #ADCport is 0, 1, 2, or 3 for A0, A1, A2, or A3 on the ADC
    ADS1015 = 0x00  # 12-bit ADC
    ADS1115 = 0x01  # 16-bit ADC
    
    gain = setgain( ADCaddress, ADCport )
    
    # Select the sample rate
    # sps = 8    # 8 samples per second
    #sps = 16   # 16 samples per second
    sps = 32   # 32 samples per second # this seems to be the fastest consistently reporting speed -Kat 7-26-15
    #sps = 64   # 64 samples per second
    #sps = 128  # 128 samples per second
    # sps = 250  # 250 samples per second
    #sps = 475  # 475 samples per second
    # sps = 860  # 860 samples per second
    
    # Initialise the ADC using the default mode (use default I2C address)
    # Set this to ADS1015 or ADS1115 depending on the ADC you are using!
    adc = ADS1x15(ic=ADS1115,address=ADCaddress)
    #volts_1 = 0 
    # Read channel 0 in single-ended mode using the settings above
    #for i in range(100):
        
        #volts_2 = adc.readADCSingleEnded(ADCport, gain, sps) / 1000

    #for i in range(100):
        
        #volts_2 = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        #volts_1 = volts_1+volts_2
        #volts = volts_1/100.
    for k in range(3):
        volts = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        #print volts
    for l in range(3):
        volts1 = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        volts2 = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        volts3 = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        volts = (volts1 + volts2 + volts3)/(3)
        #print volts1 
        #print volts2 
        #print volts3 
        #print volts    
    #volts = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
    #print volts
    #voltstoaverage=0
    #for k in range(20):
        #volt = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
        #print volt
        #voltstoaverage = voltstoaverage + volt
    #print k
    #volts = voltstoaverage / (k+1) 
    #print()
    #print volts
    #print()
        # To read channel 3 in single-ended mode, +/- 1.024V, 860 sps use:
    # volts = adc.readADCSingleEnded(3, 1024, 860)

    #print "%.6f" % (volts)
    #print(volts)
    return volts

#OutputFilePath = '/home/pi/Desktop/RPiData/TempHumidity/' 

def WriteToFile(message,OutputFile,first_time_seconds):
    file = open(OutputFile+first_time_seconds+'.csv', 'a')
    file.write(message)
    file.close()
    
#Pin assignments
PIN_MUX_ADDR_B0 = 17
PIN_MUX_ADDR_B1 = 27
PIN_MUX_ADDR_B2 = 22 
PIN_LED0 = 18
PIN_LED1 = 23
PIN_LED2 = 24
PIN_LED3 = 25
PIN_LED4 = 12
PIN_LED5 = 16
PIN_LED6 = 20
PIN_LED7 = 21

#Dictionaries
muxAddress={0:'000',1:'001',2:'010',3:'011',4:'100',5:'101',6:'110',7:'111'}
ledAddress={0:'00000001',1:'00000010',2:'00000100',3:'00001000',4:'00010000',5:'00100000',6:'01000000',7:'10000000',8:'00000000'}
###=====================FUNCTIONS=======================================

def setupGPIOPins():
    GPIO.setup(PIN_MUX_ADDR_B0, GPIO.OUT, initial=0)
    GPIO.setup(PIN_MUX_ADDR_B1, GPIO.OUT, initial=0)
    GPIO.setup(PIN_MUX_ADDR_B2, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED0, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED1, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED2, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED3, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED4, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED5, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED6, GPIO.OUT, initial=0)
    GPIO.setup(PIN_LED7, GPIO.OUT, initial=0)


def cleanGPIOPins():
    GPIO.cleanup(PIN_MUX_ADDR_B2)
    GPIO.cleanup(PIN_MUX_ADDR_B1)
    GPIO.cleanup(PIN_MUX_ADDR_B0)
    GPIO.cleanup(PIN_LED0)
    GPIO.cleanup(PIN_LED1)
    GPIO.cleanup(PIN_LED2)
    GPIO.cleanup(PIN_LED3)
    GPIO.cleanup(PIN_LED4)
    GPIO.cleanup(PIN_LED5)
    GPIO.cleanup(PIN_LED6)
    GPIO.cleanup(PIN_LED7)

def setMuxAddress(Address):
    GPIO.output(PIN_MUX_ADDR_B0,int(muxAddress[Address][2]))
    GPIO.output(PIN_MUX_ADDR_B1,int(muxAddress[Address][1]))
    GPIO.output(PIN_MUX_ADDR_B2,int(muxAddress[Address][0]))

def setLED(Address):
    GPIO.output(PIN_LED0,int(ledAddress[Address][7]))
    GPIO.output(PIN_LED1,int(ledAddress[Address][6]))
    GPIO.output(PIN_LED2,int(ledAddress[Address][5]))
    GPIO.output(PIN_LED3,int(ledAddress[Address][4]))
    GPIO.output(PIN_LED4,int(ledAddress[Address][3]))
    GPIO.output(PIN_LED5,int(ledAddress[Address][2]))
    GPIO.output(PIN_LED6,int(ledAddress[Address][1]))
    GPIO.output(PIN_LED7,int(ledAddress[Address][0]))

def getTRHCurrent(i,number_points,first_time_seconds, NUMBER_SAMPLES):    
    #Initializes variables
    TimeTempHumidity = numpy.zeros((number_points, 55))
    SliceNumber = 0
    SliceLocation = 0
    
    #Sets up the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    cleanGPIOPins()
    setupGPIOPins()
    
    
    timepoint = i
        
    if timepoint == 0:
        #Gets the timestamp of the first data pointif 
        #first_time_seconds = str('%.0f' % round(time.time(), 1)) #
        WriteToFile(str(Header[0]) + "," + str(Header[1]) + "," + str(Header[2]) + "," + str(Header[3]) + "," + \
        str(Header[4]) + "," + str(Header[5]) + "," + str(Header[6]) + "," + str(Header[7]) + "," + \
        str(Header[8]) + "," + str(Header[9]) + "," + str(Header[10]) + "," + str(Header[11]) + "," + \
        str(Header[12]) + "," + str(Header[13]) + "," + str(Header[14]) + "," + str(Header[15]) + "," + \
        str(Header[16]) + "," + str(Header[17]) + "," + str(Header[18]) + "," + str(Header[19]) + "," + \
        str(Header[20]) + "," + str(Header[21]) + "," + str(Header[22]) + "," + str(Header[23]) + "," + \
        str(Header[24]) + "," + str(Header[25]) + "," + str(Header[26]) + "," + str(Header[27]) + "," + \
        str(Header[28]) + "," + str(Header[29]) + "," + str(Header[30]) + "," + str(Header[31]) + "," + \
        str(Header[32]) + "," + str(Header[33]) + "," + str(Header[34]) + "," + str(Header[35]) + "," + \
        str(Header[36]) + "," + str(Header[37]) + "," + str(Header[38]) + "," + str(Header[39]) + "," + \
        str(Header[40]) + "," + str(Header[41]) + "," + str(Header[42]) + "," + str(Header[43]) + "," + \
        str(Header[44]) + "," + str(Header[45]) + "," + str(Header[46]) + "," + str(Header[47]) + "," + \
        str(Header[48]) + "," + str(Header[49]) + "," + \
        str(Header[50]) + "," + str(Header[51]) + "," + \
        str(Header[52]) + "," + str(Header[53]) + "," + str(Header[54]) + \
        "," +"\n",OutputFile,first_time_seconds)

            
    #Main loop
    #for i in range(0,int(number_points)):
    TimeTempHumidity[i,0] = numpy.round(i,decimals=0)
    TimeTempHumidity[i,1] = time.time()
    TimeTempHumidity[i,2] = (TimeTempHumidity[i,1]-TimeTempHumidity[0,1])/3600
    max_chanel = int(math.floor(float(NUMBER_SAMPLES-1)/8.0)+3)
    print i
    for Channel in range(0,max_chanel):
    # Sensor port 1, LED 1
        setLED(Channel)
        setMuxAddress(Channel)
    
        if Channel < 2:
            
            #Resets the sensor
            HTU21D.htu_reset
            
            #Reads the temperature and humidity
            temp = HTU21D.read_temperature()
            hum = HTU21D.read_humidity()
    
            #Stores the temperature and humidity data
            TimeTempHumidity[i,3+Channel*2] = numpy.round(temp,decimals=1)
            TimeTempHumidity[i,4+Channel*2] = numpy.round(hum,decimals=1)
            
        #elif Channel == 2: # current sense boards must be in ports 6 through 8!
            #volts0 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            #Current0 = round((volts0) / ResistanceA * 1000000000., 2) #current in nA for 10 M ohm current shunt, 350 nA max, 1 nA min
            #TimeTempHumidity[i,7]=Current0
            
            #volts1 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            #Current1 = round((volts1) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,8]=Current1
             
            #volts2 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            #Current2 = round((volts2) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,9]=Current2
             
            #volts3 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            #Current3 = round((volts3) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,10]=Current3
            
            #volts4 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            #Current4 = round((volts4) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,11]=Current4
            
            #volts5 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            #Current5 = round((volts5) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,12]=Current5
             
            #volts6 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            #Current6 = round((volts6) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,13]=Current6
            
            #volts7 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            #Current7 = round((volts7) / ResistanceA * 1000000000., 2) #current in nA
            #TimeTempHumidity[i,14]=Current7         
              
        elif Channel == 3: # current sense boards must be in ports 6 through 8!
            volts8 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            Current8 = round((volts8) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,15]=Current8
            
            volts9 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            Current9 = round((volts9) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,16]=Current9
             
            volts10 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            Current10 = round((volts10) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,17]=Current10
             
            volts11 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            Current11 = round((volts11) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,18]=Current11
            
            volts12 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            Current12 = round((volts12) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,19]=Current12
            
            volts13 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            Current13 = round((volts13) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,20]=Current13
             
            volts14 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            Current14 = round((volts14) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,21]=Current14
            
            volts15 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            Current15 = round((volts15) / ResistanceB * 1000000000., 2) #current in nA
            TimeTempHumidity[i,22]=Current15            
            
        elif Channel == 4: # current sense boards must be in ports 6 through 8!
            volts16 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            Current16 = round((volts16) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,23]=Current16
            
            volts17 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            Current17 = round((volts17) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,24]=Current17
             
            volts18 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            Current18 = round((volts18) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,25]=Current18
             
            volts19 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            Current19 = round((volts19) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,26]=Current19
            
            volts20 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            Current20 = round((volts20) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,27]=Current20
            
            volts21 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            Current21 = round((volts21) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,28]=Current21
             
            volts22 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            Current22 = round((volts22) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,29]=Current22
            
            volts23 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            Current23 = round((volts23) / ResistanceC * 1000000000., 2) #current in nA
            TimeTempHumidity[i,30]=Current23
            
        elif Channel == 5: # current sense boards must be in ports 6 through 8!
            volts24 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            Current24 = round(volts24 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,31]=volts24
            
            volts25 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            Current25 = round(volts25 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,32]=Current25
             
            volts26 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            Current26 = round(volts26 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,33]=Current26
             
            volts27 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            Current27 = round(volts27 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,34]=Current27
            
            volts28 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            Current28 = round(volts28 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,35]=Current28
            
            volts29 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            Current29 = round(volts29 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,36]=Current29
             
            volts30 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            Current30 = round(volts30 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,37]=Current30
            
            volts31 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            Current31 = round(volts31 / ResistanceD * 1000000000., 2) #current in nA
            TimeTempHumidity[i,38]=Current31
            
        elif Channel == 6: # 
            volts16 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            Current16 = round(volts16 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,39]=Current16
            
            volts17 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            Current17 = round(volts17 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,40]=Current17
             
            volts18 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            Current18 = round(volts18 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,41]=Current18
             
            volts19 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            Current19 = round(volts19 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,42]=Current19
            
            volts20 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            Current20 = round(volts20 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,43]=Current20
            
            volts21 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            Current21 = round(volts21 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,44]=Current21
             
            volts22 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            Current22 = round(volts22 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,45]=Current22
            
            volts23 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            Current23 = round(volts23 / ResistanceE * 1000000000., 2) #current in nA
            TimeTempHumidity[i,46]=Current23
            
        elif Channel == 7: # current sense boards must be in ports 6 through 8!
            volts24 = GetVolts( ADCaddress=0x4b, ADCport=0 )
            Current24 = round(volts24 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,47]=Current24
            
            volts25 = GetVolts( ADCaddress=0x4b, ADCport=1 )
            Current25 = round(volts25 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,48]=Current25
             
            volts26 = GetVolts( ADCaddress=0x4b, ADCport=2 )
            Current26 = round(volts26 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,49]=Current26
             
            volts27 = GetVolts( ADCaddress=0x4b, ADCport=3 )
            Current27 = round(volts27 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,50]=Current27
            
            volts28 = GetVolts( ADCaddress=0x4a, ADCport=0 )
            Current28 = round(volts28 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,51]=Current28
            
            volts29 = GetVolts( ADCaddress=0x4a, ADCport=1 )
            Current29 = round(volts29 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,52]=Current29
             
            volts30 = GetVolts( ADCaddress=0x4a, ADCport=2 )
            Current30 = round(volts30 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,53]=Current30
            
            volts31 = GetVolts( ADCaddress=0x4a, ADCport=3 )
            Current31 = round(volts31 / ResistanceF * 1000000000., 2) #current in nA
            TimeTempHumidity[i,54]=Current31
        else:
            print('out of bounds for port')
        setLED(8)    
    #       GPIO.cleanup(21)
    
    #Sleeps for 1ms to let HTU21D breathe
    time.sleep(0.001)
    
    for g in range(1,3):
        print("Port: %3.0f Temperature: %4.1f deg C ") % (g,TimeTempHumidity[i,1+g*2])
        print("Port:  %2.0f Humidity:    %4.1f percent RH ") % (g,TimeTempHumidity[i,2+g*2])
    for g in range(1,49):       
        print("Sample: %2.0f Current: %4.5f nA ") % (g,TimeTempHumidity[i,6+g])
    
        
    #Writes a line of data to the file
    WriteToFile(str(TimeTempHumidity[i,0]) + "," + str(TimeTempHumidity[i,1]) + "," + str(TimeTempHumidity[i,2]) + "," + str(TimeTempHumidity[i,3]) + "," + \
    str(TimeTempHumidity[i,4]) + "," + str(TimeTempHumidity[i,5]) + "," + str(TimeTempHumidity[i,6]) + "," + str(TimeTempHumidity[i,7]) + "," + \
    str(TimeTempHumidity[i,8]) + "," + str(TimeTempHumidity[i,9]) + "," + str(TimeTempHumidity[i,10]) + "," + str(TimeTempHumidity[i,11]) + "," + \
    str(TimeTempHumidity[i,12]) + "," + str(TimeTempHumidity[i,13]) + "," + str(TimeTempHumidity[i,14]) + "," + str(TimeTempHumidity[i,15]) + "," + \
    str(TimeTempHumidity[i,16]) + "," + str(TimeTempHumidity[i,17]) + "," + str(TimeTempHumidity[i,18]) + "," + str(TimeTempHumidity[i,19]) + "," + \
    str(TimeTempHumidity[i,20]) + "," + str(TimeTempHumidity[i,21]) + "," + str(TimeTempHumidity[i,22]) + "," + str(TimeTempHumidity[i,23]) + "," + \
    str(TimeTempHumidity[i,24]) + "," + str(TimeTempHumidity[i,25]) + "," + str(TimeTempHumidity[i,26]) + "," + str(TimeTempHumidity[i,27]) + "," + \
    str(TimeTempHumidity[i,28]) + "," + str(TimeTempHumidity[i,29]) + "," + str(TimeTempHumidity[i,30]) + "," + str(TimeTempHumidity[i,31]) + "," + \
    str(TimeTempHumidity[i,32]) + "," + str(TimeTempHumidity[i,33]) + "," + str(TimeTempHumidity[i,34]) + "," + str(TimeTempHumidity[i,35]) + "," + \
    str(TimeTempHumidity[i,36]) + "," + str(TimeTempHumidity[i,37]) + "," + str(TimeTempHumidity[i,38]) + "," + str(TimeTempHumidity[i,39]) + "," + \
    str(TimeTempHumidity[i,40]) + "," + str(TimeTempHumidity[i,41]) + "," + str(TimeTempHumidity[i,42]) + "," + str(TimeTempHumidity[i,43]) + "," + \
    str(TimeTempHumidity[i,44]) + "," + str(TimeTempHumidity[i,45]) + "," + str(TimeTempHumidity[i,46]) + "," + str(TimeTempHumidity[i,47]) + "," + \
    str(TimeTempHumidity[i,48]) + "," + str(TimeTempHumidity[i,49]) + "," + str(TimeTempHumidity[i,50]) + "," + str(TimeTempHumidity[i,51]) + "," + \
    str(TimeTempHumidity[i,52]) + "," + str(TimeTempHumidity[i,53]) + "," + str(TimeTempHumidity[i,54]) + "," + "\n",OutputFile,first_time_seconds)
    
    
    print ""
    #return first_time_seconds
#getCURRENT(i, number_points)    

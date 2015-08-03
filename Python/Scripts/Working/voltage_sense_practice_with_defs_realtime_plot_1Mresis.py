import sys
sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/Adafruit/Adafruit_I2C")
sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/Adafruit/Adafruit_ADS1x15")

import time
import math
import numpy
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import RPi.GPIO as GPIO
#from htu21d import HTU21D

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

#def calc_dew_pt(temp_c, rel_hum):
 #   A, B, C = 8.1332, 1762.39, 235.66
#
 #   pp_amb = 10 ** (A - (B / (temp_c + C)))
  #  return -(C + (B / (math.log10(rel_hum * pp_amb / 100) - A ))), pp_amb

run_length = float(1000) #time to collect data in hours
time_per_point = float(10)/60 # time between data pionts in minutes
number_points = run_length * 60 / time_per_point

#DataSliceTime = 1/120 # save data every (this number) of hours
#PointsPerSlice = DataSliceTime * 60 / time_per_point
#NumberSlices = run_length / DataSliceTime

def setgain(ADCaddress, ADCport):

    ADS1115 = 0x01  # 16-bit ADC
    
    # Select the gain
    # gain = 6144  # +/- 6.144V
    # gain = 4096  # +/- 4.096V
    # gain = 2048  # +/- 2.048V
    # gain = 1024  # +/- 1.024V
    # gain = 512   # +/- 0.512V
    # gain = 256   # +/- 0.256V
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

    return gain
    
def GetVolts( ADCaddress, ADCport ):
    # ADCaddress is 0x48 for ADR-GND, 0x49 for ADR-VDD, 0x4A for ADR-SDA, 0x4B for ADR-SCL
    #ADCport is 0, 1, 2, or 3 for A0, A1, A2, or A3 on the ADC
    ADS1015 = 0x00  # 12-bit ADC
    ADS1115 = 0x01  # 16-bit ADC
    
    gain = setgain( ADCaddress, ADCport )
    
    # Select the sample rate
    # sps = 8    # 8 samples per second
    # sps = 16   # 16 samples per second
    sps = 32   # 32 samples per second # this seems to be the fastest consistently reporting speed -Kat 7-26-15
    # sps = 64   # 64 samples per second
    # sps = 128  # 128 samples per second
    # sps = 250  # 250 samples per second
    # sps = 475  # 475 samples per second
    # sps = 860  # 860 samples per second
    
    # Initialise the ADC using the default mode (use default I2C address)
    # Set this to ADS1015 or ADS1115 depending on the ADC you are using!
    adc = ADS1x15(ic=ADS1115,address=ADCaddress)
    
    # Read channel 0 in single-ended mode using the settings above
    volts = adc.readADCSingleEnded(ADCport, gain, sps) / 1000
    
    # To read channel 3 in single-ended mode, +/- 1.024V, 860 sps use:
    # volts = adc.readADCSingleEnded(3, 1024, 860)

    #print "%.6f" % (volts)
    #print(volts)
    return volts

Current100Mohm = numpy.zeros((number_points, 11))
SliceNumber = 0
SliceLocation = 0

#OutputFilePath = '/home/pi/Desktop/TempHumidityData/' 

def WriteToFile(message):
    file = open(OutputFile+first_time_seconds+'.csv', 'a')
    file.write(message)
    file.close()
    
##Initializes plot (18x10 inches)
fig = plt.figure(figsize=(18, 10), dpi=80)
ax1 = fig.add_subplot(241)
ax2 = fig.add_subplot(242)
ax3 = fig.add_subplot(243)
ax4 = fig.add_subplot(244)
ax5 = fig.add_subplot(245)
ax6 = fig.add_subplot(246)
ax7 = fig.add_subplot(247)
ax8 = fig.add_subplot(248)

# draw and show it
plt.show(block=False)
    
for i in range(0,int(number_points)):
    
    if __name__ == '__main__':
        
        # Sensor port 8
        GPIO.setup(22, GPIO.OUT, initial=1)
        GPIO.setup(27, GPIO.OUT, initial=1)
        GPIO.setup(17, GPIO.OUT, initial=1)
        GPIO.setup(18, GPIO.OUT, initial=0)
        GPIO.setup(23, GPIO.OUT, initial=0)
        GPIO.setup(24, GPIO.OUT, initial=0)
        GPIO.setup(25, GPIO.OUT, initial=0)
        GPIO.setup(12, GPIO.OUT, initial=0)
        GPIO.setup(16, GPIO.OUT, initial=0)
        GPIO.setup(20, GPIO.OUT, initial=0)
        GPIO.setup(21, GPIO.OUT, initial=1)
        
        Current100Mohm[i,0]=i
        currenttime=time.time()
        Current100Mohm[i,1]=currenttime
        Current100Mohm[i,10]=round((Current100Mohm[i,1]-Current100Mohm[0,1])/3600., 3)

        volts0 = GetVolts( ADCaddress=0x49, ADCport=0 )
        Current0 = round(volts0 / 1000000. * 1000000000., 0) #current in nA
        Current100Mohm[i,2]=Current0
        
        volts1 = GetVolts( ADCaddress=0x49, ADCport=1 )
        Current1 = round(volts1 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,3]=Current1
         
        volts2 = GetVolts( ADCaddress=0x49, ADCport=2 )
        Current2 = round(volts2 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,4]=Current2
         
        volts3 = GetVolts( ADCaddress=0x49, ADCport=3 )
        Current3 = round(volts3 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,5]=Current3
        
        volts4 = GetVolts( ADCaddress=0x48, ADCport=0 )
        Current4 = round(volts4 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,6]=Current4
        
        volts5 = GetVolts( ADCaddress=0x48, ADCport=1 )
        Current5 = round(volts5 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,7]=Current5
         
        volts6 = GetVolts( ADCaddress=0x48, ADCport=2 )
        Current6 = round(volts6 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,8]=Current6
        
        volts7 = GetVolts( ADCaddress=0x48, ADCport=3 )
        Current7 = round(volts7 / 1000000. * 1000000000.) #current in nA
        Current100Mohm[i,9]=Current7

        print["%5.0f" % val for val in (Current100Mohm[i,:])]
        #print(Current100Mohm[i,2])         
        GPIO.cleanup(22)
        GPIO.cleanup(27)
        GPIO.cleanup(17)
        GPIO.cleanup(18)
        GPIO.cleanup(23)
        GPIO.cleanup(24)
        GPIO.cleanup(25)
        GPIO.cleanup(12)
        GPIO.cleanup(16)
        GPIO.cleanup(20)
        GPIO.cleanup(21)
        
        first_time_seconds = str(math.floor(Current100Mohm[0,1]))
        OutputFile = '/home/pi/Desktop/RPiData/LeakageCurrent'
        WriteToFile(str(Current100Mohm[i,0]) + "," + str(Current100Mohm[i,1]) + "," + str(Current100Mohm[i,2]) + "," + str(Current100Mohm[i,3]) + "," + \
        str(Current100Mohm[i,4]) + "," + str(Current100Mohm[i,5]) + "," + str(Current100Mohm[i,6]) + "," + str(Current100Mohm[i,7]) + "," + \
        str(Current100Mohm[i,8]) + "," + str(Current100Mohm[i,9]) + "," + "\n")

        #Plot the data
        #ax1 = plt.subplot(241)
        li, = ax1.plot(Current100Mohm[:,10],Current100Mohm[:,2],'bo',markersize=8)
        plt.title("Channel 1",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax2 = plt.subplot(242)
        li, = ax2.plot(Current100Mohm[:,10],Current100Mohm[:,3],'bo',markersize=8)
        plt.title("Channel 2",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax2.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax3 = plt.subplot(243)
        li, = ax3.plot(Current100Mohm[:,10],Current100Mohm[:,4],'bo',markersize=8)
        plt.title("Channel 3",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax3.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax4 = plt.subplot(244)
        li, = ax4.plot(Current100Mohm[:,10],Current100Mohm[:,5],'bo',markersize=8)
        plt.title("Channel 4",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax4.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax5 = plt.subplot(245)
        li, = ax5.plot(Current100Mohm[:,10],Current100Mohm[:,6],'bo',markersize=8)
        plt.title("Channel 5",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax5.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax6 = plt.subplot(246)
        li, = ax6.plot(Current100Mohm[:,10],Current100Mohm[:,7],'bo',markersize=8)
        plt.title("Channel 6",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax6.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax7 = plt.subplot(247)
        li, = ax7.plot(Current100Mohm[:,10],Current100Mohm[:,8],'bo',markersize=8)
        plt.title("Channel 7",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax7.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax8 = plt.subplot(248)
        li, = ax8.plot(Current100Mohm[:,10],Current100Mohm[:,9],'bo',markersize=8)
        plt.title("Channel 8",fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("Leakage Current (nA)", fontsize=12)
        ax8.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))    
        fig.canvas.draw()
                    
        ##Draws the plot
        #plt.draw()        
        
        time.sleep(time_per_point*60)        
#        axes = plt.gca()
#        ax1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))    
#    numpy.savetxt('/home/pi/Desktop/LeakageCurrentData/DataSlices/Current'+first_time_seconds+'_'+str(i)+'.txt',Current100MohmSlice)

#    temp_f = temp * 9/5 + 32
#    dew_pt, pp_amb = calc_dew_pt(temp, hum)

#first_time_seconds = str(math.floor(Current100Mohm[0,1]))

#numpy.savetxt('/home/pi/Desktop/LeakageCurrentData/LeakageCurrent'+first_time_seconds+'.txt',Current100Mohm)
#numpy.savetxt('Current100Mohm_'+repr(round(Current100Mohm[1,1])+'.txt'),Current100Mohm)

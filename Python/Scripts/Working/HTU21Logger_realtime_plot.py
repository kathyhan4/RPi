import sys
sys.path.append("/home/pi/Desktop/RPi/Python/Libraries/HTU21D")
import time
import math
import numpy
import time
import RPi.GPIO as GPIO
import HTU21D
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

###=====================GLOBAL DECLARATIONS=============================

#Run length
run_length = float(1)/60 #time to collect data in hours
time_per_point = float(1)/60 # time between data pionts in minutes
number_points = run_length * 60 / time_per_point

#Output file
OutputFile = '/home/pi/Desktop/RPiData/TempHumidity/TRHData'

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
ledAddress={0:'00000000',1:'00000010',2:'00000100',3:'00001000',4:'00010000',5:'00100000',6:'01000000',7:'10000000'}
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

def WriteToFile(message, OutputFile):
    file = open(OutputFile+first_time_seconds+'.csv', 'a')
    file.write(message)
    file.close()
    
#def init_plot():
    #plt.ion()
    #plt.figure()
    #plt.title("Real time data",fontsize=20)
    #plt.xlabel("Time (hours)", fontsize=20)
    #plt.ylabel("%RH or Temperature Deg. C", fontsize=20)
    #plt.grid(True)

#def continuous_plot(x,fx,x2,fx2):
    #plt.plot(x,fx,'bo',markersize=8)
    #plt.plot(x2,fx2,'ro',markersize=8)
    #plt.draw()
##======================MAIN FUNCTION===================================

#Initializes variables
TimeTempHumidity = numpy.zeros((number_points, 33))
SliceNumber = 0
SliceLocation = 0

#Sets up the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
cleanGPIOPins()
setupGPIOPins()

#Initializes plot (24x12 inches)
plt.figure(figsize=(24, 12), dpi=80)
plt.ion()
plt.show()

#Main loop
for i in range(0,int(number_points)):
    for Channel in range(0,8):
    # Sensor port 1, LED 1
        setLED(Channel)
        setMuxAddress(Channel)

        #Resets the sensor
        HTU21D.htu_reset
        
        #Reads the temperature and humidity
        temp = HTU21D.read_temperature()
        hum = HTU21D.read_humidity()

        #Stores the temperature and humidity data
        TimeTempHumidity[i,0+Channel*4] = numpy.round(i,decimals=0)
        TimeTempHumidity[i,1+Channel*4] = time.time()
        TimeTempHumidity[i,2+Channel*4] = numpy.round(temp,decimals=1)
        TimeTempHumidity[i,3+Channel*4] = numpy.round(hum,decimals=1)
        TimeTempHumidity[i,32] = (TimeTempHumidity[i,1]-TimeTempHumidity[0,1])/3600
        
        #Prints the data for this channel
        print("Channel: %d  Temperature: %3.1fC  Humidity: %3.1f%%" % (Channel+1, temp , hum))
        
        #Plot the data
        ax = plt.subplot(241+Channel)
        plt.plot(TimeTempHumidity[:,32],TimeTempHumidity[:,2+Channel*4],'bo',markersize=8)
        plt.plot(TimeTempHumidity[:,32],TimeTempHumidity[:,3+Channel*4],'ro',markersize=8)
        plt.title("Real time data - Channel " + str(Channel+1),fontsize=20)
        plt.xlabel("Time (hours)", fontsize=12)
        plt.ylabel("%RH or Temperature Deg. C", fontsize=12)
        axes = plt.gca()
        axes.set_ylim([0,100])
        ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        
        #Sleeps for 1ms to let HTU21D breathe
        time.sleep(0.001)
    
    #Draws the plot
    plt.draw()
    
    #Gets the timestamp of the first data point
    first_time_seconds = str(math.floor(TimeTempHumidity[0,1]))
    
    #Writes a line of data to the file
    WriteToFile(str(TimeTempHumidity[i,0]) + "," + str(TimeTempHumidity[i,1]) + "," + str(TimeTempHumidity[i,2]) + "," + str(TimeTempHumidity[i,3]) + "," + \
    str(TimeTempHumidity[i,4]) + "," + str(TimeTempHumidity[i,5]) + "," + str(TimeTempHumidity[i,6]) + "," + str(TimeTempHumidity[i,7]) + "," + \
    str(TimeTempHumidity[i,8]) + "," + str(TimeTempHumidity[i,9]) + "," + str(TimeTempHumidity[i,10]) + "," + str(TimeTempHumidity[i,11]) + "," + \
    str(TimeTempHumidity[i,12]) + "," + str(TimeTempHumidity[i,13]) + "," + str(TimeTempHumidity[i,14]) + "," + str(TimeTempHumidity[i,15]) + "," + \
    str(TimeTempHumidity[i,16]) + "," + str(TimeTempHumidity[i,17]) + "," + str(TimeTempHumidity[i,18]) + "," + str(TimeTempHumidity[i,19]) + "," + \
    str(TimeTempHumidity[i,20]) + "," + str(TimeTempHumidity[i,21]) + "," + str(TimeTempHumidity[i,22]) + "," + str(TimeTempHumidity[i,23]) + "," + \
    str(TimeTempHumidity[i,24]) + "," + str(TimeTempHumidity[i,25]) + "," + str(TimeTempHumidity[i,26]) + "," + str(TimeTempHumidity[i,27]) + "," + \
    str(TimeTempHumidity[i,28]) + "," + str(TimeTempHumidity[i,29]) + "," + str(TimeTempHumidity[i,30]) + "," + str(TimeTempHumidity[i,31]) + "," + "\n",OutputFile)

    #Waits for the next time point
    time.sleep(time_per_point*60)
    print ""

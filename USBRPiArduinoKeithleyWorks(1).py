
import serial
import traceback
import re
import datetime
#import sys
import time



def fileData(data):
   db = MySQLdb.connect("192.168.1.145","superWrite","spaceshipfallsfast","solarHome" )
   #con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

   cur = db.cursor()
   cur.execute("SELECT VERSION()")

   ver = cur.fetchone()

   print "Database version : %s " % ver

   cursor = db.cursor()
   tableName = "solarHome.hottub2"
   names = ""
   values = ""
   oxford = ""
   for key in data:
       names = names + oxford + key
       values = values + oxford + data[key]
       oxford = ','
   qstring = "insert into %s (%s) values (%s);"%(tableName,names,values)
   print "Saying %s"%qstring
   cursor.execute(qstring)
   db.commit()
   result = cursor.fetchall()

   print result
   db.close()


def processString(instring):
   print "I Got stuff: %s"%instring
   got_results = re.search(r'pH,[-+]?([0-9]*\.[0-9]+|[0-9]+),InternalTemp,[-+]?([0-9]*\.[0-9]+|[0-9]+),ExternalTemp,[-+]?([0-9]*\.[0-9]+|[0-9]+)',instring)
   if got_results != None:
       things = got_results.groups()
       if len(things) == 3:
           data = {}
           #YYYY-MM-DD HH:MM:SS
           immediate = '\'' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'\''
           data['entry_datetime'] = immediate
           data['pH'] = things[0]
           data['tubtemp'] = things[1]
           data['airtemp'] = things[2]
           fileData(data)
       else:
           print "Only got %d results"%len(things)
           print things
   else:
       print "Got no result from %s"%instring

def main():
   print "hello"
   #time.sleep(5)
   for i in range(1000):
       try:
           ####################
           instring = ""
           ##thingsToDo = [1]
           serArduino = serial.Serial(
               port='/dev/ttyACM0',
               baudrate=9600,
               #parity=serial.PARITY_ODD,
               #stopbits=serial.STOPBITS_TWO,
               #bytesize=serial.SEVENBITS
           )

           #try:
           
           #######reading
           #while True:
               #while serArduino.inWaiting() > 0:
                   #inchar = serArduino.read(1)
                   #if inchar == '\r':
                       #processString(instring)
                       ##ser.write("C,1\r")
                       #time.sleep(1)

                       #while serArduino.inWaiting()>0:
                           #inchar = serArduino.read(1)
                   #elif inchar == '$':
                       #instring = "$"
                   #else:
                       #instring = instring + inchar
             #########done reading          
                       
       #except:
               #print "*** print_exc:"
               #traceback.print_exc()
           #serArduino.close()
           #    time.sleep(10000)
           #####################
           instring = ""
           ##thingsToDo = [1]
           serKeithley=serial.Serial()
           serKeithley.baudrate = 57600
           serKeithley.port = '/dev/ttyUSB0'
           serKeithley.timeout = 10
           try:
               serKeithley.close()
               serArduino.close()
           except:
               print "ports already closed"
           serArduino.open()
           print "try to turn on/off ports"
           serArduino.write('13C')
           time.sleep(1)
           serArduino.write('13O')
           time.sleep(1)
           serArduino.close()
           #serKeithley = serial.Serial(
               #port='/dev/ttyUSB0',
               #baudrate=9600,
               ##parity=serial.PARITY_ODD,
               ##stopbits=serial.STOPBITS_TWO,
               ##bytesize=serial.SEVENBITS
           #)
           print "open keithley port"
           serKeithley.open()
           serKeithley.flushInput()
           serKeithley.flushOutput()
           serKeithley.write('*RST\n')
           time.sleep(0.1)
           serKeithley.write('*IDN?\n')
           time.sleep(0.1)
           ident = serKeithley.read(200)
           print "reading ser"
           time.sleep(0.5)
           print ident
           serKeithley.write(':ROUT:TERM REAR\n')
           #time.sleep(1)
           #ser.write('13C')
           #try:
           #while True:
               #while serArduino.inWaiting() > 0:
                   #inchar = serArduino.read(1)
                   #if inchar == '\r':
                       #processString(instring)
                       ##ser.write("C,1\r")
                       #time.sleep(1)

                       #while ser.inWaiting()>0:
                           #inchar = serArduino.read(1)
                   #elif inchar == '$':
                       #instring = "$"
                   #else:
                       #instring = instring + inchar
           #except:
           #    print "*** print_exc:"
           #    traceback.print_exc()
           serKeithley.close()
           #serArduino.close()
           #    time.sleep(10000)
       except:
           print "Exception:"
           traceback.print_exc()
           pass
           break



if __name__ == "__main__":
   main()

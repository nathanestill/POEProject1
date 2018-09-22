#      ******************************************************************
#      *                                                                *
#      *                                                                *
#      *    Example Python program that receives data from an Arduino   *
#      *                                                                *
#      *                                                                *
#      ******************************************************************


import serial
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#
# NOTE: While this is running, you can not re-program the Arduino.  You must exit
# this Phython program before downloading a sketch to the Arduino.
#


#
# Set the name of the serial port.  Determine the name as follows:
#	1) From Arduino's "Tools" menu, select "Port"
#	2) It will show you which Port is used to connect to the Arduino
#
# For Windows computers, the name is formatted like: "COM6"
# For Apple computers, the name is formatted like: "/dev/tty.usbmodemfa141"
#
arduinoComPort = "/dev/ttyUSB0"


#
# Set the baud rate
# NOTE1: The baudRate for the sending and receiving programs must be the same!
# NOTE2: Set the baudRate to 115200 for faster communication
#
baudRate = 9600


#
# open the serial port
#
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)


fig = plt.figure() # adds a figure
ax = fig.add_subplot(111, projection='3d') # Makes the figure 3D
# initializes a counter so we know when to stop
Xs = [];
Ys = [];
Zs = [];
counter = 0
#
# main loop to read data from the Arduino, then display it
#
while counter < 1649: # stops when all of the angles have been depleted
  #
  # ask for a line of data from the serial port, the ".decode()" converts the
  # data from an "array of bytes", to a string
  #
  lineOfData = serialPort.readline().decode()
  #
  # check if data was received
  #
  if len(lineOfData) > 0:
    #
    # data was received, convert it into 4 integers
    #
    counter = counter+1 # increments the counter because data was received
    SensorValue, angle1, angle2 = (int(x) for x in lineOfData.split(',')) # receives the data from the Arduino
    Distance = SensorValue / 100.0 # The data was sent as an int multiplied by 100, so it is divided by 100 to get cm
    angle1 = radians(angle1 - 90) # subtracts 90 from each angle to center it
    angle2 = radians(angle2 - 90) # subtracts 90 from each angle to center it
    CoordX = Distance * (-sin(angle1)*cos(angle2)) # Gets the X coordinate with trig
    CoordY = Distance * (sin(angle2)) # gets the Y coordinate with trig
    CoordZ = Distance * (cos(angle1) * cos(angle2)) # gets the Z coordinate with trig
    if (Distance < 35 and Distance > 20):
        Xs.append(CoordX)
        Ys.append(CoordY)
        Zs.append(CoordZ)


    #
    # print the results
    #
    print(Distance) 
    print("{" + str(CoordX) + ", " + str(CoordY) + ", " + str(CoordZ) + "}")

ax.scatter(Xs,Ys,Zs)
ax.set_xlabel('X') # labels the X axis
ax.set_ylabel('Y') # labels the Y axis
ax.set_zlabel('Z') # labels the Z axis

plt.show() # shows the plot

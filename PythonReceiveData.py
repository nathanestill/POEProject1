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
Xs = []
Ys = []
Zs = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
counter = 0
#
# main loop to read data from the Arduino, then display it
#
while counter < 1000:
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
    counter = counter+1
    SensorValue, angle1, angle2 = (int(x) for x in lineOfData.split(','))
    Distance = SensorValue / 100.0
    angle1 = radians(angle1 - 90)
    angle2 = radians(angle2 - 90)
    CoordX = Distance * (-sin(angle1)*cos(angle2))
    CoordY = Distance * (sin(angle2))
    CoordZ = Distance * (cos(angle1) * cos(angle2))
    ax.scatter(CoordX,CoordZ,CoordY)
    
    Xs.append(CoordX)
    Ys.append(CoordY)
    Zs.append(CoordZ)

    #
    # print the results
    #
    print(Distance)
    print("{" + str(CoordX) + ", " + str(CoordY) + ", " + str(CoordZ) + "}")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

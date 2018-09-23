import serial
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


arduinoComPort = "/dev/ttyUSB0" # Sets the usb port that the Arduino is plugged into

baudRate = 9600 # Sets the rate at which data is transferred.

serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1) # Opens the serial Port


Xs = []
Ys = []
Zs = np.random.random((1, 31))

counter = 0 # initializes a counter so we know when to stop

while counter < 31: # stops when all of the angles have been depleted
  #
  # ask for a line of data from the serial port, the ".decode()" converts the
  # data from an "array of bytes", to a string
  #
  lineOfData = serialPort.readline().decode()
  #
  # check if data was received
  #
  if len(lineOfData) > 0:
    counter = counter+1 # increments the counter because data was received
    SensorValue, angle1, angle2 = (int(x) for x in lineOfData.split(',')) # receives the data from the Arduino
    Distance = SensorValue / 100.0 # The data was sent as an int multiplied by 100, so it is divided by 100 to get cm
    angle1 = angle1 - 75
    angle2 = angle2 - 90
    Zs[angle2,angle1] = Distance

plt.imshow(Zs, cmap='hot', interpolation='nearest',extent=[75,105,89,91]) # makes a heat map of the scans
plt.xlabel("Theta in Degrees") 
plt.ylabel("Phi in Degrees")
plt.title("2D Scan of Letter W")
plt.show()

import serial
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


arduinoComPort = "/dev/ttyUSB0" # Sets the usb port that the Arduino is plugged into

baudRate = 9600 # Sets the rate at which data is transferred

serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1) # Opens the serial Port



# Initializes an array of distances to collect
Zs = np.random.random((56, 30))
counter = 0 # initializes a counter so we know when to stop

while counter < 1649: # stops when all of the angles have been depleted, calculated as the number of total angles looked at

  lineOfData = serialPort.readline().decode()

  if len(lineOfData) > 0: # if data is received

    counter = counter+1 # increments the counter because data was received
    SensorValue, angle1, angle2 = (int(x) for x in lineOfData.split(',')) # receives the data from the Arduino
    Distance = SensorValue / 100.0 # The data was sent as an int multiplied by 100, so it is divided by 100 to get cm
    angle1 = angle1 - 75 # indexes the angles at 0
    angle2 = angle2 - 65 # indexes the angles at 0
    Zs[angle2,angle1] = Distance # adds the distance to the two angles 

plt.imshow(Zs, cmap='hot', interpolation='nearest',extent=[75,105,120,65]) # Plots the Heatmap
plt.xlabel("Theta in Degrees")
plt.ylabel("Phi in Degrees")
plt.title("3D Scan of Letter W")
plt.show()
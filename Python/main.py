#Main code of the project, running the fonctionnal part
# coding: utf-8

from driverI2C import *
import time
import grovepi

print("Starting")

#Set up of the buttons : ports 7,4,3 and 2 (3 and 2 are tactils ones)
# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
button = 7

grovepi.pinMode(button,"INPUT")

while True:
    try:
        print(grovepi.digitalRead(button))
        time.sleep(.5)

    except IOError:
        print ("Error")







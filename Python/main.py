#Main code of the project, running the fonctionnal part
# coding: utf-8

#bouton increment : D2 et D3
#bouton ok : D4
#bouton retour : D7 

import driverI2C as LCD
import time
import DriverThermometre as thermo

LCD.effacerText()

LCD.setTextLigne2("    Bienvenue"    )
time.sleep(2)

# while True :
#     température = thermo.ReadTemperature()
#     print(température)
#     LCD.setTextLigne1(str(round(température,2))+' Celsius')

#Set up of the buttons : ports 7,4,3 and 2 (3 and 2 are tactils ones)
# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
button = 4

grovepi.pinMode(button,"INPUT")

while True:
    try:
        print(grovepi.digitalRead(button))
        time.sleep(.5)

    except IOError:
        print ("Error")





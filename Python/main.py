#Main code of the project, running the fonctionnal part
# coding: utf-8

import driverI2C as LCD
import time
import DriverThermometre as thermo


while True :
    température = thermo.ReadTemperature()
        print(température)
        LCD.setTextLigne1(str(round(température),2))





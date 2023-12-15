#Main code of the project, running the fonctionnal part
# coding: utf-8

from driverI2C import *
import time
import DriverThermometre as thermo


while True :
        print(thermo.ReadTemperature())





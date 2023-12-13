# coding: utf-8

from driverI2C import *
import time
import NFCDriver as carte

while True : 
    print(carte.ReadCard())



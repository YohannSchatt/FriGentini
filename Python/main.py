# coding: utf-8

from driverI2C import *
import time
import NFCDriver as carte

uid = carte.ReadCard()
for i in uid : 
    print(i)



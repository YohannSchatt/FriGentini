# GrovePi LED Blink example

import time
from grovepi import *

def TurnOn(LB):
    digitalWrite(LB,1)

def TurnOff(LB):
    digitalWrite(LB,0)

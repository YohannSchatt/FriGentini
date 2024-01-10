# GrovePi LED Blink example

import time
from grovepi import *

pinMode(led,"OUTPUT")
time.sleep(1)

def TurnOn(LB):
    digitalWrite(LB,1)

def TurnOff(LB):
    digitalWrite(LB,0)

# GrovePi LED Blink example
from grovepi import *

def TurnOn(LB):
    digitalWrite(LB,1)

def TurnOff(LB):
    digitalWrite(LB,0)

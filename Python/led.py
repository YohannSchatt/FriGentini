# GrovePi LED Blink example
from grovepi import *

def TurnOn(LB): #Allume la led
    digitalWrite(LB,1)

def TurnOff(LB): #Eteint la led
    digitalWrite(LB,0)

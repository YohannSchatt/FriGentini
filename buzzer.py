#!/usr/bin/python3
#-*- coding: utf-8 -*-

import grovepi as g

def init(pin):
    grovepi.pinMode(pin,"OUTPUT")     

def turnOFF(pin):
    grovepi.analoglWrite(pin,0)

def turnON(pin,puissance):
    assert(0<=puissance<=255)
    grovepi.analogWrite(pin,puissance)

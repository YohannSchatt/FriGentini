#Main code of the project, running the fonctionnal part
# coding: utf-8

#bouton increment : D2 et D3
#bouton ok : D4
#bouton retour : D7 

import driverI2C as LCD
import time
import DriverThermometre as thermo
import grovepi 

buttonOk = 4
buttonBack = 7
buttonPlus = 2
buttonMoins = 3

LCD.effacerText()

LCD.setTextLigne2("    Bienvenue"    )
time.sleep(2)

# while True :
#     température = thermo.ReadTemperature()
#     print(température)
#     LCD.setTextLigne1(str(round(température,2))+' Celsius')
#     print(grovepi.digitalRead(buttonPlus))
#Set up of the buttons : ports 7,4,3 and 2 (3 and 2 are tactils ones)
# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND

grovepi.pinMode(buttonOk,"INPUT")
grovepi.pinMode(buttonBack,"INPUT")
grovepi.pinMode(buttonPlus,"INPUT")
grovepi.pinMode(buttonMoins,"INPUT")

def LectBouton():
    if grovepi.digitalRead(buttonOk) == 1:
        return "Ok"
    if grovepi.digitalRead(buttonBack) == 1:
        return "Back"
    if grovepi.digitalRead(buttonPlus) == 1:
        return "Plus"
    if grovepi.digitalRead(buttonMoins) == 1:
        return "Moins"
pageMenu = 0
selectionPage = 1
while True:
    Bouton = LectBouton()
    if pageMenu == 0:
        LCD.setTextLigne1("    Selection")
        if selectionPage == 1:
            LCD.setTextLigne2("< affiche Temp >")
            if Bouton == "Ok":
                pageMenu = 1
        if selectionPage == 2:
            LCD.setTextLigne2("<  ajout data  >")
            if Bouton == "Ok":
                pageMenu = 2
        if selectionPage == 3:
            LCD.setTextLigne2("< afficher data >")
            if Bouton == "Ok":
                pageMenu = 3
        if selectionPage == 4:
            LCD.setTextLigne2("<  suppr data  >")
            if Bouton == "Ok":
                pageMenu = 4
        if selectionPage == 5:
            LCD.setTextLigne2("<   Eteindre   >")
            if Bouton == "Ok":
                pageMenu = 5
        if Bouton == "Plus":
            selectionPage = (selectionPage+1)%5
        if Bouton == "Moins":
            if selectionPage == 0:
                selectionPage = 5
            else :
                selectionPage = selectionPage - 1
    if pageMenu == 1 :
        LCD.setTextLigne1(str(round(thermo.ReadTemperature(),2))+' Celsius')
        LCD.setTextLigne2("retour -> menu")
        if LectBouton == "Back":
            pageMenu = 0





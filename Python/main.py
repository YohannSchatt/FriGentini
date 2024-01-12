#Main code of the project, running the fonctionnal part
# coding: utf-8

#bouton increment : D2 et D3
#bouton ok : D4
#bouton retour : D7 

import driverI2C as LCD
import time
import DriverThermometre as thermo
import grovepi 
import pandas as p
import led 
import threading

buttonOk = 4
buttonBack = 7
buttonPlus = 2
buttonMoins = 3
buzzer = 6
diode = 8

LCD.initialisation()
LCD.effacerText()
LCD.setRGB(127,0,127)

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
grovepi.pinMode(diode,"OUTPUT")
grovepi.pinMode(buzzer,"OUTPUT")

event_Bouton = threading.Event()
event_Menu = threading.Event()

def LectBouton():
    if grovepi.digitalRead(buttonOk) == 1:
        Bouton = "Ok"
        event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
    elif grovepi.digitalRead(buttonBack) == 1:
        Bouton = "Back"
        event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
    elif grovepi.digitalRead(buttonPlus) == 1:
        Bouton = "Plus"
        event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
    elif grovepi.digitalRead(buttonMoins) == 1:
        Bouton = "Moins"
        event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)

def Alarme(temperatureAct,temperature,approximation,Alarme):
    if Alarme and (temperatureAct < temperature - approximation or temperatureAct > temperature + approximation):
        led.turnON(buzzer)
        led.turnON(diode)
    else :
        led.turnOFF(buzzer)
        led.turnOFF(buzzer)

        
def deplacementcursor():
    if Bouton == "Moins" or Bouton == "Plus": # Permet de déplacer le curseur
            if poscursor == 0:
                poscursor = 1
            else :
                poscursor = 0
    return poscursor

def changementtemp():
    if Bouton == "Plus":
            temp[poscursor] +=0.1 #augmente la température
    if Bouton == "Moins":
            temp[poscursor] -=0.1 #augmente l'approximation
    return temp

def SelectionPage():
    event_Menu.wait() # Attend d'avoir reçu le déclenchement dans LectBouton
    températureAct = thermo.ReadTemperature()
    if pageMenu == 0 :
        PageMenu0(Bouton)
    if pageMenu == 1 : #Affiche la température
        pageMenu1(Bouton)
    if pageMenu == 5 : #Paramètre
        pageMenu5(Bouton)
        Bouton = None



def pageMenu0(Bouton):
    if pageMenu == 0: #Menu de selection
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
            LCD.setTextLigne2("< affiche data >")
            if Bouton == "Ok":
                pageMenu = 3
        if selectionPage == 4:
            LCD.setTextLigne2("<  suppr data  >")
            if Bouton == "Ok":
                pageMenu = 4
        if selectionPage == 5: #Paramètres
            LCD.setTextLigne2("<  Parametres  >")
            if Bouton == "Ok":
                pageMenu = 5
        if selectionPage == 6: #Stoppe le programme
            LCD.setTextLigne2("<   Eteindre   >")
            if Bouton == "Ok":
                pageMenu = 6
        if Bouton == "Plus":
            selectionPage = (selectionPage+1)%6
        if Bouton == "Moins":
            if selectionPage == 0:
                selectionPage = 6
            else :
                selectionPage = selectionPage - 1

def pageMenu1(Bouton):
    if pageMenu == 1 : #Affiche la température
        LCD.setTextLigne1(str(round(températureAct))+' Celsius       ')
        LCD.setTextLigne2("retour -> menu ")
        if Bouton == "Back": #permet de faire retour
            pageMenu = 0

def pageMenu5(Bouton):
    if pageParamètre == 0 : # Menu principale des paramètres
        LCD.setTextLigne1("temp : " + str(temp[0]) + " +- "+ str(temp[1]) + " " + cursor[poscursor] + "        ")
        LCD.setTextLigne2("Alarme : " + str(Alarme) +  cursor[(poscursor+1)%2] + "       ") #(poscursor+1%2) permet de selectionner l'autre element du tableau
        poscursor = deplacementcursor(poscursor)
        if Bouton == "Ok" and poscursor == 0: 
            pageParamètre = 1 
        if Bouton == "Ok" and poscursor == 1: 
            Alarme = not Alarme
    elif pageParamètre == 1 :  #Menu selection
        LCD.setTextLigne1("temp : " + str(temp[0]) + cursor[(poscursor+1)%2] +"         ")
        LCD.setTextLigne2("approx : " + str(temp[1]) + cursor[(poscursor+1)%2]  +"       ") 
        if Bouton == "Back": #permet de faire retour
            if blocked :
                cursor[0] = "<-"
                blocked = False
            else :
                pageParamètre = 0
                poscursor = 0
            if Bouton == "Ok":
                cursor[0] = "X"
                blocked = True
                temp = changementtemp(temp,cursor)
    elif Bouton == "Back": #permet de faire retour
        pageMenu = 0
        poscursor = 0


def main():

    global temp  #[température défini, approximation défini
    temo = [6,1]
    global pageMenu = 0 #Int qui permet de changer de Menu
    global selectionPage = 1 #Int qui permet de défiler entre les différents page du menu
    global pageParamètre = 0 #Int qui permet savoir ou on est dans les paramètres
    global poscursor = 0 #Int qui permet de connaitre ou se situe le curseur dans paramètre
    global cursor = ["<-",""] # curseur utilisé dans les différents menu qui se déplace sur les deux lignes
    global Alarme = True #variable pour savoir si l'alarme est active ou non
    global blocked = False #variable qui permet de bloquer le curseur
    global Bouton = None

    while True:
        tmenu = threading.Thread(target=SelectionPage()) #tmenu lancera SelectionPage()
        tbouton = threading.Thread(target=LectBouton()) #tbouton lancera LectBouton()

        tbouton.start()
        tmenu.start()       
        
        t1.join()
        t2.join()

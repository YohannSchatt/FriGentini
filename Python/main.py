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
import datetime as dt
import NFCDriver as nfc
import os

class Menu:
    def __init__(self):
        self.temp = [24,2]
        self.pageMenu = 0
        self.selectionPage = 0
        self.pageParamètre = 0
        self.poscursor = 0
        self.cursor = ["<-",""]
        self.Alarme = True
        self.blocked = False
        self.Bouton = None
        self.températureAct = thermo.ReadTemperature()
        self.pageAjout = 0 
        self.date = dt.date.today() #On set la date d'achat a aujourd'hui
        self.date_peremption = self.date #On initialise la date de péremption a aujourd'hui
        self.delta = dt.timedelta(days = 1) #On définit notre incrément a 1 jour
        self.NFC = ''
        self.index_menu4 = 0
        self.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
        self.df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
        self.page_menu_4 = 0

    def deplacementcursor(self):
        if self.Bouton == "Moins" or self.Bouton == "Plus": # Permet de déplacer le curseur
            if self.poscursor == 0:
                self.poscursor = 1
            else :
                self.poscursor = 0

    def changementtemp(self):
        if self.Bouton == "Plus":
            self.temp[self.poscursor] = round(self.temp[self.poscursor] + 0.1,1) #augmente la température
        elif self.Bouton == "Moins":
            self.temp[self.poscursor] = round(self.temp[self.poscursor] - 0.1,1) #augmente l'approximation

#[température défini, approximation défini
#temp = [6,1]
#Int qui permet de changer de Menu
#pageMenu = 0
#Int qui permet de défiler entre les différents page du menu
#selectionPage = 0
#Int qui permet savoir ou on est dans les paramètres
#pageParamètre = 0
#Int qui permet de connaitre ou se situe le curseur dans paramètre
#poscursor = 0
# curseur utilisé dans les différents menu qui se déplace sur les deux lignes
#cursor = ["<-",""]
#variable pour savoir si l'alarme est active ou non
#Alarme = True
#variable qui permet de bloquer le curseur
#blocked = False
#variable qui stocke la valeur du bouton
#Bouton = None

event_Bouton = threading.Event()
event_Menu = threading.Event()
verrou = threading.Lock()
menu = Menu()


def LectBouton():
    with verrou:
        buttonOk = 4
        buttonBack = 7
        buttonPlus = 2
        buttonMoins = 3
        buzzer = 6
        diode = 8


        grovepi.pinMode(buttonOk,"INPUT")
        grovepi.pinMode(buttonBack,"INPUT")
        grovepi.pinMode(buttonPlus,"INPUT")
        grovepi.pinMode(buttonMoins,"INPUT")
        grovepi.pinMode(diode,"OUTPUT")
        grovepi.pinMode(buzzer,"OUTPUT")

    while True:
        menu.températureAct = thermo.ReadTemperature()
        event_Bouton.wait()
        with verrou:
            if grovepi.digitalRead(buttonOk) == 1:
                menu.Bouton = "Ok"
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)                 
            elif grovepi.digitalRead(buttonBack) == 1:
                menu.Bouton = "Back"
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
            elif grovepi.digitalRead(buttonPlus) == 1:
                menu.Bouton = "Plus"
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
            elif grovepi.digitalRead(buttonMoins) == 1:
                menu.Bouton = "Moins"
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)                
            else:
                menu.Bouton = None
            Alarme()

def Alarme():
    buzzer = 6
    diode = 8
    if menu.Alarme and (menu.températureAct < menu.temp[0] - menu.temp[1] or menu.températureAct > menu.temp[0] + menu.temp[1]):
        led.TurnOn(buzzer)
        led.TurnOn(diode)
    else :
        led.TurnOff(buzzer)
        led.TurnOff(buzzer)


def SelectionPage():
    while True:
        with verrou:
            if menu.pageMenu == 0 :
                pageMenu0()
            if menu.pageMenu == 1 : #Affiche la température
                pageMenu1()
            if menu.pageMenu == 2:
                pageMenu2()
            if menu.pageMenu == 4:
                pageMenu4()
            if menu.pageMenu == 5 : #Paramètre
                pageMenu5()
            if menu.pageMenu == 6:
                pageMenu6
        event_Bouton.set()
        time.sleep(0.2)
        event_Menu.wait()



def pageMenu0():
    LCD.setTextLigne1("    Selection     ")
    if menu.selectionPage == 0:
        LCD.setTextLigne2("< affiche Temp >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 1
    if menu.selectionPage == 1:
        LCD.setTextLigne2("<  ajout data  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 2
    if menu.selectionPage == 2:
        LCD.setTextLigne2("< affiche data >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 3
    if menu.selectionPage == 3:
        LCD.setTextLigne2("<  suppr data  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 4
    if menu.selectionPage == 4: #Paramètres
        LCD.setTextLigne2("<  Parametres  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 5
    if menu.selectionPage == 5: #Stoppe le programme
        LCD.setTextLigne2("<   Eteindre   >")
        if menu.Bouton == "Ok":
           menu.pageMenu = 6
    if menu.Bouton == "Plus":
        menu.selectionPage = (menu.selectionPage+1)%6
    if menu.Bouton == "Moins":
        if menu.selectionPage == 0:
            menu.selectionPage = 6
        else :
            menu.selectionPage = menu.selectionPage - 1

def pageMenu1():
    LCD.setTextLigne1(str(round(menu.températureAct,1))+' Celsius       ')
    LCD.setTextLigne2("retour -> menu ")
    if menu.Bouton == "Back": #permet de faire retour
        menu.pageMenu = 0

def pageMenu2():
    #df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
    if menu.pageAjout == 0:
        LCD.setTextLigne1("Veuillez scanner")
        LCD.setTextLigne2("votre produit")
        cancel = False
        menu.NFC = 0
        while menu.NFC == 0 and not cancel : 
            menu.NFC = ''.join([hex(i)[-2:] for i in nfc.ReadCard()])
            #print(NFC)
        menu.pageAjout = 1
        menu.Bouton = None
    if menu.pageAjout == 1:
        print("Je rentre dans pageAjout 1 et le bouton vaut ", menu.Bouton)
        print("La date sélectionné est : " + str(menu.date_peremption))
        LCD.effacerText()
        LCD.setTextLigne1("Date peremption")
        LCD.setTextLigne2(str(menu.date_peremption)[0:10])

        if menu.Bouton == "Plus" :
            menu.date_peremption = menu.date_peremption + menu.delta
        elif menu.Bouton == "Moins" : 
            menu.date_peremption = menu.date_peremption - menu.delta
        elif menu.Bouton == "Ok" :
            menu.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
            menu.pageAjout = 0
            menu.pageMenu = 0
            menu.df_frigo.loc[len(menu.df_frigo.index)] = [len(menu.df_frigo)+1,menu.NFC,menu.date_peremption.strftime('%d/%m/%Y'),menu.date.strftime('%d/%m/%Y')] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
            menu.df_frigo.to_csv('../CSV/frigo.csv',index=False)
            LCD.effacerText()
            LCD.setTextLigne1("Produit ajouté")
            menu.date_peremption = menu.date
            time.sleep(1)
        else : 
            print("mauvaise commande")

def pageMenu4():
    if menu.page_menu_4 == 0:
        menu.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
        menu.df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits

        print("Veuillez parcourir la liste des produits du frigo et selectionne celui a supprimé")
        LCD.effacerText()
        LCD.setTextLigne1("Selectionné")
        LCD.setTextLigne2("celui a retire")
        menu.page_menu_4 = 1
        menu.Bouton = None
    if menu.page_menu_4 == 1 :
        liste_index = menu.df_frigo.index
        produit = menu.df_frigo.iloc[[liste_index[menu.index_menu4]]]
        nom_produit = menu.df_produits.query("Code_barre == '" + produit["Type_Produit"].values[0] + "'")['nom']
        LCD.effacerText()
        LCD.setTextLigne1("Nom : " + nom_produit.values[0])
        LCD.setTextLigne2("Prtp " + produit["date_péremption"].values[0])
        time.sleep(0.2)
        if menu.Bouton == "Plus" : 
            if menu.index_menu4 == len(liste_index) - 1:
                menu.index_menu4 = 0
            else : 
                menu.index_menu4 += 1 
        if menu.Bouton == "Moins" :
            if menu.index_menu4 == 0:
                menu.index_menu4 = len(liste_index) - 1
            else :
                menu.index_menu4 -= 1
        if menu.Bouton == "Ok":
            menu.df_frigo = menu.df_frigo.drop(liste_index[menu.index_menu4])
            menu.df_frigo.to_csv('../CSV/frigo.csv',index=False)
            menu.pageMenu = 0
            menu.page_menu_4 = 0
            menu.index_menu4 = 0
            print(menu.df_frigo)


def pageMenu5():
    if menu.pageParamètre == 0 : # Menu principale des paramètres
        LCD.setTextLigne1("temp : " + str(menu.temp[0]) + " +- "+ str(menu.temp[1]) + " " + menu.cursor[menu.poscursor] + "        ")
        LCD.setTextLigne2("Alarme : " + str(menu.Alarme) +  menu.cursor[(menu.poscursor+1)%2] + "       ") #(poscursor+1%2) permet de selectionner l'autre element du tableau
        menu.deplacementcursor()
        if menu.Bouton == "Ok" and menu.poscursor == 0: 
            menu.pageParamètre = 1 
        elif menu.Bouton == "Ok" and menu.poscursor == 1: 
            menu.Alarme = not menu.Alarme
        elif menu.Bouton == "Back": #permet de faire retour
            menu.pageMenu = 0
            menu.poscursor = 0
    elif menu.pageParamètre == 1 :  #Menu selection
        LCD.setTextLigne1("temp : " + str(menu.temp[0]) + " " +str(menu.cursor[menu.poscursor]) +"         ")
        LCD.setTextLigne2("approx : " + str(menu.temp[1]) + " " +str(menu.cursor[(menu.poscursor+1)%2])  +"       ") 
        if menu.Bouton == "Back": #permet de faire retour
            if menu.blocked :
                menu.cursor[0] = "<-"
                menu.blocked = False
            else :
                menu.pageParamètre = 0
                menu.poscursor = 0
        elif menu.Bouton == "Ok":
            menu.cursor[0] = "X"
            menu.blocked = True
        elif menu.blocked:
            menu.changementtemp()
        else:
            menu.deplacementcursor()

def pageMenu6():
    quit()

def main():

    LCD.initialisation()
    LCD.effacerText()
    LCD.setRGB(127,0,127)

    LCD.setTextLigne2("    Bienvenue"    )
    time.sleep(2)

    tmenu = threading.Thread(target=SelectionPage) #tmenu lancera SelectionPage()
    tbouton = threading.Thread(target=LectBouton) #tbouton lancera LectBouton() 

    tbouton.start()
    tmenu.start()       
        
    tbouton.join()
    tmenu.join()

main()

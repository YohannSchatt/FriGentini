#Main code of the project, running the fonctionnal part
# coding: utf-8

#bouton increment : D2 et D3
#bouton ok : D4
#bouton retour : D7 

import driverI2C as LCD
import time
import DriverThermometre as thermo
import NFCDriver as nfc
import grovepi 
import pandas as p
import led 
import threading
import datetime as dt

#Instance du menu 
class Menu:
    #Initialiation du menu avec les variables de départ
    def __init__(self):
        self.temp = [6,1]
        self.pageMenu = 0
        self.selectionPage = 0
        self.pageParamètre = 0
        self.poscursor = 0
        self.cursor = ["<-",""]
        self.Alarme = True
        self.blocked = False
        self.Bouton = None
        self.températureAct = thermo.ReadTemperature()

    #Méthode 
    def deplacementcursor(self):
        if self.Bouton == "Moins" or self.Bouton == "Plus": # Permet de déplacer le curseur
            if self.poscursor == 0:
                self.poscursor = 1
            else :
                self.poscursor = 0
    #Méthode
    def changementtemp(self):
        if self.Bouton == "Plus":
            self.temp[poscursor] +=0.1 #augmente la température
        elif self.Bouton == "Moins":
            self.temp[poscursor] -=0.1 #augmente l'approximation

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

"""
Fonction qui gère la lecture des boutons de la carte, il y a 4 boutons sur la carte, 2 tactiles et 2 classiques. On utilise les tactiles pour faire
les défilements, ils sont plus sensibles et les boutons normaux pour faire des validations.
Elle est associé à un thread et met a jour les valeurs de Bouton dans l'instance de menu
"""

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
        #print("je suis dans bouton")
        event_Bouton.wait()
        with verrou:
            if grovepi.digitalRead(buttonOk) == 1:
                menu.Bouton = "Ok"
                print("Ok")
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)        
                event_Bouton.wait()            
            elif grovepi.digitalRead(buttonBack) == 1:
                menu.Bouton = "Back"
                print("back")
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
                event_Bouton.wait()
            elif grovepi.digitalRead(buttonPlus) == 1:
                menu.Bouton = "Plus"
                print("plus")
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)
                event_Bouton.wait()
            elif grovepi.digitalRead(buttonMoins) == 1:
                menu.Bouton = "Moins"
                print("moins")
                event_Menu.set() #Déclenche le Menu (le wait dans selectionPage() est fini)                
                event_Bouton.wait()
            else:
                menu.Bouton = None


"""
Fonction qui s'occuppe de gérer l'alarme, vérifie si la température < seuil, si non active le buzzer, et si trop long supprime les objets impropre 
a la consommation
"""
def Alarme():
    buzzer = 6
    diode = 8
    if menu.Alarme and (menu.temperatureAct < menu.temp[0] - menu.temp[1] or menu.temperatureAct > menu.temp[0] + menu.temp[1]):
        led.turnON(buzzer)
        led.turnON(diode)
    else :
        led.turnOFF(buzzer)
        led.turnOFF(buzzer)


"""
Fonction qui s'occuper de basculer sur les différentes pages du menu principales en lisant la valeur de bouton, appel la fonction associé a la page 
demandée
"""
def SelectionPage():
    while True:
        with verrou:
            print("SelectionPage")
            menu.températureAct = thermo.ReadTemperature()
            if menu.pageMenu == 0 :
                pageMenu0()
                menu.Bouton = None
            if menu.pageMenu == 1 : #Affiche la température
                pageMenu1()
            if menu.pageMenu == 2 :
                pageMenu2()
                menu.Bouton = None
            if menu.pageMenu == 5 : #Paramètre
                pageMenu5()
                menu.Bouton = None
        event_Bouton.set()
        time.sleep(0.05)
        event_Menu.wait()


"""
Fonction qui gère le menu principal, on navigue avec les boutons tactiles et on valide avec les boutons poussoirs
"""
def pageMenu0():
    print("PageMenu0")
    print("selectionPage :", menu.selectionPage)
    print("Bouton :", menu.Bouton)
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
        print("coucou")
        menu.selectionPage = (menu.selectionPage+1)%6
    if menu.Bouton == "Moins":
        print("coucou2")
        if menu.selectionPage == 0:
            menu.selectionPage = 6
        else :
            menu.selectionPage = menu.selectionPage - 1

"""
Page qui affiche la température en direct
"""
def pageMenu1():
    if menu.pageMenu == 1 : #Affiche la température
        LCD.setTextLigne1(str(round(menu.températureAct))+' Celsius       ')
        LCD.setTextLigne2("retour -> menu ")
        if Bouton == "Back": #permet de faire retour
            menu.pageMenu = 0
    
"""Page permettant d'ajouter en produits en scannant son code NFC"""
def pageMenu2():
    LCD.setTextLigne1("Veuillez scanner")
    LCD.setTextLigne2("votre produit")
    cancel = False
    NFC = 0
    while NFC == 0 and not cancel : 
        NFC = ''.join([hex(i)[-2:] for i in nfc.ReadCard()])
         #print(NFC)
    
    df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
    df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
    produit = df_produits.query("Code_barre == '" + NFC + "'")
    print(produit["nom"][0])

    date = dt.date.today() #On set la date d'achat a aujourd'hui
    date_peremption = date #On initialise la date de péremption a aujourd'hui
    delta = dt.timedelta(days = 1) #On définit notre incrément a 1 jour
    sortie = False
    while not sortie : 
        print("La date sélectionné est : " + str(date_peremption))
        LCD.setTextLigne1("Date peremption")
        LCD.setTextLigne2(str(date_peremption))
        if menu.Bouton == "Plus" :
            date_peremption = date_peremption + delta
        elif menu.Bouton == "Moins" : 
            date_peremption = date_peremption - delta
        elif menu.Bouton == "Ok" :
            sortie = True
        else : 
            print("mauvaise commande")

    df_frigo.loc[len(df_frigo.index)] = [len(df_frigo)+1,'5dc2f869',date_peremption.strftime('%d/%m/%Y'),date.strftime('%d/%m/%Y')] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
    print(df_frigo)
    menu.pageMenu = 0
    LCD.effacerText()
    LCD.setTextLigne1("Produit ajouté")
    time.sleep(1)


def pageMenu5():
    global pageParamètre #Int qui permet savoir ou on est dans les paramètres
    global Alarme  #variable pour savoir si l'alarme est active ou non
    global Bouton  #variable qui permet de conserver la valeur de bouton
    global blocked  #variable qui permet de bloquer le curseur
    global cursor  # curseur utilisé dans les différents menu qui se déplace sur les deux lignes
    global poscursor  #Int qui permet de connaitre ou se situe le curseur dans paramètre
    if menu.pageParamètre == 0 : # Menu principale des paramètres
        LCD.setTextLigne1("temp : " + str(menu.temp[0]) + " +- "+ str(menu.temp[1]) + " " + menu.cursor[menu.poscursor] + "        ")
        LCD.setTextLigne2("Alarme : " + str(menu.Alarme) +  menu.cursor[(menu.poscursor+1)%2] + "       ") #(poscursor+1%2) permet de selectionner l'autre element du tableau
        menu.deplacementcursor()
        if menu.Bouton == "Ok" and menu.poscursor == 0: 
            menu.pageParamètre = 1 
        if menu.Bouton == "Ok" and menu.poscursor == 1: 
            menu.Alarme = not menu.Alarme
    elif menu.pageParamètre == 1 :  #Menu selection
        LCD.setTextLigne1("temp : " + str(menu.temp[0]) + cursor[(poscursor+1)%2] +"         ")
        LCD.setTextLigne2("approx : " + str(menu.temp[1]) + cursor[(poscursor+1)%2]  +"       ") 
        if menu.Bouton == "Back": #permet de faire retour
            if menu.blocked :
                menu.cursor[0] = "<-"
                menu.blocked = False
            else :
                menu.pageParamètre = 0
                menu.poscursor = 0
        elif Bouton == "Ok":
            menu.cursor[0] = "X"
            menu.blocked = True
        elif blocked:
            menu.temp = menu.changementtemp(menu.temp,cursor)
        


    elif Bouton == "Back": #permet de faire retour
        pageMenu = 0
        poscursor = 0


def main():

    LCD.initialisation()
    LCD.effacerText()
    LCD.setRGB(127,0,127)

    LCD.setTextLigne2("    Bienvenue"    )
    time.sleep(2)

    tmenu = threading.Thread(target=SelectionPage) #tmenu lancera SelectionPage()
    print("coucou")
    tbouton = threading.Thread(target=LectBouton) #tbouton lancera LectBouton() 

    tbouton.start()
    tmenu.start()       
        
    tbouton.join()
    tmenu.join()

main()

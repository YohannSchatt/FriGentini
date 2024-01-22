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
import Releve_temperature as rt

class Menu:
    def __init__(self):
        self.temp = [24,2] #température initial pour les paramètres
        self.pageMenu = 0 #menu
        self.selectionPage = 0 #selectionne page de pageMenu0
        self.pageParamètre = 0 #pageParamètre selection
        self.poscursor = 0 #position du curseur
        self.cursor = ["<-",""] #curseur sur 2 ligne
        self.Alarme = True #Active l'alarme
        self.blocked = False #variable qui blocked l'avancé du programme dans des cas spécifique
        self.Bouton = None #variable de bouton lu
        self.températureAct = thermo.ReadTemperature() #lit une température initial
        self.pageAjout = 0 
        self.date = dt.date.today() #On set la date d'achat a aujourd'hui
        self.date_peremption = self.date #On initialise la date de péremption a aujourd'hui
        self.delta = dt.timedelta(days = 1) #On définit notre incrément a 1 jour
        self.NFC = ''
        self.index_menu4 = 0
        self.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
        self.df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
        self.page_menu_4 = 0
        self.tmenu = -1 #défini une valeur au thread
        self.tbouton = -1 #défini une valeur au thread
        self.eteindre = False #variable qui éteindra le programme
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
# curseur utilisé dans les différents menu qui se déplace sur les deux lignes    #df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
#blocked = False
#variable qui stocke la valeur du bouton
#Bouton = None

event_Bouton = threading.Event() #crée le semaphore event_bouton
event_Menu = threading.Event() #crée le semaphire event_menu
verrou = threading.Lock() #crée un mutex
menu = Menu() #crée l'objet menu


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
        event_Bouton.wait() #attend le menu
        menu.températureAct = thermo.ReadTemperature() #temperature
        rt.releve_temp(menu.températureAct)
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
            if menu.eteindre:
                quit()

def Alarme():
    buzzer = 6
    diode = 8
    if menu.Alarme and (menu.températureAct < menu.temp[0] - menu.temp[1] or menu.températureAct > menu.temp[0] + menu.temp[1]): #si la température est comprise entre la température voulu et approximé
        led.TurnOn(buzzer)
        led.TurnOn(diode) #on allume diode et buzzer
    else :
        led.TurnOff(buzzer) #sinon on l'éteint
        led.TurnOff(diode)


def SelectionPage():
    while True:
        with verrou:
            if menu.pageMenu == 0 :
                pageMenu0()
            if menu.pageMenu == 1 : #Affiche la température
                pageMenu1()
            if menu.pageMenu == 2: #ajout data
                pageMenu2()
            if menu.pageMenu == 3: #affiche data
                pageMenu3()
            if menu.pageMenu == 4: #supprime data
                pageMenu4()
            if menu.pageMenu == 5 : #Paramètre
                pageMenu5()
            if menu.pageMenu == 6: #Eteindre
                pageMenu6()
        event_Bouton.set()
        time.sleep(0.2)
        event_Menu.wait()



def pageMenu0(): #Menu principale, affiche la page ou se trouve l'utilisateur
    if menu.selectionPage == 0: #affice temp
        LCD.setTextLigne2("< affiche Temp >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 1
    if menu.selectionPage == 1: #ajout data
        LCD.setTextLigne2("<  ajout data  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 2
    if menu.selectionPage == 2: #affiche data
        LCD.setTextLigne2("< affiche data >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 3
    if menu.selectionPage == 3: #suppr data
        LCD.setTextLigne2("<  suppr data  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 4
    if menu.selectionPage == 4: #Paramètres
        LCD.setTextLigne2("<  Parametres  >")
        if menu.Bouton == "Ok":
            menu.pageMenu = 5
            blocked = True
    if menu.selectionPage == 5: #Stoppe le programme
        LCD.setTextLigne2("<   Eteindre   >")
        if menu.Bouton == "Ok":
           menu.pageMenu = 6
        LCD.setTextLigne1("    Selection     ")
    if menu.Bouton == "Plus": #permet d'incrémenter la selection de Page
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
    if menu.pageAjout == 0:
        LCD.setTextLigne1("Veuillez scanner")
        LCD.setTextLigne2("votre produit")
        cancel = False
        menu.NFC = 0
        while menu.NFC == 0 and not cancel : 
            menu.NFC = ''.join([hex(i)[-2:] for i in nfc.ReadCard()])
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

def pageMenu3() :
    menu.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
    menu.df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits

    print("Parcours des data")
    LCD.effacerText()
    LCD.setTextLigne1("Affichage")
    LCD.setTextLigne2("du stock")
    time.sleep(1)

    liste_index = menu.df_frigo.index

    for i in range(len(liste_index)):
        produit = menu.df_frigo.iloc[[liste_index[i]]]
        nom_produit = menu.df_produits.query("Code_barre == '" + produit["Type_Produit"].values[0] + "'")['nom']
        LCD.effacerText()
        LCD.setTextLigne1("Nom : " + nom_produit.values[0])
        LCD.setTextLigne2("Prtp " + produit["date_péremption"].values[0])
        time.sleep(1)
    menu.pageMenu = 0



#Menu de suppression d'un produit
def pageMenu4():
    if menu.page_menu_4 == 0:
        menu.df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock
        menu.df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits

        print("Veuillez parcourir la liste des produits du frigo et selectionne celui a supprimé")
        LCD.effacerText()
        LCD.setTextLigne1("Selectionné")
        LCD.setTextLigne2("celui a retire")
        time.sleep(1)
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
            LCD.effacerText()
            LCD.setTextLigne1("Produit retiré")
            time.sleep(1)


def pageMenu5():
    if menu.pageParamètre == 0 : # Menu principale des paramètres
        LCD.setTextLigne1("temp : " + str(menu.temp[0]) + " +- "+ str(menu.temp[1]) + " " + menu.cursor[menu.poscursor] + "        ")
        LCD.setTextLigne2("Alarme : " + str(menu.Alarme) +  menu.cursor[(menu.poscursor+1)%2] + "       ") #(poscursor+1%2) permet de selectionner l'autre element du tableau
        menu.deplacementcursor() #permet de déplacer le curseur
        if menu.Bouton == "Ok" and menu.poscursor == 0 and not menu.blocked: 
            menu.pageParamètre = 1 
        elif menu.Bouton == "Ok" and menu.poscursor == 1 and not menu.blocked: 
            menu.Alarme = not menu.Alarme
        elif menu.Bouton == "Back": #permet de faire retour
            menu.pageMenu = 0
            menu.poscursor = 0
        blocked = False
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

#affiche la page eteindre
def pageMenu6():
    LCD.setTextLigne1("      Fin      ") #affiche fin
    time.sleep(0.2)
    tabtext = [" "," "," "," "," "," "," "," "," "," "] #stock les différents caractère de la barre de chargement
    text = "          "
    LCD.setTextLigne2("  [" + text + "]    ")
    for i in range(10):
        text = ""
        tabtext[i] = "#"
        for j in range(10):
            text = text + tabtext[j] #actualise le texte
        LCD.setTextLigne2("  [" + text + "]     ") #affiche le texte
        time.sleep(0.2)
    menu.eteindre = True #lance l'extinction LectBouton
    event_Bouton.set()
    led.TurnOff(6) #coupe le buzzer
    led.TurnOff(8) #coupe la led
    LCD.effacerText() #efface text
    LCD.setRGB(0,0,0) #stop l'écran
    quit()






def main():
    LCD.initialisation() #initialise l'écran
    LCD.effacerText() #efface l'ancien text
    LCD.setRGB(127,0,127) #met l'écran en violet

    LCD.setTextLigne2("    Bienvenue"    ) #écrit bienvenue sur la ligne 2
    time.sleep(2) 

    menu.tmenu = threading.Thread(target=SelectionPage) #tmenu lancera SelectionPage()
    menu.tbouton = threading.Thread(target=LectBouton) #tbouton lancera LectBouton() 

    menu.tbouton.start() #lance le thread tbouton
    menu.tmenu.start()  #lance le thread tmenu

    menu.tbouton.join() #rejoint les deux threads
    menu.tmenu.join()   #rejoint les deux threads
main()

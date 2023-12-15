# coding: utf-8
import smbus
import time

bus = smbus.SMBus(1)  # pour I2C-1 (0 pour I2C-0)

# Indiquez ici les deux adresses de l'ecran LCD
# celle pour les couleurs du fond d'ecran
# et celle pour afficher des caracteres
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR =0x3e

# Completez le code de la fonction permettant de choisir la couleur
# du fond d'ecran, n'oubliez pas d'initialiser l'ecran
def setRGB(rouge,vert,bleu):
	# rouge, vert et bleu sont les composantes de la couleur qu'on vous demande
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,bleu)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,vert)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,rouge)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
	print("Couleur écran changée")

# Envoie  a l'ecran une commande concerant l'affichage des caracteres
# (cette fonction vous est donnes gratuitement si vous
# l'utilisez dans la fonction suivante, sinon donnez 2000€
# a la banque et allez dictement en prison :)
def textCmd(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# Completez le code de la fonction permettant d'ecrire le texte recu en parametre
# Si le texte contient un \n ou plus de 16 caracteres pensez a gerer
# le retour a la ligne
def setText(texte):
        textCmd(0x01)
        time.sleep(0.00001)
        textCmd(0x0F)
        time.sleep(0.00001)
        textCmd(0x38) #2eme ligne 
        time.sleep(0.00001)
        antislash = False
        compteur = 0
        for i in texte :
                #print(i)
                if i == "\\" :
                        antislash = True
                elif (i == "n" and antislash) or compteur == 16:  # si on rencontre \n ou si on depasse 16 caracteres
                        textCmd(0xc0) # pour passer a la ligne
                        compteur = 0
                        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(i))
                else :
                        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(i))
                        antislash = False
                        compteur += 1
        print ("texte ecrit")

def Textinitialisation():
        textCmd(0x01)
        time.sleep(0.001)
        textCmd(0x0F)
        time.sleep(0.001)
        textCmd(0x38)
        time.sleep(0.001)
#fonction qui permet d'écrire sur la ligne 1 de l'écran
#a pour entré un texte qui inférieur ou égal a 16
def setTextLigne1(texte):
        textCmd(0x02)
        textCmd(0x08 | 0x04)
        i = 0
        while i<= 15 and i<len(texte) and texte[i] != "\n":
                bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[i]))
                i += 1

#fonction qui permet d'écrire sur la ligne 2 de l'écran
#a pour entré un texte qui inférieur ou égal a 16
def setTextLigne2(texte):
        textCmd(0xc0) # pour passer a la ligne
        i = 0
        while i <= 15 and i < len(texte) and texte[i] != "\n":
                bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[i]))
                i += 1

        

def setText(texte):
        row = 1
        tab = texte.split("\n")
        print(tab)
        for i in range(len(tab)-1):
                effacerText(0x01)
                setTextLigne1(tab[i])
                setTextLigne2(tab[i+1])
                print("Coucou")
                time.sleep(2)

                




def effacerText():
        textCmd(0x01)


                         
        

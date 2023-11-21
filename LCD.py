#!/usr/bin/python3
#-*- coding: utf-8 -*-

import grovepi
import smbus
import time

bus = smbus.SMBus(1)  # pour I2C-1 (0 pour I2C-0)

# Indiquez ici les deux adresses de l'ecran LCD
# celle pour les couleurs du fond d'ecran 
# et celle pour afficher des caracteres
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# Completez le code de la fonction permettant de choisir la couleur
# du fond d'ecran, n'oubliez pas d'initialiser l'ecran
def setRGB(rouge,vert,bleu):
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
        time.sleep(0.01)

# Completez le code de la fonction permettant d'ecrire le texte recu en parametre
# Si le texte contient un \n ou plus de 16 caracteres pensez a gerer
# le retour a la ligne
def Text(texte):
        textCmd(0x01)
        textCmd(0x0F)
        textCmd(0x38)
        compteur = 0
        ligne1 = ""
        ligne2 = ""
        for i in range(0,len(c)):
            compteur = 0
            if ligne1 == "":
                bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[i]))
                ligne1 += texte[i]
                compteur += 1
                if compteur == 16 or texte[i] == '\n':
                        textCmd(0xc0)
                        timesleep(0.1)
            elif ligne1 != "" and ligne2 != "":
                ligne1 = ""
                for c in ligne2:
                    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[i]))
                    ligne1 += c
                    compteur += 1
                    if compteur == 16 or texte[i] == '\n':
                        textCmd(0xc0)
                        ligne2 = ""
                        timesleep(2)
            elif ligne2 == "":
                bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[i]))
                ligne2 += texte[i]
                compteur += 1
                if compteur == 16 or texte[i] == '\n':
                        textCmd(0xc0)
                        timesleep(2)
        print ("texte ecrit")

def SetText1(texte):
    textCmd(0x01)
    textCmd(0x0F)
    textCmd(0x38)
    compteur = 0
    for c in texte:
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
        compteur += 1
            if compteur == 16 or c == '\n':
                    textCmd(0xc0)
                    compteur = 0 

def setColor(nomCouleur):
    if nomCouleur == "rouge":
        setRGB(255,0,0)
    if nomCouleur == "bleu":
        setRGB(0,0,255)
    if nomCouleur == "vert":
        setRGB(0,255,0)
    if nomCouleur == "blanc":
        setRGB(0,0,0)
    if nomCouleur == "jaune":
        setRGB(127,127,0)
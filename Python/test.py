import pandas as p
import datetime as dt

#Partie du code permettant l'ajout d'une ligne dans le tableau des produits
#######################################################################################################################################################


df_produits = p.read_csv('../CSV/liste_produits.csv') #On récupère le csv des produits
df_frigo = p.read_csv('../CSV/frigo.csv') #On récupère les CSV des produits dans le stock

code_produit = df_produits.query("Code_barre == " + "'ca5f4ddb'")['Code_barre'] #Récupération de l'identifiant du produits scannées pour rentrer dans le stock
date = dt.date.today()
date_peremption = date
delta = dt.timedelta(days = 1)
sortie = False

while not sortie : 
    print("La date sélectionné est : " + str(date_peremption))
    clavier = input("Ecriver 1 pour 1 jour de +, 2 pour un jour en arriere et 0 pour valider \n")
    if int(clavier) == 1 :
        date_peremption = date_peremption + delta
    elif int(clavier) == 2 : 
        date_peremption = date_peremption - delta
    elif int(clavier) == 0 :
        sortie = True
    else : 
        print("mauvaise commande")

df_frigo.loc[len(df_frigo.index)] = [len(df_frigo)+1,'5dc2f869',date_peremption.strftime('%d/%m/%Y'),date.strftime('%d/%m/%Y')] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
print(df_frigo)


#######################################################################################################################################################
#https://www.delftstack.com/fr/howto/python-pandas/drop-row-pandas/

print("Veuillez parcourir la liste des produits du frigo et selectionne celui a supprimé")
valide = False
liste_index = df_frigo.index
i = 0
while not valide : 
    produit = df_frigo.iloc[[liste_index[i]]]
    nom_produit = df_produits.query("Code_barre == '" + produit["Type_Produit"][0] +"'")['nom']
    print("Vous avez choisi le produit " + nom_produit.values[0])
    clavier = input("Appuyer sur 1 pour le suivant, 0 pour valider \n")
    if int(clavier) == 1 : 
        if i == len(liste_index) - 1:
            i = 0
        else : 
            i += 1
    valide = int(clavier) == 0 

df_frigo = df_frigo.drop(liste_index[i])
print(df_frigo)

######################################################################################################################################################
#Partie affichage des data, probablement un parcours avec des sleep et hop 
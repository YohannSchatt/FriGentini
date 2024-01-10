import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = "root",
    database = "frigentini"
)

#my_cursor = db.cursor()

#my_cursor.execute("CREATE DATABASE test") #Commande qui permet de créer une base de donnée

#my_cursor.execute("DROP DATABASE testdatabase") #Commande qui permet de supprimer une base de donnée

#my_cursor.execute("CREATE TABLE Produits (produitID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50))")#Commande qui permet de creer une table dans la BD courante

#my_cursor.execute("DROP TABLE Produits") #

#my_cursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)",("Joe",22)) #Bonne pratique 

#db.commit() #Valider les changements dans la BD

#my_cursor.execute("SELECT * FROM Person")

#for x in my_cursor : #Cursor est un élément itératif  
    #print(x)


#########################################################################################################################################################################


def crea_tables ():
    my_cursor = db.cursor()
    try : 
        my_cursor.execute("DROP TABLE STOCK,TEMPERATURES,PRODUITS")
    except mysql.connector.Error as err: 
        print(f"Erreur d'exécution de la commande SQL : {err}")
    # Lire les instructions SQL à partir du fichier
    with open('../SQL/creation_BD.sql', 'r') as file:
        sql_commands = file.read().split('\n')

    # Exécuter chaque instruction SQL du fichier, ici création de la BD
    for command in sql_commands:
        try:
            my_cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"Erreur d'exécution de la commande SQL : {err}")

    # Lire les instructions SQL à partir du fichier, Injection des données de base
    with open('../SQL/Donnees.sql', 'r') as file:
        sql_commands = file.read().split('\n')

    # Exécuter chaque instruction SQL du fichier
    for command in sql_commands:
        print(command)
        try:
            my_cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"Erreur d'exécution de la commande SQL : {err}")

    db.commit() #Valider les changements dans la BD
    my_cursor.close()

def requete_BD(requete) :
    my_cursor = db.cursor()
    try:
        my_cursor.execute(requete)
        return my_cursor
    except mysql.connector.Error as err:
            print(f"Erreur d'exécution de la commande SQL : {err}")
    db.commit() #Valider les changements dans la BD
    my_cursor.close()

def deconnexion_BD():
    db.close()

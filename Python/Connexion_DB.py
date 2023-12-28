import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = "root",
    database = "frigentini"
)

my_cursor = db.cursor()

#my_cursor.execute("CREATE DATABASE test") #Commande qui permet de créer une base de donnée

#my_cursor.execute("DROP DATABASE testdatabase") #Commande qui permet de supprimer une base de donnée

my_cursor.execute("CREATE TABLE Produits (produitID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50))")#Commande qui permet de creer une table dans la BD courante

#my_cursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)",("Joe",22))

#db.commit()
#my_cursor.execute("SELECT * FROM Person")

#for x in my_cursor : 
    #print(x)

my_cursor.close()
db.close()

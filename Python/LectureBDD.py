import pandas as pd

def createdataframe(nom):
    dataFrame = pd.read_csv(nom)
    return dataFrame

Stock = createdataframe("../CSV/Stock.csv")
Produits = createdataframe("../CSV/produits.csv")

def ajoutelement(dataframe,tab):
    

print(Stock)
print("")
print(Produits)
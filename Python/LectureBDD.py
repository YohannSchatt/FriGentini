import pandas as pd

def createdataframe(nom):
    dataFrame = pd.read_csv(nom)
    return dataFrame

Stock = createdataframe("../CSV/Stock.csv")
Produits = createdataframe("../CSV/produits.csv")

def ajoutelement(data,elementajout):
    if len(elementajout) == len(data.columns):
        df2 = pd.DataFrame([elementajout], columns=data.columns)
        data = data._append(df2, ignore_index=True)
    return data

def datatocsv(data):
    csvdata =  data.to_csv()
    return csvdata

print(len(Stock.columns))
Stock = ajoutelement(Stock,[1,"pate","02/01/24","22/12/23"])

print(datatocsv(Stock))

def ecrireDansFichier(self,path,texte):
        fichier = open(path,"w")
        fichier.writelines(texte)
        fichier.close()

with open( )
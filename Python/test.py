import pandas as p
df_produits = p.read_csv('../CSV/liste_produits.csv')
df_frigo = p.read_csv('../CSV/frigo.csv')
type_produit = df_produits.query("Code_barre == " + "'ca5f4ddb'")['Code_barre']
ligne = {'Id' : 3,'Code_barre' : '5dc2f869','date_péremption' : '30/01/2024','date_achat' : '12/01/2024'}
df_frigo.loc[len(df_frigo.index)] = [len(df_frigo)+1,'5dc2f869','30/01/2024','12/01/2024']
print(df_frigo)
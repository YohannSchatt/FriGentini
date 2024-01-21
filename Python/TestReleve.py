import datetime
import pandas as pd

df_temperature = pd.read_csv('../CSV/temperature.csv').sort_values(by = ["date","heure"])
dernier_releve_temperature = df_temperature.iloc[[-1]][["date","heure"]]

date_jour = datetime.datetime.today()
dernier_relevé = datetime.datetime.strptime(dernier_releve_temperature["date"].values[0],'%d/%m/%Y')
print(dernier_relevé)
print(date_jour)
diff =  date_jour - dernier_relevé
print(diff.days)
print(24*3600)


if diff.days >= 1 :
    print([len(df_temperature)+1,date_jour.strftime('%d/%m/%Y'),date_jour.hour,5])
    df_temperature.loc[len(df_temperature.index)] = [len(df_temperature)+1,date_jour.strftime('%d/%m/%Y'),date_jour.hour,5] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
    df_temperature.to_csv('../CSV/temperature.csv',index=False)
elif diff.seconds/3600 >= 1:
    print("chibrax")



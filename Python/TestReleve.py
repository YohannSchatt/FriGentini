import datetime
import pandas as pd

df_temperature = pd.read_csv('../CSV/temperature.csv')
df_temp_normalise = df_temperature
df_temp_normalise["date"] = pd.to_datetime(df_temp_normalise["date"],dayfirst= True)
df_temp_normalise = df_temp_normalise.sort_values(by = ["date","heure"])

dernier_releve_temperature = df_temp_normalise.iloc[[-1]][["date","heure"]]
print(dernier_releve_temperature)

date_jour = datetime.datetime.today()
dernier_releve = datetime.datetime.strptime(str(dernier_releve_temperature["date"].values[0])[0:10],'%Y-%m-%d')
print(dernier_releve)
diff =  date_jour - dernier_releve


if diff.days >= 1 :
    print([len(df_temperature)+1,date_jour.strftime('%d/%m/%Y'),date_jour.hour,5])
    df_temperature.loc[len(df_temperature.index)] = [len(df_temperature),date_jour.strftime('%d/%m/%Y'),date_jour.hour,5] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
    df_temperature.to_csv('../CSV/temperature.csv',index=False)
elif diff.seconds/3600 >= 1:
    print("chibrax")



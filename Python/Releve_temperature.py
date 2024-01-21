import datetime
import pandas as pd



def releve_temp(temperature):
    df_temperature = pd.read_csv('../CSV/temperature.csv')
    df_temp_normalise = df_temperature.copy()
    df_temp_normalise["date"] = pd.to_datetime(df_temp_normalise["date"],dayfirst= True)
    df_temp_normalise = df_temp_normalise.sort_values(by = ["date","heure"])
    dernier_releve_temperature = df_temp_normalise.iloc[[-1]][["date","heure"]]

    date_jour = datetime.datetime.today()
    dernier_releve = datetime.datetime.strptime(str(dernier_releve_temperature["date"].values[0])[0:10],'%Y-%m-%d')
    heure_du_releve = datetime.timedelta(hours = int(dernier_releve_temperature["heure"].values[0]))
    dernier_releve = dernier_releve + heure_du_releve
    diff =  date_jour - dernier_releve 

    if diff.days >= 1 :
        df_temperature.loc[len(df_temperature.index)] = [len(df_temperature),date_jour.strftime('%d/%m/%Y'),date_jour.hour,temperature] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
        df_temperature.to_csv('../CSV/temperature.csv',index=False)
        print("Relevé effectué")
    elif diff.seconds/3600 >= 1:
        df_temperature.loc[len(df_temperature.index)] = [len(df_temperature),date_jour.strftime('%d/%m/%Y'),date_jour.hour,temperature] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
        df_temperature.to_csv('../CSV/temperature.csv',index=False)
        print("Relevé effectué")


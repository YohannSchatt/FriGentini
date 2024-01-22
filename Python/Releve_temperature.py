import datetime
import pandas as pd



def releve_temp(temperature):
    df_temperature = pd.read_csv('../CSV/temperature.csv')#Récupération du CSV du relevés des températures
    df_temp_normalise = df_temperature.copy() #Copy du dtaframe pour eviter la référence
    df_temp_normalise["date"] = pd.to_datetime(df_temp_normalise["date"],dayfirst= True) #Reconvertit les dates au bon format
    df_temp_normalise = df_temp_normalise.sort_values(by = ["date","heure"]) #Trie dans l'ordre croissant des dates, de la plus anciennes a la plus proche
    dernier_releve_temperature = df_temp_normalise.iloc[[-1]][["date","heure"]]#Récupération du dernier relevé en date

    date_jour = datetime.datetime.today()#Récupération date du jour
    dernier_releve = datetime.datetime.strptime(str(dernier_releve_temperature["date"].values[0])[0:10],'%Y-%m-%d')#Récupération de la date au format datetime
    heure_du_releve = datetime.timedelta(hours = int(dernier_releve_temperature["heure"].values[0]))#Récupération de l'heure du dernier relevé
    dernier_releve = dernier_releve + heure_du_releve #Ajout de l'heure a la date
    diff =  date_jour - dernier_releve #Calcul du delta de temps


    #Si il y a plus d'un jour
    if diff.days >= 1 :
        #Edition du CSV avec le nouveau relevé
        df_temperature.loc[len(df_temperature.index)] = [len(df_temperature),date_jour.strftime('%d/%m/%Y'),date_jour.hour,temperature] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
        df_temperature.to_csv('../CSV/temperature.csv',index=False)
    #Sinon vérification si il y a plus d'une heure
    elif diff.seconds/3600 >= 1:
        #Edition du CSV avec le nouveau relevé
        df_temperature.loc[len(df_temperature.index)] = [len(df_temperature),date_jour.strftime('%d/%m/%Y'),date_jour.hour,temperature] #Ajout d'une ligne dans le csv de la liste des produits dans le stock
        df_temperature.to_csv('../CSV/temperature.csv',index=False)


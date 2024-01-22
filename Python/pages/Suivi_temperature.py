import pandas as pd
import Menu as mn
import streamlit as st
from PIL import Image
import datetime

#Fonction qui vérifie si la date en entrée au format date, est la date du jour
#Entrée : date au format jour/mois/année
#Sortie : Vrai si le jour correspond a aujourd'hui
def isToday (date:datetime.date) -> bool: 
    date_jour = datetime.date.today()
    return date_jour == date

#Fonction qui vérifie si la date en entrée au format date, est une date dans la semaine courante
#Entrée : date au format jour/mois/année
#Sortie : Vrai si le jour correspond a la semaine courante
def isWeek(date) : 
    date_jour = datetime.date.today()
    return 0<= date_jour.weekday() - (date_jour - date).days and date_jour.weekday() - (date_jour - date).days < 7


def main () :
    #On récupère l'image de thermomètre pour l'icone de l'onglet
    image_directory = '../Image/image_thermo.png'   
    image = Image.open(image_directory)

    #configuration de la page
    st.set_page_config(
    page_title = 'Frigentini Temperature',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = image,
    layout = 'wide'
    )

    st.title("Suivi de la temperature")
    st.markdown("## Page qui représente le suivi des températures journalière ou hebdomadaire")

    #récupération des données du CSV qui enregistre les relevés de température
    df_temperature = mn.get_data('../CSV/temperature.csv')

    df_temperature['date'] = pd.to_datetime(df_temperature['date'],dayfirst=True).dt.date

    #Mise en place de la zone de sélection permettant de choisir le détail d'affichage du graphique
    option = st.selectbox(
    "Quel détail pour le relevé ?",
    ("Journalier", "Hebdomadaire"),
    index=0,
    placeholder="Selectionner une fréquence ...",)

    #Action a effectuer si le champs de sélection est sur Journalier
    if option == "Journalier" : 
        filtered_df = df_temperature[df_temperature['date'].apply(isToday)]

        pd_temperature = pd.DataFrame(filtered_df)

        pd_temperature = pd_temperature.set_index("heure")

        st.line_chart(pd_temperature, y = "temperature")

    #Action a effectuer si le champs de sélection est sur Hebdomadaire
    if option == "Hebdomadaire" : 
        filtered_df = df_temperature[df_temperature['date'].apply(isWeek)]

        df_moyenne = filtered_df.groupby('date')['temperature'].mean().reset_index()

        pd_temperature = pd.DataFrame(df_moyenne)

        pd_temperature = pd_temperature.set_index("date")

        st.line_chart(pd_temperature, y = "temperature")



if __name__ == '__main__':
    main()
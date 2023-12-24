import streamlit as st
import Menu as mn
import datetime
from PIL import Image


#Fonction qui permet de savoir si une date du format jour/mois/année est dans moins du nombre de jour

def est_date_courte (date:str,nb_jour:int) -> bool:
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return diff <= nb_jour



def main() :

    image_directory = '../Image/icons8-fromage-50.png'   
    image = Image.open(image_directory)

    #Bouton toggle
    on = st.toggle('Option date courte')

    #condition si le bouton est activé
    if on:
        #Slider permettant de selectionner le nombre de jour a partir duquel on veut récupéré
        nb_jour = st.select_slider(
        "Selectionner le nombre de jour correspondant a une date courte",
        options=range(10),
        value=(3))
        #Recuperation du CSV
        df = mn.get_data('../CSV/frigo.csv')

        #On recupere seulement les lignes qui correspondent a nos jours de marge selectionné
        filtered_df = df[df['date_péremption'].apply(est_date_courte, nb_jour=nb_jour)]
        st.dataframe(filtered_df)

    #Condition si le toggle est eteint
    if not on :
        #On récupère le CSV
        df = mn.get_data('../CSV/frigo.csv')
        st.dataframe(df) 


if __name__ == '__main__':
    main()
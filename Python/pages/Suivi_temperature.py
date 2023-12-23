import pandas as pd
import Menu as mn
import streamlit as st
from PIL import Image


def main () :

    image_directory = '../Image/icons8-thermomètre-50.png'   
    image = Image.open(image_directory)

    st.set_page_config(
    page_title = 'Frigentini Temperature',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = image,
    layout = 'wide'
    )

    st.title("Suivi de la temperature")
    st.markdown("## Page qui représente le suivi des températures journalière ou hebdomadaire")

    df_temperature = mn.get_data('../CSV/temperature.csv')

    pd_temperature = pd.DataFrame(df_temperature)


    option = st.selectbox(
    "Quel détail pour le relevé ?",
    ("Journalier", "Hebdomadaire"),
    index=0,placeholder="Selectionner une fréquence ...",)

    if option == "Journalier" : 
        st.write("Affichage Journalier")
    
    if option == "Hebdomadaire" : 
        st.write("affichage hebdomadaire")


    st.line_chart(pd_temperature, y = "temperature")

if __name__ == '__main__':
    main()
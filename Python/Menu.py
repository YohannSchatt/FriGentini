import streamlit as st
import pandas as pd
from PIL import Image
import main as mn

#Commande pour lancer l'application
#streamlit run Menu.py
#!etre dans le repertoire Python
@st.cache_data
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

def main () :

    #Récupération de l'image pour l'icone de la page 
    image_directory = '../Image/icons8-frigo-50.png'
    image = Image.open(image_directory)

    #Configuration de la page
    st.set_page_config(
        page_title = 'Frigentini Dashboard', 
        page_icon = image,
        layout = 'wide'
    )

    st.title("Frigentini Dashboard")
    st.markdown("## Temperature and storage information")

    st.write("Bienvenu sur votre dashboard")

    #Gestion des metrics qui sont utilisés pour résumer l'etat de notre système
    #A rendre dynamique (Capturer la température au lancement de la page et compter les objets dans nos tables)
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", str(mn.menu.températureAct))
    col2.metric("Aliments", "5")
    col3.metric("Aliments périmée", "1")

if __name__ == '__main__':
    main()






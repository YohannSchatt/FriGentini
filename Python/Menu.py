import streamlit as st
import pandas as pd
import time # to simulate real time data
from PIL import Image

#streamlit run Menu.py
#!etre dans le repertoire Python
@st.cache_data
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

def main () :
    image_directory = '../Image/icons8-frigo-50.png'
    image = Image.open(image_directory)


    st.set_page_config(
        page_title = 'Frigentini Dashboard',  # important pour le référencement sur Google quand on hébergera l'app
        page_icon = image,
        layout = 'wide'
    )


    st.title("Frigentini Dashboard")
    st.markdown("## Temperature and storage information")

    st.write("Bienvenu sur votre dashboard")


    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "3 °C")
    col2.metric("Aliments", "5")
    col3.metric("Aliments périmée", "1")

if __name__ == '__main__':
    main()






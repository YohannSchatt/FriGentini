import streamlit as st
import pandas as pd
import time # to simulate real time data
from PIL import Image

#streamlit run Menu.py
#!etre dans le repertoire Python

image_directory = '../Image/icons8-frigo-50.png'
image = Image.open(image_directory)


st.set_page_config(
    page_title = 'Frigentini Dashboard',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = image,
    layout = 'wide'
)

@st.cache_data
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

st.title("Frigentini Dashboard")
st.markdown("## Temperature and storage information")

st.write("Bienvenu sur votre dashboard")








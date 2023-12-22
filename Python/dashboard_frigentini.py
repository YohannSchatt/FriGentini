import streamlit as st
import numpy as np
import pandas as pd
import time # to simulate real time data
import plotly.express as px # interactive charts
import matplotlib.pyplot as plt
from PIL import Image

#streamlit run dashboard_frigentini.py
#!etre dans le repertoire Python

image_directory = '../Image/icons8-frigo-50.png'
image = Image.open(image_directory)


st.set_page_config(
    page_title = 'Your Frigentini Dashboard',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = image,
    layout = 'wide'
)

@st.cache_data
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

df = get_data('../CSV/frigo.csv')
st.title("Frigentini Dashboard")
st.markdown("## Temperature and storage information")

df_temperature = get_data('../CSV/temperature.csv')

pd_temperature = pd.DataFrame(df_temperature)

# Prints the first lines of the filtered dataframe
st.dataframe(df) # prints only 5 lines


pd_temperature = pd_temperature.set_index("heure")

st.line_chart(pd_temperature, y = "temperature")



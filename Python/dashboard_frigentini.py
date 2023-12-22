import streamlit as st
import numpy as np
import pandas as pd
import time # to simulate real time data
import plotly.express as px # interactive charts
import matplotlib.pyplot as plt
from PIL import Image

#streamlit run dashboard_frigentini.py 

image_directory = '../Image/icons8-frigo-50.png'
image = Image.open(image_directory)


st.set_page_config(
    page_title = 'Your Frigentini Dashboard',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = image,
    layout = 'wide'
)

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv('../CSV/frigo.csv')

df = get_data()
st.title("Frigentini Dashboard")
st.markdown("## Temperature and storage information")

# Prints the first lines of the filtered dataframe
st.dataframe(df[0:10]) # prints only 5 lines

temperature = pd.DataFrame([[5,0],[4,1],[3,2],[2,3],[1,4],[-1,5],[3.2,6],[5,7],[10,8],[30,9],[35,10],[5,11],[5,12],[5,13],[5,14],[5,15],[5,16],[5,17],[5,18]],columns = ["temperature","hour"])

temperature2 = pd.DataFrame({
    "temp" : [3,2,6,8] ,
    "hour" : [0,9,10,14]}

)
temperature2 = temperature2.rename(columns={'hour':'index'}).set_index('index')

st.line_chart(temperature, y = ["temperature"])

st.line_chart(temperature2, y="temp")
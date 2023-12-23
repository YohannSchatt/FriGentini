import pandas as pd
import Menu as mn
import streamlit as st


st.title("Suivi de la temperature")
st.markdown("## Page qui représente le suivi des températures journalière ou hebdomadaire")

df_temperature = mn.get_data('../CSV/temperature.csv')

pd_temperature = pd.DataFrame(df_temperature)

st.line_chart(pd_temperature, y = "temperature")
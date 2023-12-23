import streamlit as st
import Menu as mn
import datetime

def est_date_courte (date:str,nb_jour:int) -> bool:
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return diff < nb_jour



on = st.toggle('Option date courte')

if on:
    nb_jour = st.select_slider(
    "Selectionner le nombre de jour correspondant a une date courte",
    options=range(10),
    value=(3))

    df = mn.get_data('../CSV/frigo.csv')

    st.write('Feature activated!')
    filtered_df = df[df['date_péremption'].apply(est_date_courte, nb_jour=nb_jour)]
    st.dataframe(filtered_df)

if not on :
    st.write("Option désactivé")
    df = mn.get_data('../CSV/frigo.csv')
    st.dataframe(df) 

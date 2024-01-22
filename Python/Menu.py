import streamlit as st
import pandas as pd
from PIL import Image
import pandas as pd
import datetime

#Commande pour lancer l'application
#streamlit run Menu.py
#!etre dans le repertoire Python
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

def est_périmé (date:str) -> bool : 
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return diff < 0

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

    with open('temperature.txt', 'r') as file:
        contenu = file.read()

    import pandas as pd

    # Spécifiez le chemin vers votre fichier CSV
    chemin_fichier_csv = '../CSV/frigo.csv'

    # Chargez le fichier CSV dans un DataFrame
    df = pd.read_csv(chemin_fichier_csv)

    # Obtenez le nombre de lignes en utilisant la propriété shape
    nombre_lignes = df.shape[0]

    filtered_df = df[df['date_péremption'].apply(est_périmé)]
    count_périmé = filtered_df.shape[0]

    #Gestion des metrics qui sont utilisés pour résumer l'etat de notre système
    #A rendre dynamique (Capturer la température au lancement de la page et compter les objets dans nos tables)
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", str(contenu))
    col2.metric("Aliments", str(nombre_lignes))
    col3.metric("Aliments périmée", "1")

    refresh_button = st.button("Refresh")

    # Vérifiez si le bouton a été cliqué
    if refresh_button:
        # Utilisez le module streamlit pour forcer le rafraîchissement
        st.experimental_rerun()

if __name__ == '__main__':
    main()






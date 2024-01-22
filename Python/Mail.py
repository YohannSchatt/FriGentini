#Fichier qui permet la gestion de l'envoie des différents mail
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

#Fonction qui renvoie le Datadrame étant l'image du CSV passée en paramètre
def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

#Fonction qui vérifie si la date de péremption est antérieur a la date actuelle
#Entrée : date au format jour/mois/année
#True si la date est antérieur a celle d'aujourd'hui sinon False
def est_périmé (date:str) -> bool : 
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return diff < 0

#Fonction qui renvoie si une date est dans dans moins d'un certain nombre de jour mais pas encore passé
#Entrée : date au format jour/mois/année
#True si 0 <= date <= nb_jour sinon False
def est_date_courte (date:str,nb_jour:int) -> bool:
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return  0 <= diff <= nb_jour

#Fonction qui permet d'envoyer un mail dans nos condition
#Entrée : le contenu du mail sous le format html
def envoyer_mail (texte):
    #Serveur d'envoie
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    #Information de l'envoyeur
    email_address = 'frigentini@gmail.com' #adresse mail de l'envoyeur
    email_password = 'bzkj puyn afbc rghm ' #Code application fournit par Google lors de la création d'un accès application

    #Mail du destinataire, a change en fonction des demandes de l'utilisateur
    #A ajouter un parametre qui permet de spécifier le destinataire ainsi qu'une interface pour la définir
    email_receiver = 'mathnor01@gmail.com'


    # Instance de mail
    message = MIMEMultipart("MAJ produits")
    # on ajoute un sujet
    message["Subject"] = "Point sur les produits"
    # un émetteur
    message["From"] = email_address
    # un destinataire
    message["To"] = email_receiver

    #Instance d'un objet pour le corps du mail
    html_mime = MIMEText(texte, 'html')

    #Ajout de l'objet html a l'objet message
    message.attach(html_mime)

    # on crée la connexion 
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        # connexion au compte
        server.login(email_address, email_password)
        # envoi du mail
        server.sendmail(email_address, email_receiver, message.as_string())


def mail_MAJ_produit ():
    #Recupération du Dataframe du CSV frigo 
    df = get_data('../CSV/frigo.csv')

    #On recupere seulement les lignes qui correspondent a nos jours de marge selectionné
    filtered_df = df[df['date_péremption'].apply(est_date_courte, nb_jour=3)]
    df1 = get_data('../CSV/liste_produits.csv') #On récupère la liste des produits existants
    df2 = pd.merge(filtered_df,df1,left_on= 'Type_Produit',right_on='Code_barre')#Join de la liste des produits sur le stockage pour avoir le nom des produits


    filtered_df = df[df['date_péremption'].apply(est_périmé)] #Récupération du dataframe avec seulement les produits périmés
    df3 = pd.merge(filtered_df,df1,left_on= 'Type_Produit',right_on='Code_barre')#Liste des produits périmés avec le nom des produits

    # Contenu du mail en format html
    html = '''
    <html>
    <body>
    <h1>Liste des produits périmés et proche de la date</h1>
    <p>Produits périmés : </p><br>
    <table border="1">
        <tr>
            <th>Produit</th>
            <th>Date de Péremption</th>
        </tr>'''+ formattage(df3)+ '''
    </table>

    <p>Produit proche de la péremption (3jours) : </p>
    <table border="1">
        <tr>
            <th>Produit</th>
            <th>Date de Péremption</th>
        </tr>'''+formattage(df2) +'''
    </table>
    <b>Cdt</b> <br>
    </body>
    </html>
    '''
    envoyer_mail(html)

#Permet d'éditer le mail de notification de démarrage du système
def mail_demarrage ():
    html = '''
    <html>
    <body>
    <h1>Notification de démarrage</h1>
    <p>Demarrage de la carte</p>
    </body>
    </html>
    '''
    envoyer_mail(html)

#Permet d'éditer le mail de notification d'arret du système
def mail_arret ():
    html = '''
    <html>
    <body>
    <h1>Notification d'arret</h1>
    <p>Le systeme vient d'etre arreté</p>
    </body>
    </html>
    '''
    envoyer_mail(html)

#Permet de retourner d'après le dataframe l'image du tableau html avec nom, date de péremption, au format html
def formattage (df : pd.DataFrame) -> str: 
    sortie = ""
    #On parcours toutes les lignes du Dataframe
    for i in df.index:
        ligne = df[["nom","date_péremption"]].iloc[i].values[0:2]#On recupère les valeurs de nom et date péremption 
        nom = ligne[0]
        date = ligne[1]
        #Concatéation du string repésentant l'html
        sortie += "<tr>\n"
        sortie += "<td>" + str(nom) + "</td>\n"
        sortie += "<td>" + str(date) + "</td>\n"
        sortie += "</tr>\n"
    return sortie
        






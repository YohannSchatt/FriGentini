#https://datascientest.com/comment-envoyer-un-e-mail-avec-python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

def get_data(chemin) -> pd.DataFrame:
    return pd.read_csv(chemin)

def est_périmé (date:str) -> bool : 
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return diff < 0


def est_date_courte (date:str,nb_jour:int) -> bool:
    auj = datetime.datetime.today()
    diff =  -(auj - datetime.datetime.strptime(date,'%d/%m/%Y')).days
    return  0 <= diff <= nb_jour

def envoyer_mail (texte):
    # on rentre les renseignements pris sur le site du fournisseur
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    # on rentre les informations sur notre adresse e-mail
    email_address = 'frigentini@gmail.com'
    email_password = 'bzkj puyn afbc rghm '

    # on rentre les informations sur le destinataire
    email_receiver = 'mathnor01@gmail.com'


    # on crée un e-mail
    message = MIMEMultipart("MAJ produits")
    # on ajoute un sujet
    message["Subject"] = "Point sur les produits"
    # un émetteur
    message["From"] = email_address
    # un destinataire
    message["To"] = email_receiver
    # on rentre les renseignements pris sur le site du fournisseur
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    html_mime = MIMEText(texte, 'html')

    message.attach(html_mime)

    # on crée la connexion 
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        # connexion au compte
        server.login(email_address, email_password)
        # envoi du mail
        server.sendmail(email_address, email_receiver, message.as_string())


def mail_MAJ_produit ():
    df = get_data('../CSV/frigo.csv')


    #On recupere seulement les lignes qui correspondent a nos jours de marge selectionné
    filtered_df = df[df['date_péremption'].apply(est_date_courte, nb_jour=3)]
    df1 = get_data('../CSV/liste_produits.csv')
    df2 = pd.merge(filtered_df,df1,left_on= 'Type_Produit',right_on='Code_barre')#Liste des produits proche de la date < 3 jours


    filtered_df = df[df['date_péremption'].apply(est_périmé)]
    df3 = pd.merge(filtered_df,df1,left_on= 'Type_Produit',right_on='Code_barre')#Liste des produits périmés 
    # sa version HTML
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


def formattage (df : pd.DataFrame) -> str: 
    sortie = ""
    for i in df.index:
        ligne = df[["nom","date_péremption"]].iloc[i].values[0:2]
        nom = ligne[0]
        date = ligne[1]
        sortie += "<tr>\n"
        sortie += "<td>" + str(nom) + "</td>\n"
        sortie += "<td>" + str(date) + "</td>\n"
        sortie += "</tr>\n"
    return sortie
        
        
mail_demarrage()
mail_MAJ_produit()





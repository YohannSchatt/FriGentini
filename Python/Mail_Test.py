#https://datascientest.com/comment-envoyer-un-e-mail-avec-python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    </tr>
    <tr>
        <td>Pain</td>
        <td>2024-01-31</td>
    </tr>
    <tr>
        <td>Lait</td>
        <td>2024-02-15</td>
    </tr>
</table>


<p>Produit proche de la péremption (3jours) : </p>
<table border="1">
    <tr>
        <th>Produit</th>
        <th>Date de Péremption</th>
    </tr>
    <tr>
        <td>Pain</td>
        <td>2024-01-31</td>
    </tr>
    <tr>
        <td>Lait</td>
        <td>2024-02-15</td>
    </tr>
</table>
<b>Cdt</b> <br>
</body>
</html>
'''


html_mime = MIMEText(html, 'html')

message.attach(html_mime)

# on crée la connexion
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
  # connexion au compte
  server.login(email_address, email_password)
  # envoi du mail
  server.sendmail(email_address, email_receiver, message.as_string())

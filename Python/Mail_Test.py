import smtplib, ssl

# on rentre les renseignements pris sur le site du fournisseur
smtp_address = 'smtp.gmail.com'
smtp_port = 465

# on rentre les informations sur notre adresse e-mail
email_address = 'frigentini@gmail.com'
email_password = 'polytech'

# on rentre les informations sur le destinataire
email_receiver = 'mathnor01@gmail.com'

# on crée la connexion
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
  # connexion au compte
  server.login(email_address, email_password)
  # envoi du mail
  server.sendmail(email_address, email_receiver, 'le contenu de l\'e-mail')
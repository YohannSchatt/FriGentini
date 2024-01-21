import datetime
date_jour = datetime.datetime.today()
diff =  -(date_jour - datetime.datetime(2024, 1, 21, 3))

print((diff.seconds)/3600)

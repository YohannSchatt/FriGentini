#Connected to I2C-0
#Fichier qui permet la gestion du thermometre
import time
import board
from adafruit_dps310.basic import DPS310

i2c = board.I2C()  # uses board.SCL and board.SDA
dps310 = DPS310(i2c)

#Fonction qui permet de récupérer la température relevé par notre thermometre
def ReadTemperature():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    dps310 = DPS310(i2c)
    return dps310.temperature
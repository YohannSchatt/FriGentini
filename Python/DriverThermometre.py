#Connected to I2C-0
import time
import board
from adafruit_dps310.basic import DPS310

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
dps310 = DPS310(i2c)

def ReadTemperature():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    dps310 = DPS310(i2c)
    return dps310.temperature
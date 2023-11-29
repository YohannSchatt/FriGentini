#Connected to I2C-3
import hp206c
h= hp206c.hp206c()

ret=h.isAvailable()
if h.OK_HP20X_DEV == ret:
    print("HP20x_dev is available.")
else:
    print("HP20x_dev isn't available.")
    
temp=h.ReadTemperature()
pressure=h.ReadPressure()
altitude=h.ReadAltitude()
print("Temperature\t: %.2f C\nPressure\t: %.2f hPa\nAltitude\t: %.2f m" %(temp,pressure,altitude))
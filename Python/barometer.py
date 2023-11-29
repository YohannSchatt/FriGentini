#Connected to I2C-3
import hp206c as hp
h= hp.hp206c()
temp=h.ReadTemperature()
print(temp)
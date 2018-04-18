import Adafruit_BMP.BMP085 as BMP

sensor = BMP.BMP085()

print('Temp: {}'.format(sensor.read_temperature()))
print('Pres: {}'.format(sensor.read_pressure()))
print('Alti: {}'.format(sensor.read_altitude()))

import Adafruit_ADS1x15
import time
from math import pow

adc = Adafruit_ADS1x15.ADS1115()

def convert_lux(value):
    a4 = 5.893358146e-13
    a3 = -1.400831211e-8
    a2 = 1.226504657e-4
    a1 = -4.741469289e-1
    C = 710.2720872
    return (a4 * pow(value, 4)) + (a3 * pow(value, 3)) + (a2 * pow(value, 2)) + (a1 * pow(value, 1)) + C

while True:
    value = adc.read_adc(0, 1)
    lux = convert_lux(value)
    print('Lux: {}'.format(lux))
    time.sleep(0.25)

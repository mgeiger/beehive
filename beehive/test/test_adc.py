import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

for i in range(0, 4):
    print("{}: {}".format(i, adc.read_adc(i)))

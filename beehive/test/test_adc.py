import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

for i in range(0, 4):
    adc_value = adc.read_adc(i)
    print("{}: {}".format(i, adc_value) 

import Adafruit_DHT
import time

DHT_TYPE = 22
DHT_GPIO = 23

for i in range(0, 10):
    values = Adafruit_DHT.read_retry(DHT_TYPE, DHT_GPIO)
    print('Values: {}'.format(values))
    time.sleep(2)

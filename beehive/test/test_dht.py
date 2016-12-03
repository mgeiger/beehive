import Adafruit_DHT

DHT_TYPE = 22
DHT_GPIO = 23

values = Adafruit_DHT.read_retry(DHT_TYPE, DHT_GPIO)
print('Values: {}'.format(values))

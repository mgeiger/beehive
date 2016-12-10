#!/usr/bin/python3
import Adafruit_DHT
import Adafruit_ADS1x15
import Adafruit_BMP.BMP085 as BMP
import time
import requests
import json
from math import pow
import logging

DHT_TYPE = 22
DHT_GPIO = 23
ADDRESS = 0x48
GAIN = 1
LIGHT_ADC = 0
URI = 'http://192.168.0.5:5000/add'

adc = Adafruit_ADS1x15.ADS1115()
sensor = BMP.BMP085()

class sensor:
    self.last_value = None

    def __init__():
        self.last_acquire = time.now()

    def get_value():
        return self.last_value

    def get_unit():
        return "N/A"


def dht_sensor(sensor):


def acquire_dht():
    return Adafruit_DHT.read_retry(DHT_TYPE, DHT_GPIO)

def convert_lux(value):
    a4 = 5.893358146e-13
    a3 = -1.400831211e-8
    a2 = 1.226504657e-4
    a1 = -4.741469289e-1
    C = 710.2720872
    return (a4 * pow(value, 4)) + (a3 * pow(value, 3)) + (a2 * pow(value, 2)) + (a1 * pow(value, 1)) + C

def acquire_light():
    return convert_lux(adc.read_adc(LIGHT_ADC, gain=GAIN))

def main():
    total_light = 0.0
    total_humidity = 0.0
    total_temperature = 0.0
    total_t2 = 0.0
    total_pressure = 0.0
    total_altitude = 0.0
    count = 0.0
    try:
        while True:
            if count >= 10.0:
                # Generate the data
                sensor_dict = {}
                sensor_dict['light'] = total_light / count
                sensor_dict['humidity'] = total_humidity / count
                sensor_dict['temperature'] = total_temperature / count
                sensor_dict['temperature2'] = total_t2 / count
                sensor_dict['pressure'] = total_pressure / count
                sensor_dict['altitude'] = total_altitude / count
                try:
                    # Post Everything
                    requests.post(URI, json.dumps(sensor_dict))
                except requests.exceptions.Timeout:
                    # Try again?
                    print('We timed out.')
                    continue
                except requests.exceptions.TooManyRedirects:
                    print('Too many redirects failure.')
                    continue
                except requests.exceptions.RequestException:
                    print('Bad error for requests.')
                    continue
                # Reset Everything
                total_light = 0.0
                total_humidity = 0.0
                total_temperature = 0.0
                total_t2 = 0.0
                total_pressure = 0.0
                count = 0.0
            humidity, temperature = acquire_dht()
            light = acquire_light()
            total_humidity += humidity
            total_temperature += temperature
            total_light += light
            total_t2 += sensor.read_temperature()
            total_pressure += sensor.read_pressure()
            total_altitude += sensor.read_altitude()
            count += 1.0
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting")

if __name__ == "__main__":
    main()

# Overview
Source code for local beehive monitoring.
Project includes all sensor 

# Todo
- [ ] Layout the Hardware system 
- [ ] Figure out if I'm going to use the AD Convertor (ADS1x15)
- [ ] Investigae Weight Sensor system
- [ ] Need to figure out how to handle the API to get random numbers for the test code system

# Hardware
## Sensor Hardware
1. BMP180
1. DHT22
1. DS18B20 (4 or 5x)
1. Light Sensor ()

### DS18B20
A digital temperature sensor.
This is a "1-wire" sensor that can be connected in parallel.
All sensors share the same pin and will only need 4.7K resistor between them all if they are connected in parallel.
You can run in parasite mode. Data and ground just connects, you don't need to connect the power positive.
You can sample every 750ms.
The waterproof item will have three leads: red, black, yellow.
Red goes to the power positive connection.
Black goes to the negative or ground rail.
The yellow will connect to the GPIO pin, with a 4.7-10K from data to 3.3V.

You will need to setup onewire support on the Raspberry Pi.
In /boot/config.txt, add the following to the bottom:
dtoverlay=w1-gpio

run the following after a reboot:
- sudo modprobe w1-gpio
- sudo modprobe w1-therm
- cd /sys/bus/w1/devices
- ls
- cd 28-xxxxx (Change this to match what your serial number is)
- cat w1_slave

The first two lines...I'm not too sure what is going on there. I need to get more information.

If you read the output from w1_slave, you will see t= which is the temperature in 1000ths of degrees celcius.
The "crc=da YES" means the sensor is working, you should check for that.

### BMP180
You can get altitude, temperature and pressure off this system. 

You need to enable i2c on raspi-config.
Reboot the system.
Install the following: python-smbus i2c-tools.
Check to see if i2c is enabled: lsmod | grep i2c_. Look for something like i2c_bcm2708.

For Model A, B rev 2, or B+, run sudo i2cdetect -y 1
For Mobel B rev 1, sudo i2cdetect -y 0

You need to setup the GPIO for this,
VCC - 3.3V P1-01
GND - Ground P1-06
SCL i2c SCL P1-05
SDA i2c SDA P1-03
3.3V Not needed.

For python
import smbus
smbus.SMBus(0) or 1

There is some code here: https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bmp180.py

### DHT22
I like this one more than the DHT11. 

You can only query this every once or two seconds. DHT22 has a resolution of 0.5degC with 2-5% RH.

Pins:
1. VCC 3.3 to 5V (left most when look at front with pins down)
2. Data Out
3. NC
4. Ground Wire

You need to put a 10k pullup between VCC and the data pin.

You need to have to pip items installed RPi (RPi.GPIO as GPIO) and Adafruit_DHT.
I should look at the later and figure out if I can make this cleaner.
There is some good details here:
http://www.home-automation-community.com/temperature-and-humidity-from-am2302-dht22-sensor-displayed-as-chart/

### Analog to Digital Converter (ADC)
I have an ADS1115 at home. It is a 16bit 4-channel ADC. 
VCC to RPi 3.3V
SDA to SDA
SCL to SCL
GND to GND

Use I2C Bus 1 (Pins 3 and 5), not I2C Bus 0 (pins 27 and 28).

This will have the light sensor and the ligth sensor.


## Sensors Locations
- Temperatures
  - Bottom Brood Super
  - Top Brood Super
  - Bottom Honey Super
  - Top Honey Super
  - External
  - Hive Entrance
- Humidity
  - Hive Entrance
  - Middle of Hive
  - External
- Other
  - Altitude
  - Light

# Software
## Database Storage
Will be using Postgres as our database storage. 
The other idea is to use InfluxDB or Graphite. 
Both of these databases are good for time-series data storage.



# Reference
## Blogs to View

Other Setups
------------
- https://hackaday.io/project/2453-arduino-beehive-monitor
- https://hackaday.io/project/1741-honeybee-hive-monitoring
- https://www.kickstarter.com/projects/hivemind/innovative-wireless-beehive-scales/description

##### Video Monitoring
http://dansbeehives.blogspot.com/2013/07/fully-automated-beehive-surveillance.html

##### Bee Monitoring
- http://annemariemaes.net/tag/bee-monitoring/
- http://hivetool.org/w/index.php?title=HiveTool.org

##### Integrating to Xively Feed
https://hackaday.io/project/2453-arduino-beehive-monitor

Datalogging
-----------
- https://www.circuits.dk/datalogger-example-using-sense-hat-influxdb-grafana/
- http://docs.gadgetkeeper.com/pages/viewpage.action?pageId=7700673
- https://rethinkdb.com/blog/temperature-sensors-and-a-side-of-pi/
- http://www.instructables.com/id/Raspberry-Pi-Temperature-Logger/
- https://www.raspberrypi-spy.co.uk/2015/06/basic-temperature-logging-to-the-internet-with-raspberry-pi/
- http://www.instructables.com/id/Raspberry-datalogger-with-Mysql-Highcharts/

With Frontend
-------------
- https://github.com/geerlingguy/temperature-monitor

Database Choice
---------------
- https://mike.depalatis.net/blog/postgres-time-series-database.html
- http://www.postgresqltutorial.com/postgresql-python/connect/
- https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=6335

Battery monitoring
------------------
- https://blog.adafruit.com/2017/01/27/remote-battery-monitoring-piday-raspberrypi-raspberry_pi/

Bee Counting
------------
- http://www.instructables.com/id/Honey-Bee-Counter-II/

Control System
--------------
- https://lifehacker.com/how-to-control-a-raspberry-pi-remotely-from-anywhere-in-1792892937

#!/usr/bin/python3
import sqlite3 as lite
import logging
import sys

table_name = 'sensor_values'
col_date_time = 'date_time'
col_temperature = 'temperature'
col_temp2 = 'temperature2'
col_pressure = 'pressure'
col_altitude = 'altitude'
col_humidity = 'humidity'
col_light = 'light'
create = "CREATE TABLE IF NOT EXISTS {}({} DATETIME PRIMARY KEY NOT NULL, {} REAL, {} REAL, {} REAL);".format(table_name, col_date_time, col_temperature, col_humidity, col_light)
database_file = '/home/pi/beehive/beehive.db'
create_sql = """
CREATE TABLE IF NOT EXISTS {}({} DATETIME PRIMARY KEY NOT NULL, 
{} REAL, {} REAL, {} REAL, 
{} REAL, {} REAL, {} REAL);""".format(table_name, col_date_time, 
        col_temperature, col_temp2, col_humidity, 
        col_pressure, col_altitude, col_light)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    con = lite.connect(database_file)
    try:
        logging.debug('Acquired database')
        cur = con.cursor()
        cur.execute(create_sql)
        con.commit()
    except lite.Error:
        e = sys.exc_info()[0]
        logging.error(e.args[0])
    finally:
        if con:
            con.close()

def insert_database(temperature=None, temperature2=None, humidity=None, pressure=None, altitude=None, light=None):
    insert = "INSERT INTO {} VALUES(datetime('now'), {}, {}, {}, {}, {}, {});".format(table_name, temperature, temperature2, humidity, pressure, altitude, light)
    con = lite.connect(database_file)
    try:
        logging.debug('Inserting into database')
        cur = con.cursor()
        cur.execute(insert)
        con.commit()
    except lite.Error:
        e = sys.exc_info()[0]
        logging.error(e.args[0])
    finally:
        if con:
            con.close()

def get_averages():
    query = "SELECT DATETIME((STRFTIME('%s', date_time) / 900) * 900, 'unixepoch', 'localtime') interval, avg(temperature) temperature, avg(temperature2) temperature2, avg(humidity) humidity, avg(pressure) pressure, avg(altitude) altitude, avg(light) light from sensor_values where date_time > datetime('now', '-1 day') group by interval order by interval;"
    con = lite.connect(database_file)
    try:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
    except lite.Error:
        e = sys.exc_info()[0]
        logging.error(e.args[0])
    finally:
        if con:
            con.close()
    
    # Now do something with the data...
    if not data or len(data) < 1:
        return None

    return {'time': [x[0] for x in data], 
            'temperature': [x[1] for x in data],
            'temperature2': [x[2] for x in data],
            'humidity': [x[3] for x in data],
            'pressure': [x[4] for x in data],
            'altitude': [x[5] for x in data],
            'light': [x[6] for x in data]}

if __name__ == "__main__":
    print(get_averages())

import sqlite3 as lite
from sensors import convert_lux

database_file = '/home/pi/beehive/beehive.db'
table_name = 'sensor_values'
column_name = 'light'
time_column = 'date_time'
select_all_query = 'SELECT {}, {} FROM {}'.format(column_name, time_column, table_name)

def update_light(conn, l_t):
    sql = ''' UPDATE sensor_values
              SET light = ?
              WHERE date_time = ?; '''
    cur = conn.cursor()
    cur.execute(sql, l_t)

try:
    con = lite.connect(database_file)
    cur = con.cursor()
    cur.execute(select_all_query)
    rows = cur.fetchall()

    print('Found {} rows.'.format(len(rows)))

    for i, row in enumerate(rows):
        lux_value = convert_lux(row[0] * 100)
        print('[{}/{}] {}: {:.2f} ADC to {:.2f} LUX'.format(i + 1, len(rows), row[1], row[0], lux_value))  
        update_light(con, row)

finally:
    if con:
        con.close()

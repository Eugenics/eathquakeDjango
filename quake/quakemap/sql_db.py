import datetime
import sqlite3
from sqlite3 import Error
from .get_json import get_json_data
from quake.settings import BASE_DIR
import os


def create_db_connection():
    conn = None

    try:
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    except Error as e:
        print(e)

    return conn


def insert_eathquake(sql_object):
    conn = create_db_connection()

    sql_string = '''INSERT INTO quakemap_eathquake(session_id,src,id_eathquake,version
                        ,eathquake_time,lat,lng,mag,depth,nst,region,data_source,create_date,url)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

    try:
        with conn:
            sql_cursor = conn.cursor()
            sql_cursor.execute(sql_string, sql_object)
    except Error as e:
        print(e)

    # return sql_cursor.lastrowid


def create_row(feature, session_id):

    properties = feature['properties']
    geometry = feature['geometry']
    coordinates = geometry['coordinates']

    local_date_time = datetime.datetime.strptime(
        '1970-01-01' + ' 0:0:0.0', "%Y-%m-%d %H:%M:%S.%f")
    local_date_time = local_date_time + \
        datetime.timedelta(milliseconds=properties['time'])

    sql_object = (session_id,
                    properties['sources'],
                    feature['id'],
                    '1',
                    local_date_time,
                    coordinates[0],
                    coordinates[1],
                    properties['mag'],
                    coordinates[2],
                    properties['nst'],
                    properties['place'],
                    'usgs-gov',
                    datetime.datetime.now(),
                    properties['url']
                  )

    row_id = insert_eathquake(sql_object)

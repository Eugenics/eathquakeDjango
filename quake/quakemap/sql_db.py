import datetime
import sqlite3
from sqlite3 import Error
from quake_code.quakemap import get_json


def create_db_connection():
    conn = None

    try:
        conn = sqlite3.connect("db.sqlite3")
    except Error as e:
        print(e)

    return conn


def insert_eathquake(conn, sql_object):
    sql_string = ''' INSERT INTO quakemap_eathquake(session_id,src,id_eathquake,version
                        ,eathquake_time,lat,lng,mag,depth,nst,region,data_source,create_date
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                    # WHERE id_eathquake <> ?

    sql_cursor=conn.cursor()
    sql_cursor.execute(sql_string, sql_object)

    return sql_cursor.lastrowid


def create_row():
    conn=create_db_connection()

    features=get_json_data('2020-01-13', '2020-01-14')

    for feature in features:
        properties=feature['properties']
        geometry=properties['geometry']
        coordinates=geometry['coordinates']

        local_date_time=datetime.datetime.strptime(
            '1970-01-01' + ' 0:0:0.0', "%Y-%m-%d %H:%M:%S.%f")
        local_date_time=local_date_time + datetime.timedelta(milliseconds = properties['time'])

        sql_object=(''
            , properties['sources']
            , feature['id']
            , '1'
            , local_date_time
            , coordinates[0]
            , coordinates[1]
            , properties['mag']
            , coordinates[2]
            , properties['nst']
            , properties['place']
            , 'usgs-gov'
            , datetime.datetime.now()
        ) 

        with conn:
            row_id = insert_eathquake(conn,sql_object)

if __name__ == "__main__":
    create_row()

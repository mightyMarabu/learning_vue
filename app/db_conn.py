import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request

import mysql.connector
from mysql.connector import Error

import pymysql.cursors

# postgres connection
mov_db = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.44', port='5432', password='service_3000')
# mov_db = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.45', port='5432', password='service_3000')

############################ API ########################################
def getMyBox(id):
    connect = psycopg2.connect(dbname='mov_db', user='rhino', host='192.168.3.44', port='5432', password='stevieB')
    cur = connect.cursor(cursor_factory = RealDictCursor)
    cur.execute("select id, laenge, breite, hoehe from measure.box where id = %s",(id,))
    box = cur.fetchall()
    connect.commit()
    connect.close()
    return box
    print ("box info")

def getMyMeasureData(aid):
    connect = psycopg2.connect(dbname='mov_db', user='rhino', host='192.168.3.44', port='5432', password='stevieB')
    cur = connect.cursor(cursor_factory = RealDictCursor)
    cur.execute("select p_id, level, date::text as date, u, l_l, a_p, dist2zero from measure.torso where a_id = %s", (aid,))
    #cur.execute("select p_id, level from measure.torso where a_id = %s", (aid,))
    pmdata = cur.fetchall()
    connect.commit()
    connect.close()
    return pmdata

def saveMyConfig(json):
    connect = psycopg2.connect(dbname='mov_db', user='rhino', host='192.168.3.44', port='5432', password='stevieB')
    cur = connect.cursor()
    cur.execute("select measure.saveConfig(%s)",(json,))
    #config = cur.fetchall()
    connect.commit()
    connect.close()
    print("config saved")

def getMyConfig(id):
    connect = psycopg2.connect(dbname='mov_db', user='rhino', host='192.168.3.44', port='5432', password='stevieB')
    cur = connect.cursor()
    cur.execute("select config from measure.config where (config ->> 'id') = %s",(id,))
    myconfig = cur.fetchall()
    connect.commit()
    connect.close()
    return myconfig
    print("config loaded")
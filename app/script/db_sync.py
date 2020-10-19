#!/usr/bin/env python

####### db-sync ###########################################################
import pymysql

import pandas as pd

from sqlalchemy import create_engine
import psycopg2 
from psycopg2.extras import RealDictCursor

import io
import datetime


p = "SELECT id, name, vorname, geburtsdatum, strasse, plz, ort, telefon, telefon_mobil FROM `hecrasoft-movimento`.patienten;"
m = "SELECT id, name, vorname, geburtsdatum, strasse, plz, ort FROM `hecrasoft-movimento`.adresse where firma like 'Movi%' and id_adressart = 7;"
a = "select id, case when id_filiale = 1 then 'KS' when id_filiale = 2 then 'GÖ' end as filiale, bemerkung, kostenstelle, erstellt_am, case when geplante_abgabe_am = '0000-00-00' then CAST('3000-01-01' as date) else geplante_abgabe_am END  as geplante_abgabe_am from `hecrasoft-movimento`.auftraege where unix_timestamp(storno_am) = 0"

p2a = "SELECT id_patienten as pid, id as aid from `hecrasoft-movimento`.auftraege where (unix_timestamp(storno_am) = 0 or storno_am is null)"
m2a = "select id_ma_werkstatt as mid, id as aid from `hecrasoft-movimento`.auftraege where unix_timestamp(storno_am) = 0"
p2u = "select id as pid, id_kassen as kid, id_aerzte as aeid, id_aerzte2 as aeid2, id_aerzte3 as aeid3, id_aerzte4 as aeid4, id_einrichtung as eid, id_therapeut as thid, id_therapeut2 as thid2 from `hecrasoft-movimento`.patienten"

l = "SELECT id, firma, name, vorname, geburtsdatum, strasse, plz, ort, telefon, telefax, email, internet, kundennr from `hecrasoft-movimento`.lieferanten"
ls = "SELECT lfdnum as id, id_auftraege as aid, erstellt_am, gedruckt_am, unterschrieben_am from `hecrasoft-movimento`.lieferschein"


pgp = "select * from patients"
pga = "select id, filiale, bemerkung, kostenstelle, erstellt_am, geplante_abgabe_am::date from auftraege"
pgm = "select * from mitarbeiter"
pgp2a = "select * from p2a"
pgm2a = "select * from m2a"
pgp2u = "select * from p2u"

def getPGData(pg_Query):
    try:
        #connect = psycopg2.connect(dbname='mov_db', user='postgres', host='192.168.3.157', port='54321', password='postgres')
        connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.44', port='5432', password='postgres')
        cur = connect.cursor(cursor_factory = RealDictCursor)
        cur.execute(pg_Query)
        pg_data = cur.fetchall()
        connect.commit()
        connect.close()
    except:
        print("Error") 
    else:    
        print ("pg data loaded: "+pg_Query)
        return pg_data
    finally:
        print("everything went fine!")


df_p = pd.DataFrame(getData(p))
df_m = pd.DataFrame(getData(m))
df_p2a = pd.DataFrame(getData(p2a))
df_m2a = pd.DataFrame(getData(m2a))
df_p2u = pd.DataFrame(getData(p2u))
df_a = pd.DataFrame(getData(a))
df_l = pd.DataFrame(getData(l))
df_ls = pd.DataFrame(getData(ls))
print ("Hecrasoft-Data sucessfully loaded!")
# get pg-Data
df_pgp = pd.DataFrame(getPGData(pgp))
df_pgm = pd.DataFrame(getPGData(pgm))
df_pgp2a = pd.DataFrame(getPGData(pgp2a))
df_pgm2a = pd.DataFrame(getPGData(pgm2a))
df_pgp2u = pd.DataFrame(getPGData(pgp2u))
df_pga = pd.DataFrame(getPGData(pga))
print ("postgres-Data sucessfully loaded!")
df_diff_p = pd.concat([df_pgp, df_p], sort=False).loc[df_pgp.index.symmetric_difference(df_p.index)]
df_diff_a = pd.concat([df_pga, df_a], sort=False).loc[df_pga.index.symmetric_difference(df_a.index)]
df_diff_m = pd.concat([df_pgm, df_m], sort=False).loc[df_pgm.index.symmetric_difference(df_m.index)]
df_diff_p2a = pd.concat([df_pgp2a, df_p2a], sort=False).loc[df_pgp2a.index.symmetric_difference(df_p2a.index)]
df_diff_m2a = pd.concat([df_pgm2a, df_m2a], sort=False).loc[df_pgm2a.index.symmetric_difference(df_m2a.index)]
df_diff_p2u = pd.concat([df_pgp2u, df_p2u], sort=False).loc[df_pgp2u.index.symmetric_difference(df_p2u.index)]
print("differences checked!")
engine = create_engine('postgresql+psycopg2://service_user:service@192.168.3.44:5432/mov_db')
#engine = create_engine('postgresql+psycopg2://service_user:service@192.168.3.157:54321/mov_db')
df_diff_p.to_sql('patients', engine, if_exists='append',index=False)
df_diff_a.to_sql('auftraege', engine, if_exists='append',index=False)
df_diff_m.to_sql('mitarbeiter', engine, if_exists='append',index=False)
df_diff_p2a.to_sql('p2a', engine, if_exists='append',index=False)
df_diff_m2a.to_sql('m2a', engine, if_exists='append',index=False)
#df_diff_p2u.to_sql('p2u', engine, if_exists='append',index=False)
print("data loaded to postgres!")
connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.44', port='5432', password='postgres')
cur = connect.cursor(cursor_factory = RealDictCursor)
cur.execute('select company.update_tables();')
print("update completed")
cur.execute('TRUNCATE public.lieferschein;')
connect.commit()
connect.close()
df_ls.to_sql('lieferschein', engine, if_exists='append',index=False)
print("update lieferschein")    
now = datetime.datetime.now()
print("db-sync completed:"+now.strftime("%Y-%m-%d %H:%M:%S"))

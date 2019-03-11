from contextlib import contextmanager
import os
from legi.models import db_proxy, DBMeta, DuplicateFile, Conteneur, Texte, Sommaire, Section
from playhouse.db_url import connect
from peewee import fn


db = connect("postgresql://legipy:dilamite@localhost/kali2")
# db = connect("sqlite:///KALI.sqlite")
db_proxy.initialize(db)

section = Section.select().where(Section.id == "KALISCTA000032074276").dicts().first()
# Texte.select(Texte.id).order_by(Texte.id.desc()).limit(1)[0] + 1

# r = db.commit()
print("sommaires is %s" % section)

# res3 = db.execute_sql("delete from db_meta where value='yolo';")
# db.commit()

# res1 = DBMeta.create(key='test1', value="yolo")
# print("res1 is %s" % res1)
# res2 = DBMeta.create(key='test2', value="yolo")
# print("res2 is %s" % res2)
# res3 = db.execute_sql("delete from db_meta where value='yolo';")
# print("res3 is %s" % res3)
# res4 = db.commit()
# print("res4 is %s" % res4)

# res = Conteneur.get(Conteneur.id == 'KALICONT000030400200').id

# print("'%s'" % res)

# import psycopg2
# conn = psycopg2.connect("dbname=kali user=legipy password=dilamite")
# cur = conn.cursor()
# cur.execute("SELECT id FROM conteneurs WHERE id='KALICONT000030400200'")
# res = cur.fetchone()
# print("'%s'" % res)

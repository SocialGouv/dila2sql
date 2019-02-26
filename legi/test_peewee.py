from contextlib import contextmanager
import os
from models import db_proxy, DBMeta, DuplicateFile
from playhouse.db_url import connect


address = "./KALI.sqlite"
db = connect("postgresql://legipy:dilamite@localhost/kali")
db_proxy.initialize(db)

res3 = db.execute_sql("delete from db_meta where value='yolo';")
db.commit()

# res1 = DBMeta.create(key='test1', value="yolo")
# print("res1 is %s" % res1)
# res2 = DBMeta.create(key='test2', value="yolo")
# print("res2 is %s" % res2)
# res3 = db.execute_sql("delete from db_meta where value='yolo';")
# print("res3 is %s" % res3)
# res4 = db.commit()
# print("res4 is %s" % res4)

df = len(DuplicateFile.select() \
    .where(DuplicateFile.id == 'KALIARTI000026951576a') \
    .order_by(DuplicateFile.mtime.desc()) \
    .limit(1) \
    .dicts())

print(df)

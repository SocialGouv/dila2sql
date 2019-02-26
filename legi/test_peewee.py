from peewee import SqliteDatabase
from contextlib import contextmanager
import os

IGNORE = object()
NIL = object()
ROOT = os.path.dirname(__file__) + '/'

class DB(SqliteDatabase):
    pass

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

address = "./KALI.sqlite"
db = DB(address)
db.address = address

# class DBMeta(Model):
#     table_name = CharField()
#     value = CharField()
#     key = CharField()

#     class Meta:
#         database = db # This model uses the "people.db" database.


# cursor = db.execute_sql("SELECT value FROM db_meta WHERE key = 'schema_version'")
# row = cursor.fetchone()
# v = row[0] if row is not None else 0

res = db.execute_sql("select * from db_meta;").fetchone()

def iter_results(q):
    while True:
        r = q.fetchmany()
        if not r:
            return
        for row in r:
            yield row

@contextmanager
def patch_object(obj, attr, value):
    if value is IGNORE:
        yield
        return
    backup = getattr(obj, attr, NIL)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        if backup is NIL:
            delattr(obj, attr)
        else:
            setattr(obj, attr, backup)

def get_all(*a, **kw):
    to_dict = kw.get('to_dict', False)
    with patch_object(db, 'row_factory', dict_factory if to_dict else IGNORE):
        q = db.execute_sql(*a)
    return iter_results(q)

versions = get_all("""
    SELECT cid, id
        FROM textes_versions
        WHERE nature = 'accord'
    ORDER BY date_debut ASC
""", to_dict=True)

for v in versions:
    print("bonjour %s" % (v, ))

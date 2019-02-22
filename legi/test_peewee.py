from peewee import SqliteDatabase

class DB(SqliteDatabase):
    pass

db = DB("../legi-postgres/tarballs3/KALI.sqlite")
db.address ="../legi-postgres/tarballs3/KALI.sqlite"
# class DBMeta(Model):
#     table_name = CharField()
#     value = CharField()
#     key = CharField()

#     class Meta:
#         database = db # This model uses the "people.db" database.


cursor = db.execute_sql("SELECT value FROM db_meta WHERE key = 'schema_version'")
row = cursor.fetchone()
v = row[0] if row is not None else 0

db.cursor().execute_sql("select 1; select 1; select 1;")

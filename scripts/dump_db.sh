if [ -z "$1" ]
  then
    echo "You need to pass the db name (kali, legi ...)"
fi

dbname=$1
dumpdir=/var/lib/dila2sql/generated_dumps/`date +"%Y-%m-%d"`
mkdir -p $dumpdir
echo "running pg_dump -U ${POSTGRES_USER} -f $dumpdir/$dbname.sql $dbname ..."
pg_dump -U ${POSTGRES_USER} -f $dumpdir/$dbname.sql $dbname
echo "done!"

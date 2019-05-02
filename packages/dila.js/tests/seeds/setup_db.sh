DB_NAME=dila2sql_test
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
createdb $DB_NAME
psql $DB_NAME -c "DROP SCHEMA public CASCADE;"
psql $DB_NAME -c "CREATE SCHEMA public;"
psql -d $DB_NAME -f tests/seeds/schema.sql
psql -d $DB_NAME -c "COPY sommaires FROM '$DIR/sommaires.csv'"
psql -d $DB_NAME -c "COPY sections FROM '$DIR/sections.csv'"
psql -d $DB_NAME -c "COPY articles FROM '$DIR/articles.csv'"
psql -d $DB_NAME -c "COPY textes_versions FROM '$DIR/textes_versions.csv'"
echo "$DB_NAME db seeded."

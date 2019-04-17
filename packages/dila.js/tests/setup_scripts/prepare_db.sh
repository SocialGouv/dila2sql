# TEST_DB_URL=postgresql://localhost/dila2sql_test prepare_db.sh
if [ -z "$TEST_DB_URL" ]; then echo "no TEST_DB_URL env var set" && exit 1; fi
psql $TEST_DB_URL -c "DROP SCHEMA public CASCADE;"
psql $TEST_DB_URL -c "CREATE SCHEMA public;"
psql -d $TEST_DB_URL -f schema.sql
psql -d $TEST_DB_URL -c "COPY sommaires FROM '$PWD/sommaires.csv'"
psql -d $TEST_DB_URL -c "COPY sections FROM '$PWD/sections.csv'"
psql -d $TEST_DB_URL -c "COPY articles FROM '$PWD/articles.csv'"
psql -d $TEST_DB_URL -c "COPY textes_versions FROM '$PWD/textes_versions.csv'"
echo "done"

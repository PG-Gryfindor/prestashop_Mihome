docker exec -i $1 rm -rf /var/www/html/install
docker exec -i $1 mv /var/www/html/admin /var/www/html/Admin
#gunzip -c db-dump/dump.sql.gz > tmp/dump.sql
#cat tmp/db-dump.sql | docker exec -i $2 psql postgresql://postgres:student@127.0.0.1:5432/$3?sslmode=require
docker exec -i $2 bash -l -c "gunzip -c /dump/dump.sql.gz > /tmp/dump.sql && mysql -h127.0.0.1 -uroot -pAlohomora prestashopMI < /tmp/dump.sql"
#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift

until PGPASSWORD="admin" psql -h "$host" -d "postgres" -U "postgres" -c '\q';

do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 3

done

  >&2 echo "Postgres is up - executing command"

exec "$@"
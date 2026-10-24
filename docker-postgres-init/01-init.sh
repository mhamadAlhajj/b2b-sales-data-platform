#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -v reader_user="$READER_USER" \
  -v reader_password="$READER_PASSWORD" \
  -v db_name="$POSTGRES_DB" \
  -v postgres_user="$POSTGRES_USER" <<'EOSQL'

CREATE ROLE :"reader_user" LOGIN PASSWORD :'reader_password';

REVOKE ALL ON DATABASE :"db_name" FROM PUBLIC;
GRANT CONNECT ON DATABASE :"db_name" TO :"reader_user";

ALTER DATABASE :"db_name" SET default_transaction_read_only = on;


ALTER DEFAULT PRIVILEGES FOR ROLE :"postgres_user"
  GRANT SELECT ON TABLES TO :"reader_user";

EOSQL
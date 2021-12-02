#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS $POSTGRES_SCHEMA AUTHORIZATION $POSTGRES_USER;
    CREATE TABLE $POSTGRES_SCHEMA._dataemon (
        inserted_on TIMESTAMP DEFAULT NOW(),
        package_url TEXT,
        package_version TEXT
    );
EOSQL

while true
do
    echo Download package dependencies
    dbt deps --profiles-dir .dbt
    echo Run models
    dbt run --profiles-dir .dbt
    sleep 5s
done

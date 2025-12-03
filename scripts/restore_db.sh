#!/bin/bash
set -e

if [ -f "database_dump.sql" ]; then
    PGPASSWORD=31415926535 psql \
    -h localhost \
    -U admin \
    -d test_sync_db \
    -f database_dump.sql \
    2>&1 | tee restore.log
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
    PGPASSWORD=31415926535 psql -h localhost -U admin -d test_sync_db -c \
        "\dt"
    else
    cat restore.log
    exit 1
    fi
else
    PGPASSWORD=31415926535 psql -h localhost -U admin -d test_sync_db -c "
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    );
    "
fi
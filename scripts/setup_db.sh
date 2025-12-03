#!/bin/bash
set -e
echo "Setting up database"
echo "Creating user 'admin'"
PGPASSWORD=postgres psql -q -h localhost -U postgres -c "CREATE USER admin WITH PASSWORD '31415926535';"
echo "Creating database 'test_sync_db'"
PGPASSWORD=postgres psql -q -h localhost -U postgres -c "CREATE DATABASE test_sync_db;"
echo "Granting 'admin' privileges to 'test_sync_db'"
PGPASSWORD=postgres psql -q -h localhost -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE test_sync_db TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -d test_sync_db -c "GRANT ALL ON SCHEMA public TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -d test_sync_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -d test_sync_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -d test_sync_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -d test_sync_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO admin;"
PGPASSWORD=postgres psql -q -h localhost -U postgres -c "\l" | grep test_sync_db
PGPASSWORD=postgres psql -q -h localhost -U postgres -c "\du" | grep admin
echo "Database created successfully."
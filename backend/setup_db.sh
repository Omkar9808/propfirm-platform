#!/bin/bash
# Setup PostgreSQL database for Prop Firm Platform

# Create database and user
psql -U postgres -c "CREATE USER propfirm_user WITH PASSWORD 'propfirm_password';"
psql -U postgres -c "CREATE DATABASE propfirm_db OWNER propfirm_user;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE propfirm_db TO propfirm_user;"

echo "Database setup complete!"
echo "Database: propfirm_db"
echo "User: propfirm_user"
echo "Password: propfirm_password"
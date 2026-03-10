@echo off
REM Setup PostgreSQL database for Prop Firm Platform on Windows

echo Setting up PostgreSQL database...

REM You'll need to run these commands manually in psql or pgAdmin:
echo.
echo Run these commands in PostgreSQL:
echo CREATE USER propfirm_user WITH PASSWORD 'propfirm_password';
echo CREATE DATABASE propfirm_db OWNER propfirm_user;
echo GRANT ALL PRIVILEGES ON DATABASE propfirm_db TO propfirm_user;
echo.
echo Or use pgAdmin to create:
echo - Database: propfirm_db
echo - User: propfirm_user
echo - Password: propfirm_password
echo.
pause
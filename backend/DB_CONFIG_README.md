# Database Configuration for Supabase Connection Pooler

## Configuration Steps

To connect to your Supabase database using the connection pooler:

1. **Update your `.env` file** with your actual Supabase connection details:

```
# Environment Configuration - Supabase with Connection Pooler
POSTGRES_SERVER=your-project-id.supabase.co
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_DB=your_database_name
POSTGRES_PORT=6543  # Connection pooler port

# Note: When using special characters in password, they must be URL-encoded
# For example: @ becomes %40, # becomes %23, etc.

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

2. **Install dependencies** (if not already installed):

```bash
pip install -r requirements.txt
```

3. **Run database migrations**:

```bash
# Using PowerShell
cd backend
python -m alembic upgrade head

# Or using Command Prompt
cd backend && python -m alembic upgrade head
```

## Connection String Format

The application is configured to use:
- Driver: `postgresql+psycopg2://`
- SSL Mode: `require`
- Port: `6543` (transaction pooler)
- URL encoding for passwords with special characters

## Database Configuration Details

- **Pool Pre-ping**: Enabled to ensure connections are alive
- **Pool Size**: 5 connections
- **Max Overflow**: 10 additional connections
- **Pool Recycle**: Every 300 seconds
- **SSL Mode**: Require (for security)

## Troubleshooting

If you encounter connection issues:
1. Verify your Supabase project ID, username, and password
2. Ensure your IP is whitelisted in Supabase settings
3. Confirm you're using the connection pooler port (6543) not the direct port (5432)
4. Check that special characters in passwords are URL-encoded

## Verification

After running the migrations, check your Supabase dashboard to confirm that the tables have been created successfully.
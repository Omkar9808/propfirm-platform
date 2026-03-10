# Prop Firm Practice Platform - Backend

FastAPI backend for the Prop Firm Practice Platform with PostgreSQL database.

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

## Project Structure

```
backend/
├── app/
│   ├── api/v1/routes/     # API route handlers
│   ├── core/              # Core configuration
│   ├── db/                # Database configuration and models
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── main.py           # FastAPI app entry point
├── migrations/            # Alembic migrations
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL Database

#### Option A: Using setup script (Linux/Mac)
```bash
chmod +x setup_db.sh
./setup_db.sh
```

#### Option B: Manual setup
Create a PostgreSQL database and user:
```sql
CREATE USER propfirm_user WITH PASSWORD 'propfirm_password';
CREATE DATABASE propfirm_db OWNER propfirm_user;
GRANT ALL PRIVILEGES ON DATABASE propfirm_db TO propfirm_user;
```

#### Option C: Using pgAdmin
1. Open pgAdmin
2. Create a new database named `propfirm_db`
3. Create a new user named `propfirm_user` with password `propfirm_password`
4. Grant all privileges to the user

### 3. Configure Environment Variables

Edit the `.env` file:
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=propfirm_user
POSTGRES_PASSWORD=propfirm_password
POSTGRES_DB=propfirm_db
POSTGRES_PORT=5432

SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Initialize Database

```bash
python init_db.py
```

This will:
- Create database tables
- Initialize default roles (super_admin, admin, trader, guest)
- Create default admin user (admin@propfirm.com / Admin123!)

### 5. Run the Application

```bash
python run.py
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/` - Get all users (authenticated users only)

## Default Admin Credentials

Email: `admin@propfirm.com`
Password: `Admin123!`

⚠️ **Important**: Change the admin password in production!

## Development Commands

### Run with auto-reload
```bash
python run.py
```

### Create database migration
```bash
alembic revision --autogenerate -m "Migration description"
```

### Run migrations
```bash
alembic upgrade head
```

### Downgrade migration
```bash
alembic downgrade -1
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Login audit logging
- IP address tracking
- Account status management

## Testing

### Test Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Test Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| POSTGRES_SERVER | Database server | localhost |
| POSTGRES_USER | Database user | propfirm_user |
| POSTGRES_PASSWORD | Database password | propfirm_password |
| POSTGRES_DB | Database name | propfirm_db |
| POSTGRES_PORT | Database port | 5432 |
| SECRET_KEY | JWT secret key | (required) |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration | 30 |

## Production Considerations

1. Change `SECRET_KEY` to a strong random value
2. Use environment variables for all secrets
3. Set up proper logging
4. Configure HTTPS
5. Set up database backups
6. Implement rate limiting
7. Add monitoring and alerting
8. Use a production WSGI server (Gunicorn)
9. Set `DEBUG=False` in production
10. Use connection pooling for database

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists and user has permissions

### Migration Issues
- Check that all models are imported in `app/models/__init__.py`
- Ensure database URL is correct in `alembic.ini`

### Authentication Issues
- Verify JWT secret key is set
- Check token expiration settings
- Ensure user exists and is active
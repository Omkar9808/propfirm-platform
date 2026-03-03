# Development Environment Setup

## Local Development Only

### Starting the Application

1. **Backend Server**:
   ```bash
   cd backend
   python run.py
   ```
   Access at: http://localhost:8000

2. **Frontend Server**:
   ```bash
   cd Propfirm/website
   npm start
   ```
   Access at: http://localhost:3000

3. **Database Setup**:
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Initialize database
   python init_database.py
   ```

### Security Features Enabled

-✅ JWT Authentication
-✅ Password Hashing (Argon2)
-✅ Role-Based Access Control
- ✅ Input Validation
- ✅ Database Security
- ✅ HTTPS for Public Access (when needed)

### Local Access Points

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Main Website**: http://localhost:3000
- **Admin Panel**: http://localhost:3000/admin

### Admin Credentials
- **Email**: admin@propfirm.com
- **Password**: Admin123

### Development Guidelines

1. Always run locally first
2. Test all features in development
3. Use proper authentication
4. Never expose development servers publicly
5. Keep environment variables secure
# PropFirm Platform - Complete Project Structure

## 📁 Root Directory: `Propfirm/`

```
Propfirm/
├── .gitignore
├── SECURITY.md
├── DEVELOPMENT.md
├── *.md (Documentation files)
│
├── backend/                      # Python FastAPI Backend
├── vercel-frontend/              # Vercel Frontend (Node.js/Next.js)
└── Propfirm/website/             # Additional website files
```

---

## 🐍 BACKEND STRUCTURE: `backend/`

### Backend Root Files
```
backend/
├── .env                          # Environment variables
├── .gitignore
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
├── alembic.ini                   # Database migration config
├── init_database.py              # Database initialization
├── init_db.py                    # Alternative DB init
├── setup_db.bat                  # Windows DB setup script
├── setup_db.sh                   # Linux/Mac DB setup script
├── test_backend.py               # Backend tests
├── test_imports.py               # Import verification
├── verify_phase5.py              # Phase 5 verification
├── verify_phase6.py              # Phase 6 verification
│
├── Documentation Files:
├── ARCHITECTURE.md
├── CONSOLIDATION_SUMMARY.md
├── DATABASE_MAP.md
├── DB_CONFIG_README.md
├── FRAUD_DETECTION.md
├── MONETIZATION.md
├── PHASE1_SUMMARY.md
├── PHASE2_SUMMARY.md
├── PHASE3_SUMMARY.md
├── PHASE4_SUMMARY.md
├── PHASE5_SUMMARY.md
├── PHASE6_SUMMARY.md
├── README.md
├── RISK_ENGINE.md
├── SYSTEM_FLOW.md
│
├── migrations/                   # Alembic database migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── [migration_files].py
│
└── app/                          # Main application package
```

### Backend App Package: `backend/app/`

```
app/
├── __init__.py
├── main.py                       # FastAPI application instance
│
├── api/                          # API layer
│   ├── deps.py                   # Dependencies
│   └── v1/
│       ├── endpoints/
│       │   └── [api_endpoints].py
│       └── api.py
│
├── core/                         # Core utilities
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── logger.py                 # Logging setup
│   └── security.py               # Security utilities
│
├── db/                           # Database layer
│   ├── base.py                   # SQLAlchemy base
│   ├── init_db.py                # DB initialization
│   ├── models.py                 # SQLAlchemy models
│   └── seed.py                   # Database seeding
│
├── domains/                      # Domain-driven design modules
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── analytics_engine.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   ├── challenge/
│   │   ├── __init__.py
│   │   ├── challenge_manager.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   ├── finance/
│   │   ├── __init__.py
│   │   ├── finance_core.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   ├── identity/
│   │   ├── __init__.py
│   │   ├── identity_service.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   ├── notification/
│   │   ├── __init__.py
│   │   ├── notification_engine.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── risk_engine.py
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   │
│   └── trading/
│       ├── __init__.py
│       ├── trading_engine.py
│       ├── services/
│       ├── repositories/
│       └── schemas/
│
├── models/                       # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py                   # User model
│   ├── role.py                   # Role model
│   ├── audit.py                  # Audit log model
│   ├── certificate.py            # Certificate model
│   ├── monetization.py           # Monetization model
│   ├── payout.py                 # Payout model
│   ├── phase2/                   # Phase 2 specific models
│   │   └── [models].py
│   ├── phase3/                   # Phase 3 specific models
│   │   └── [models].py
│   ├── phase4/                   # Phase 4 specific models
│   │   └── [models].py
│   ├── phase5/                   # Phase 5 specific models
│   │   └── [models].py
│   └── phase6/                   # Phase 6 specific models
│       └── [models].py
│
├── repositories/                 # Data access layer
│   ├── __init__.py
│   ├── user.py
│   ├── role.py
│   ├── audit.py
│   ├── phase2.py
│   ├── phase3.py
│   ├── phase4.py
│   └── [entity].py
│
├── routes/                       # HTTP routes
│   ├── __init__.py
│   ├── certificate.py
│   ├── challenge_tier.py
│   ├── enhanced_metrics.py
│   ├── monetization.py
│   ├── monetization_dashboard.py
│   └── payout.py
│
├── schemas/                      # Pydantic schemas
│   ├── __init__.py
│   ├── auth.py
│   ├── certificate.py
│   ├── challenge_tier.py
│   ├── monetization.py
│   ├── payout.py
│   ├── phase2.py
│   ├── phase3.py
│   ├── phase4.py
│   ├── phase5.py
│   └── phase6.py
│
├── services/                     # Business logic layer
│   └── [service_modules].py     # Various service files
│
└── utils/                        # Utility functions
    ├── [utilities].py
    └── [helpers].py
```

---

## ⚛️ VERCEL FRONTEND: `vercel-frontend/`

### Frontend Root Files
```
vercel-frontend/
├── .env.local                    # Environment variables (local)
├── .gitignore
├── package.json                  # NPM dependencies
├── package-lock.json             # Locked dependency versions
├── server.js                     # Custom server
├── app.js                        # Application entry
├── vercel.json                   # Vercel configuration
├── README.md
│
├── lib/                          # Shared libraries
│   ├── supabase.js               # Supabase client
│   └── [utils].js
│
├── components/                   # React components
│   └── Leaderboard.jsx           # Leaderboard component
│
├── app/                          # Next.js App Router
│   └── leaderboard/
│       └── page.jsx              # Leaderboard page route
│
├── api/                          # API routes (serverless)
│   ├── auth.js
│   ├── challenge.js
│   ├── dashboard.js
│   ├── index.js
│   └── risk.js
│
├── public/                       # Static assets
│   ├── css/
│   │   └── style.css             # Global styles
│   ├── images/
│   │   └── [image_files]
│   └── js/
│       └── main.js               # Client-side JavaScript
│
└── views/                        # HTML view templates
    ├── index.html                # Homepage
    ├── checkout.html             # Checkout page
    ├── pricing.html              # Pricing page
    ├── rules.html                # Rules page
    ├── leaderboard.html          # Leaderboard page (static HTML)
    │
    ├── admin/                    # Admin dashboard views
    │   ├── index.html
    │   ├── login.html
    │   ├── overview.html
    │   ├── accounts.html
    │   ├── analytics.html
    │   ├── challenges.html
    │   ├── payments.html
    │   ├── risk-monitor.html
    │   ├── settings.html
    │   ├── users.html
    │   └── violations.html
    │
    ├── auth/                     # Authentication views
    │   ├── login.html
    │   └── register.html
    │
    └── dashboard/                # User dashboard views
        ├── index.html
        ├── accounts.html
        ├── account-detail.html
        ├── buy.html
        ├── certificates.html
        ├── affiliate.html
        └── settings.html
```

---

## 🌐 ADDITIONAL WEBSITE: `Propfirm/website/`

```
Propfirm/website/
├── public/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   └── js/
│       └── main.js
│
├── views/
│   ├── admin/
│   │   ├── accounts.html
│   │   ├── analytics.html
│   │   ├── challenges.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── overview.html
│   │   ├── payments.html
│   │   ├── risk-monitor.html
│   │   ├── settings.html
│   │   ├── users.html
│   │   └── violations.html
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── dashboard/
│   │   ├── account-detail.html
│   │   ├── accounts.html
│   │   ├── affiliate.html
│   │   ├── buy.html
│   │   ├── certificates.html
│   │   ├── index.html
│   │   └── settings.html
│   │
│   ├── checkout.html
│   ├── index.html
│   ├── leaderboard.html
│   ├── pricing.html
│   └── rules.html
│
├── package.json
└── package-lock.json
```

---

## 📦 KEY TECHNOLOGIES

### Backend Stack
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (via SQLAlchemy)
- **Migrations:** Alembic
- **Authentication:** JWT-based
- **Architecture:** Domain-Driven Design (DDD)

### Frontend Stack (Vercel)
- **Framework:** Next.js / Node.js
- **Styling:** TailwindCSS + Custom CSS
- **State:** React (for components)
- **Deployment:** Vercel
- **Database Client:** Supabase

### Additional Tools
- **Version Control:** Git
- **Package Manager:** npm (Node), pip (Python)
- **Testing:** pytest (Backend)

---

## 🔑 IMPORTANT FILES EXPLANATION

### Configuration Files
- `backend/.env` - Backend environment variables (DB credentials, API keys)
- `vercel-frontend/.env.local` - Frontend environment variables (Supabase URL/Key)
- `vercel.json` - Vercel deployment configuration
- `alembic.ini` - Database migration configuration

### Entry Points
- `backend/run.py` - Backend server entry point
- `vercel-frontend/server.js` - Frontend server
- `vercel-frontend/app.js` - Frontend application logic

### Key Documentation
- `backend/ARCHITECTURE.md` - System architecture overview
- `backend/DATABASE_MAP.md` - Database schema documentation
- `backend/SYSTEM_FLOW.md` - System flow diagrams
- `backend/RISK_ENGINE.md` - Risk engine documentation
- `backend/FRAUD_DETECTION.md` - Fraud detection system

### Critical Components
- `vercel-frontend/components/Leaderboard.jsx` - React leaderboard component
- `vercel-frontend/lib/supabase.js` - Supabase database client
- `vercel-frontend/public/views/leaderboard.html` - Static HTML leaderboard (production)

---

## 📊 PROJECT STATISTICS

**Total Major Directories:** 3 root folders
- `backend/` - Python FastAPI backend (~50+ Python files)
- `vercel-frontend/` - Vercel/Next.js frontend (~20+ JS/JSX files)
- `Propfirm/website/` - Additional website files

**Backend Domains:** 7 domain modules
- Analytics, Challenge, Finance, Identity, Notification, Risk, Trading

**Frontend Pages:** 20+ HTML pages
- Public pages, Admin dashboard, User dashboard, Auth pages

**Database Models:** 10+ core models
- User, Role, Audit, Certificate, Monetization, Payout, Phase-specific models

---

## 🚀 DEPLOYMENT STRUCTURE

### Vercel Deployment
All files in `vercel-frontend/` are deployed to Vercel:
- Serverless functions via `/api` routes
- Static pages via `/views` directory
- React components rendered client-side
- Assets served from `/public`

### Backend Deployment
The `backend/` folder can be deployed to:
- VPS (Virtual Private Server)
- Cloud platforms (AWS, GCP, Azure)
- Container orchestration (Docker/Kubernetes)

---

## 📝 NOTES

1. **Dual Frontend Strategy:**
   - Static HTML (`/views`) for production
   - React components (`/components`) for dynamic features

2. **Database Integration:**
   - Backend uses SQLAlchemy (PostgreSQL)
   - Frontend uses Supabase (real-time features)

3. **Phase Development:**
   - Backend organized by development phases (PHASE1-6)
   - Each phase has dedicated models and schemas

4. **Domain-Driven Design:**
   - Backend follows DDD principles
   - Clear separation of concerns per business domain

---

*Last Updated: March 3, 2026*

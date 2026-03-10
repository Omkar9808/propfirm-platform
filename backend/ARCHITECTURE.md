# Prop Firm Practice Platform - Architecture Documentation

##🚀 Production Architecture Overview

**Project**: Prop Firm Practice Platform  
**Backend**: FastAPI + PostgreSQL (Supabase)  
**Status**: Production-ready, domain-based architecture  

This document provides the complete architectural blueprint for the production system, organized by business domains rather than development phases.

---

##🧠 Domain-Based Architecture Structure

The system is organized into 7 core business domains, each representing a distinct functional area:

### 1️⃣ Identity Domain
**Purpose**: User management, authentication, and access control

**Models**:
- `roles` - User role definitions and permissions
- `users` - User account information and credentials
- `user_settings` - User preference configurations
- `login_audit_log` - Authentication and access logging

**Services**:
- `AuthService` - JWT authentication and token management
- `UserService` - User lifecycle and profile management

**Routes**:
- `/auth/*` - Authentication endpoints (login, register, token refresh)
- `/users/*` - User profile and management endpoints

---

### 2️⃣ Challenge Domain
**Purpose**: Challenge offerings, rule management, and account provisioning

**Models**:
- `challenges` - Available trading challenges and pricing
- `challenge_rule_versions` - Challenge rule definitions and versioning
- `account_rule_snapshots` - Point-in-time rule captures for accounts

**Services**:
- `ChallengeService` - Challenge management and rule versioning
- `AccountService` - Trading account provisioning and lifecycle
- `PaymentService` - Payment processing and transaction management

**Routes**:
- `/challenges/*` - Challenge browsing and purchase
- `/accounts/*` - Account creation and management
- `/payments/*` - Payment processing and transaction history

---

### 3️⃣ Trading Domain
**Purpose**: Trade execution, data management, and platform connectivity

**Models**:
- `accounts` - Trading account metadata and status
- `trades` - Individual trade records and execution details
- `daily_stats` - Aggregated daily performance metrics
- `equity_snapshots` - Point-in-time account equity data
- `mt5_sync_log` - MT5 platform synchronization records
- `mt5_accounts` - MT5 account linking and credentials
- `mt5_trades` - MT5-specific trade data synchronization
- `mt5_servers` - MT5 server connection configurations

**Services**:
- `AccountService` - Account lifecycle management
- `TradeService` - Trade processing and validation
- `MT5Service` - MT5 platform integration and synchronization

**Routes**:
- `/accounts/*` - Account information and status
- `/trades/*` - Trade data import and management
- `/mt5/*` - MT5 connectivity and synchronization

---

### 4️⃣ Risk Domain
**Purpose**: Risk monitoring, violation detection, and automated evaluation

**Models**:
- `violations` - Risk rule violations and breaches
- `account_status_history` - Account status change tracking
- `job_execution_log` - Automated risk evaluation job logs

**Services**:
- `RiskEngineService` - Automated risk calculation and evaluation
- `ViolationService` - Violation detection and resolution management

**Routes**:
- `/risk/*` - Risk evaluation and monitoring
- `/violations/*` - Violation management and resolution
- `/admin/risk/*` - Administrative risk controls

---

### 5️⃣ Financial Domain
**Purpose**: Payment processing, revenue tracking, and financial operations

**Models**:
- `payments` - Customer payment transactions
- `revenue_ledger` - Financial transaction ledger and accounting
- `affiliate_commissions` - Affiliate referral tracking and payouts

**Services**:
- `PaymentService` - Payment processing and transaction management
- `RevenueService` - Revenue tracking and financial reporting

**Routes**:
- `/payments/*` - Payment processing and transaction history
- `/admin/finance/*` - Financial reporting and revenue management

---

### 6️⃣ Analytics Domain
**Purpose**: Performance analytics, trader metrics, and platform insights

**Models**:
- `trader_metrics` - Comprehensive trader performance analytics
- `leaderboard_cache` - Cached ranking and performance leaderboards
- `platform_metrics` - System-wide platform performance metrics

**Services**:
- `AnalyticsService` - Performance analytics and metric calculation
- `LeaderboardService` - Leaderboard generation and caching

**Routes**:
- `/analytics/*` - Performance analytics and metrics
- `/leaderboard/*` - Trader rankings and performance boards

---

### 7️⃣ Notification Domain
**Purpose**: Communication system and user notifications

**Models**:
- `notifications` - User notification records and delivery
- `notification_templates` - Notification content templates
- `email_queue` - Email delivery queue and scheduling
- `user_notification_settings` - User communication preferences

**Services**:
- `NotificationService` - Notification delivery and management
- `EmailService` - Email delivery and queue management

**Routes**:
- `/notifications/*` - Notification management and delivery
- `/admin/notifications/*` - Notification system administration

---

##🔗 Integration Patterns

### Core Integration Flows:
1. **User Journey**: Identity → Challenge → Trading → Risk → Analytics
2. **Financial Flow**: Payment → Account Creation → Trade Processing → Revenue Tracking
3. **Risk Management**: Trade Processing → Risk Evaluation → Violation Handling → Status Changes
4. **Notification System**: All domains → Notification triggers → Multi-channel delivery

### Data Flow Architecture:
- **Read Operations**: Each domain manages its own data with proper service isolation
- **Write Operations**: Follow strict transactional boundaries with history and ledger requirements
- **Cross-Domain Communication**: Event-based triggers with loose coupling

---

##🏗️ Technical Architecture Principles

### Data Integrity Rules (Non-Negotiable):
-✅ No status change without corresponding history record
- ✅ No financial mutation without ledger entry
- ✅ No rule changes affecting existing accounts
- ✅ No duplicate trades possible
- ✅ All monetary values use decimal precision
- ✅ All timestamps stored in UTC

### System Design Principles:
- **Domain Isolation**: Clear separation of concerns between business domains
- **Service Layer**: Business logic isolated in dedicated service classes
- **Repository Pattern**: Data access abstraction for clean architecture
- **Role-Based Access**: Proper authorization throughout the system
- **Audit Trail**: Comprehensive logging for all operations
- **RESTful Design**: Standardized API responses and error handling

---

##🔧 Configuration

### Infrastructure:
- **Database**: PostgreSQL (Supabase) with connection pooler
- **Framework**: FastAPI with Uvicorn ASGI server
- **ORM**: SQLAlchemy 2.0 with Alembic migrations
- **Authentication**: JWT with bcrypt password hashing
- **Connection Pooling**: 
  - `pool_pre_ping=True`
  - `pool_size=5`
  - `max_overflow=10`
  - `sslmode=require`

### Deployment Configuration:
- **Environment Variables**: Secure credential management via .env
- **Database URLs**: Properly formatted connection strings with SSL
- **API Versioning**: `/api/v1/` prefix for stable endpoints
- **Health Monitoring**: Built-in health check endpoints

---

##📊 Readiness Checklist

###✅ Completed Architecture Elements:
- [x] Domain-based folder structure
- [x] Clean API route organization
- [x] Comprehensive service layer separation
- [x] Proper data access abstraction
- [x] Role-based access control implementation
- [x] Audit trail and history tracking
- [x] Financial ledger integrity
- [x] Risk engine isolation
- [x] Notification system integration
- [x] Analytics and reporting capabilities

###📚 Completeness:
- [x] This architecture document
- [x] Database mapping documentation
- [x] System flow documentation
- [x] API endpoint documentation
- [x] Business process documentation

---

## 🎯 Future Scalability Considerations

### Horizontal Scaling:
- **Database**: Connection pooling and read replicas
- **Services**: Stateless service design for horizontal scaling
- **Caching**: Redis integration for performance optimization
- **Load Balancing**: Multiple application instances behind load balancer

### Domain Evolution:
- **Microservices**: Potential future separation of domains into independent services
- **Event Sourcing**: Possible future implementation for audit trail enhancement
- **CQRS**: Read/write model separation for complex analytics

This architecture provides a solid foundation for the Prop Firm Practice Platform as a production-ready, domain-based system that can scale with business growth while maintaining data integrity and operational excellence.
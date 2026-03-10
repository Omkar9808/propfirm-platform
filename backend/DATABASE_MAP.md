# Prop Firm Practice Platform - Database Mapping

##📋 Comprehensive Table Documentation

**Database**: PostgreSQL (Supabase)  
**Connection**: Transaction Pooler (port 6543)  
**Status**: Production-ready with complete schema mapping

This document provides detailed mapping of all database tables, their relationships, and usage across the 7 business domains.

---

##🔑 Core Identity Domain Tables

### `roles`
**Purpose**: User role definitions and permission levels  
**Domain**: Identity  
**Primary Key**: `id` (UUID)  
**Key Fields**: `name`, `permissions`, `description`  
**Services Using**: AuthService, UserService  
**Key Relationships**: 
- Foreign key in `users` table
- One-to-many relationship with users

**Example Records**:
- `super_admin` - Full system access
- `admin` - Administrative functions
- `trader` - Standard user access
- `affiliate` - Partner/referral access

---

### `users`
**Purpose**: User account information and credentials  
**Domain**: Identity  
**Primary Key**: `id` (UUID)  
**Key Fields**: `username`, `email`, `password_hash`, `role_id`, `is_active`  
**Services Using**: AuthService, UserService, AuditService  
**Key Relationships**:
- Foreign key to `roles.id`
- One-to-many relationships with payments, accounts, notifications
- Referenced by login_audit_log, violations, account_status_history

---

### `user_settings`
**Purpose**: User preference configurations and notification settings  
**Domain**: Identity  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `timezone`, `notification_preferences`, `ui_preferences`  
**Services Using**: UserService, NotificationService  
**Key Relationships**: 
- Foreign key to `users.id` (one-to-one)

---

### `login_audit_log`
**Purpose**: Authentication and access logging for security monitoring  
**Domain**: Identity  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `ip_address`, `user_agent`, `login_success`, `attempt_time`  
**Services Using**: AuthService, AuditService  
**Key Relationships**: 
- Foreign key to `users.id`

---

##🎯 Challenge Domain Tables

### `challenges`
**Purpose**: Available trading challenges and pricing information  
**Domain**: Challenge  
**Primary Key**: `id` (UUID)  
**Key Fields**: `name`, `description`, `price`, `is_featured`, `sort_order`  
**Services Using**: ChallengeService, PaymentService, AccountService  
**Key Relationships**: 
- Referenced by `payments.challenge_id`
- One-to-many relationship with challenge_rule_versions

---

### `challenge_rule_versions`
**Purpose**: Challenge rule definitions with versioning and historical tracking  
**Domain**: Challenge  
**Primary Key**: `id` (UUID)  
**Key Fields**: `challenge_id`, `version`, `max_daily_loss`, `max_total_loss`, `profit_target`, `max_positions`, `max_lot_size`  
**Services Using**: ChallengeService, RiskEngineService  
**Key Relationships**: 
- Foreign key to `challenges.id`
- Referenced by `account_rule_snapshots.rule_version_id`

---

### `account_rule_snapshots`
**Purpose**: Point-in-time rule captures for trading accounts (immutable rules)  
**Domain**: Challenge  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `rule_version_id`, `snapshot_date`, `max_daily_loss`, `max_total_loss`, `profit_target`  
**Services Using**: AccountService, RiskEngineService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Foreign key to `challenge_rule_versions.id`

---

### `payments`
**Purpose**: Customer payment transactions and purchase history  
**Domain**: Financial  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `challenge_id`, `amount`, `currency`, `payment_method`, `status`, `transaction_id`  
**Services Using**: PaymentService, RevenueService  
**Key Relationships**: 
- Foreign keys to `users.id` and `challenges.id`
- One-to-one relationship with `accounts.payment_id`
- Referenced by `revenue_ledger.payment_id`

---

### `revenue_ledger`
**Purpose**: Financial transaction ledger and accounting records  
**Domain**: Financial  
**Primary Key**: `id` (UUID)  
**Key Fields**: `payment_id`, `amount`, `currency`, `revenue_type`, `transaction_type`, `balance_after`  
**Services Using**: PaymentService, RevenueService, AccountService  
**Key Relationships**: 
- Foreign key to `payments.id`
- Foreign key to `users.id` (for user_id)
- Foreign key to `accounts.id` (for account_id)

---

##📈 Trading Domain Tables

### `accounts`
**Purpose**: Trading account metadata, status, and lifecycle management  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `payment_id`, `account_number`, `name`, `starting_balance`, `status`, `created_at`, `activated_at`  
**Services Using**: AccountService, TradeService, RiskEngineService  
**Key Relationships**: 
- Foreign keys to `users.id` and `payments.id`
- One-to-many relationships with trades, daily_stats, violations, mt5_accounts
- Referenced by account_rule_snapshots, equity_snapshots

---

### `trades`
**Purpose**: Individual trade records and execution details  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `ticket_id`, `symbol`, `order_type`, `volume`, `open_price`, `close_price`, `profit`, `status`, `open_time`, `close_time`  
**Services Using**: TradeService, RiskEngineService, AnalyticsService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Unique constraint on `account_id, ticket_id` (prevents duplicates)
- Referenced by `mt5_trades.platform_trade_id`
- Referenced by `violations.trade_id`

---

### `daily_stats`
**Purpose**: Aggregated daily performance metrics and risk calculations  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `stat_date`, `starting_balance`, `ending_balance`, `daily_pnl`, `trade_count`, `max_drawdown`  
**Services Using**: TradeService, RiskEngineService, AnalyticsService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Unique index on `account_id, stat_date`
- Daily aggregation of trade data

---

### `equity_snapshots`
**Purpose**: Point-in-time account equity and balance data  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `timestamp`, `balance`, `equity`, `margin`, `free_margin`, `margin_level`  
**Services Using**: TradeService, MT5Service, AnalyticsService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Indexed by `account_id, timestamp` for time-series queries

---

### `mt5_sync_log`
**Purpose**: MT5 platform synchronization records and error tracking  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `sync_type`, `status`, `record_count`, `error_message`, `sync_duration_ms`, `sync_started_at`  
**Services Using**: MT5Service, TradeService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Audit trail for all MT5 synchronization operations

---

### `mt5_accounts`
**Purpose**: MT5 account linking, credentials, and connection management  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `server_id`, `account_number`, `encrypted_password`, `balance`, `equity`, `status`, `last_sync_at`  
**Services Using**: MT5Service, AccountService  
**Key Relationships**: 
- Foreign keys to `users.id` and `mt5_servers.id`
- One-to-many relationship with `mt5_trades`
- Indexed by `user_id, server_id` for quick lookups

---

### `mt5_trades`
**Purpose**: MT5-specific trade data synchronization and platform records  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `platform_trade_id`, `mt5_ticket`, `symbol`, `direction`, `volume`, `price_open`, `price_close`, `status`, `profit`  
**Services Using**: MT5Service, TradeService  
**Key Relationships**: 
- Foreign key to `mt5_accounts.id`
- Foreign key to `trades.id` (platform_trade_id)
- Unique index on `account_id, mt5_ticket`

---

### `mt5_servers`
**Purpose**: MT5 server connection configurations and health monitoring  
**Domain**: Trading  
**Primary Key**: `id` (UUID)  
**Key Fields**: `name`, `host`, `port`, `status`, `is_primary`, `connection_timeout`, `heartbeat_interval`  
**Services Using**: MT5Service  
**Key Relationships**: 
- Referenced by `mt5_accounts.server_id`
- Health check and load balancing configuration

---

##⚠️ Risk Domain Tables

### `violations`
**Purpose**: Risk rule violations, breaches, and compliance tracking  
**Domain**: Risk  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `violation_type`, `description`, `current_value`, `threshold_value`, `symbol`, `is_resolved`, `resolved_at`, `resolved_by`  
**Services Using**: RiskEngineService, ViolationService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Foreign key to `users.id` (resolved_by)
- Foreign key to `trades.id` (optional)
- Referenced by `account_status_history.violation_id`

---

### `account_status_history`
**Purpose**: Account status change tracking with reasons and audit trail  
**Domain**: Risk  
**Primary Key**: `id` (UUID)  
**Key Fields**: `account_id`, `from_status`, `to_status`, `changed_by`, `change_reason`, `change_notes`, `changed_at`  
**Services Using**: RiskEngineService, AccountService  
**Key Relationships**: 
- Foreign key to `accounts.id`
- Foreign key to `users.id` (changed_by)
- Foreign key to `violations.id` (optional)

---

### `job_execution_log`
**Purpose**: Automated risk evaluation job execution logs and monitoring  
**Domain**: Risk  
**Primary Key**: `id` (UUID)  
**Key Fields**: `job_type`, `status`, `started_at`, `completed_at`, `records_processed`, `error_message`, `execution_details`  
**Services Using**: RiskEngineService, AdminService  
**Key Relationships**: None (standalone audit log)

---

##📊 Analytics Domain Tables

### `trader_metrics`
**Purpose**: Comprehensive trader performance analytics and metrics  
**Domain**: Analytics  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `win_rate`, `total_trades`, `total_profit`, `max_drawdown`, `profit_factor`, `risk_score`, `last_trade_time`  
**Services Using**: AnalyticsService, LeaderboardService  
**Key Relationships**: 
- Foreign key to `users.id`
- Real-time metrics calculation from trading data

---

### `leaderboard_cache`
**Purpose**: Cached ranking and performance leaderboards for performance  
**Domain**: Analytics  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `period`, `rank`, `win_rate`, `total_profit`, `trades_count`, `ranking_score`, `period_start`, `period_end`  
**Services Using**: LeaderboardService, AnalyticsService  
**Key Relationships**: 
- Foreign key to `users.id`
- Composite index on `period, user_id, rank` for fast ranking queries

---

### `platform_metrics`
**Purpose**: System-wide platform performance metrics and health indicators  
**Domain**: Analytics  
**Primary Key**: `id` (UUID)  
**Key Fields**: `metric_date`, `total_users`, `active_accounts`, `total_trades`, `revenue`, `new_signups`, `challenges_sold`, `system_uptime`  
**Services Using**: AnalyticsService, AdminService  
**Key Relationships**: None (daily aggregate metrics)

---

##📬 Notification Domain Tables

### `notifications`
**Purpose**: User notification records and delivery tracking  
**Domain**: Notification  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `type`, `title`, `message`, `status`, `priority`, `channels`, `scheduled_for`, `read_at`  
**Services Using**: NotificationService  
**Key Relationships**: 
- Foreign key to `users.id`
- Foreign key to `accounts.id` (optional)
- Foreign key to `notification_templates.id` (template_id)

---

### `notification_templates`
**Purpose**: Notification content templates with dynamic field support  
**Domain**: Notification  
**Primary Key**: `id` (UUID)  
**Key Fields**: `name`, `type`, `title_template`, `message_template`, `default_channels`, `is_active`, `variables`  
**Services Using**: NotificationService  
**Key Relationships**: 
- Referenced by `notifications.template_id`
- Template versioning and management

---

### `email_queue`
**Purpose**: Email delivery queue and scheduling system  
**Domain**: Notification  
**Primary Key**: `id` (UUID)  
**Key Fields**: `recipient_email`, `subject`, `body`, `status`, `priority`, `scheduled_for`, `attempts`, `last_error`  
**Services Using**: NotificationService, EmailService  
**Key Relationships**: 
- Foreign key to `notifications.id` (notification_id)
- Foreign key to `notification_templates.id` (template_id)

---

### `user_notification_settings`
**Purpose**: User communication preferences and notification settings  
**Domain**: Notification  
**Primary Key**: `id` (UUID)  
**Key Fields**: `user_id`, `email_enabled`, `in_app_enabled`, `sms_enabled`, `push_enabled`, `quiet_hours_start`, `quiet_hours_end`, `timezone`, `email_frequency`  
**Services Using**: NotificationService, UserService  
**Key Relationships**: 
- Foreign key to `users.id`
- One-to-one relationship (user_id unique)

---

##🔗 Cross-Domain Relationship Matrix

| Table | Primary References | Secondary References | Cross-Domain Impact |
|-------|-------------------|----------------------|-------------------|
| `users` | `roles` | `payments`, `accounts`, `notifications` | Identity → All domains |
| `accounts` | `users`, `payments` | `trades`, `violations`, `mt5_accounts` | Challenge → Trading → Risk |
| `trades` | `accounts` | `mt5_trades`, `violations` | Trading → Risk → Analytics |
| `payments` | `users`, `challenges` | `accounts`, `revenue_ledger` | Challenge → Financial |
| `notifications` | `users` | `notification_templates`, `email_queue` | Identity → Notification |

##🛠️ Key Constraints and Indexes

### Primary Constraints:
- **UUID Primary Keys**: All tables use UUID for global uniqueness
- **Unique Constraints**: 
  - `users.email`, `users.username`
  - `trades.account_id + ticket_id`
  - `mt5_trades.account_id + mt5_ticket`
  - `user_notification_settings.user_id`

### Critical Indexes:
- **Performance**: `accounts.user_id`, `trades.account_id`, `violations.account_id`
- **Time-based**: `trades.open_time`, `notifications.created_at`
- **Composite**: `leaderboard_cache.period + user_id + rank`

##🔐 Security and Access Control

### Data Sensitivity Levels:
- **High**: `users.password_hash`, `mt5_accounts.encrypted_password`
- **Medium**: `user_settings`, `payment.transaction_id`
- **Low**: `challenges`, `trader_metrics`, `platform_metrics`

### Audit Requirements:
- **Full Logging**: All CREATE, UPDATE, DELETE operations
- **Status Changes**: Account status modifications require history records
- **Financial Operations**: All monetary changes require ledger entries

This comprehensive database mapping ensures data integrity, optimal performance, and clear understanding of the platform's information architecture across all business domains.
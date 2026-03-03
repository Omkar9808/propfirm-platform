# Import all models here to ensure they are registered with SQLAlchemy
from app.models.user import User, UserSettings
from app.models.role import Role
from app.models.audit import LoginAuditLog

# Phase 2 models
from app.models.phase2.challenge import Challenge, ChallengeRuleVersion
from app.models.phase2.payment import Payment, RevenueLedger
from app.models.phase2.account import Account, AccountRuleSnapshot

# Phase 3 models
from app.models.phase3.trading import Trade, DailyStat, EquitySnapshot, MT5SyncLog

# Phase 4 models
from app.models.phase4.risk import Violation, AccountStatusHistory, JobExecutionLog

# Phase 5 models
from app.models.phase5.analytics import TraderMetrics, LeaderboardCache, PlatformMetrics

# Phase 6 models
from app.models.phase6.mt5 import MT5Server, MT5Account, MT5Trade
from app.models.phase6.notifications import Notification, NotificationTemplate, EmailQueue, UserNotificationSettings

# Monetization models
from app.models.monetization import Affiliate, Referral, AffiliateCommission

# This file ensures all models are imported when the app starts
# Add new models here as they are created
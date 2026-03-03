from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import auth, users, challenges, accounts, trades, risk, analytics, admin, mt5, notifications
from app.routes import monetization, payout, certificate, challenge_tier, enhanced_metrics, monetization_dashboard  # New monetization routes
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Prop Firm Practice Platform API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# MT5 and Notification routes
app.include_router(mt5.router, prefix=f"{settings.API_V1_STR}", tags=["mt5"])
app.include_router(notifications.router, prefix=f"{settings.API_V1_STR}", tags=["notifications"])

# Admin and Analytics routes (admin only)
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}", tags=["admin"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}", tags=["analytics"])

# Core business routes
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["challenges"])
app.include_router(accounts.router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(trades.router, prefix=f"{settings.API_V1_STR}/trades", tags=["trades"])
app.include_router(risk.router, prefix=f"{settings.API_V1_STR}/risk", tags=["risk"])

# Monetization routes
app.include_router(monetization.router, prefix=f"{settings.API_V1_STR}", tags=["monetization"])
app.include_router(payout.router, prefix=f"{settings.API_V1_STR}/payouts", tags=["payouts"])
app.include_router(certificate.router, prefix=f"{settings.API_V1_STR}/certificates", tags=["certificates"])
app.include_router(challenge_tier.router, prefix=f"{settings.API_V1_STR}/challenge-tiers", tags=["challenge-tiers"])
app.include_router(enhanced_metrics.router, prefix=f"{settings.API_V1_STR}/enhanced-metrics", tags=["enhanced-metrics"])
app.include_router(monetization_dashboard.router, prefix=f"{settings.API_V1_STR}/monetization-dashboard", tags=["monetization-dashboard"])

# Authentication routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Prop Firm Practice Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
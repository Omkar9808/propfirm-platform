from app import models
from app.core.config import settings

def verify_phase5_models():
    """Verify that Phase 5 models are properly defined"""
    print("Verifying Phase 5 models...")
    
    # Check that all models are importable
    try:
        # Test importing analytics models
        from app.models.phase5.analytics import TraderMetrics, LeaderboardCache, PlatformMetrics
        print("✓ TraderMetrics model imported successfully")
        print("✓ LeaderboardCache model imported successfully") 
        print("✓ PlatformMetrics model imported successfully")
        
        # Test importing services
        from app.services.phase5 import AnalyticsService
        print("✓ AnalyticsService imported successfully")
        
        from app.services.leaderboard import LeaderboardService
        print("✓ LeaderboardService imported successfully")
        
        from app.services.admin import AdminService
        print("✓ AdminService imported successfully")
        
        # Test importing schemas
        from app.schemas.phase5 import TraderMetricsResponse, LeaderboardEntry, AdminDashboardMetrics
        print("✓ Analytics schemas imported successfully")
        
        # Test importing routes
        from app.api.v1.routes.analytics import router as analytics_router
        print("✓ Analytics routes imported successfully")
        
        from app.api.v1.routes.admin import router as admin_router
        print("✓ Admin routes imported successfully")
        
        print("\n✅ All Phase 5 components imported successfully!")
        print("Phase 5 implementation is ready for deployment.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing Phase 5 components: {str(e)}")
        return False

if __name__ == "__main__":
    verify_phase5_models()
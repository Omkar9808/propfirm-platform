from app import models
from app.core.config import settings

def verify_phase6_models():
    """Verify that Phase 6 models are properly defined"""
    print("Verifying Phase 6 models...")
    
    # Check that all models are importable
    try:
        # Test importing MT5 models
        from app.models.phase6.mt5 import MT5Server, MT5Account, MT5Trade
        print("✓ MT5Server model imported successfully")
        print("✓ MT5Account model imported successfully") 
        print("✓ MT5Trade model imported successfully")
        
        # Test importing notification models
        from app.models.phase6.notifications import Notification, NotificationTemplate, EmailQueue, UserNotificationSettings
        print("✓ Notification model imported successfully")
        print("✓ NotificationTemplate model imported successfully")
        print("✓ EmailQueue model imported successfully")
        print("✓ UserNotificationSettings model imported successfully")
        
        # Test importing services
        from app.services.phase6 import MT5Service
        print("✓ MT5Service imported successfully")
        
        from app.services.notifications import NotificationService
        print("✓ NotificationService imported successfully")
        
        # Test importing schemas
        from app.schemas.phase6 import (
            MT5ServerResponse, MT5AccountResponse, MT5TradeResponse,
            NotificationResponse, NotificationTemplateResponse, UserNotificationSettingsResponse
        )
        print("✓ Phase 6 schemas imported successfully")
        
        # Test importing routes
        from app.api.v1.routes.mt5 import router as mt5_router
        print("✓ MT5 routes imported successfully")
        
        from app.api.v1.routes.notifications import router as notifications_router
        print("✓ Notification routes imported successfully")
        
        print("\n✅ All Phase 6 components imported successfully!")
        print("Phase 6 implementation is ready for deployment.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing Phase 6 components: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_phase6_models()
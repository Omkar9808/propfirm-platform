from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.phase5 import AnalyticsService
from app.services.leaderboard import LeaderboardService
from app.services.admin import AdminService
from app.schemas.phase5 import (
    TraderMetricsResponse, TraderPerformanceSummary, PlatformOverview,
    LeaderboardEntry, AnalyticsStatus, AnalyticsSettings,
    AdminDashboardMetrics, UserManagementAction, AccountManagementAction,
    RevenueReportRequest, RevenueReportResponse
)
from app.core.security import verify_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Trader Analytics Endpoints
@router.get("/trader/{user_id}/metrics", response_model=TraderMetricsResponse)
async def get_trader_metrics(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get trader metrics for a specific user"""
    # Users can view their own metrics, admins can view any
    if str(current_user.id) != user_id:
        verify_role(current_user, ["admin", "super_admin"])
    
    try:
        metrics = AnalyticsService.calculate_trader_metrics(db, user_id)
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating trader metrics: {str(e)}"
        )

@router.post("/trader/{user_id}/calculate", response_model=TraderMetricsResponse)
async def calculate_trader_metrics(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Force recalculate trader metrics"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        metrics = AnalyticsService.calculate_trader_metrics(db, user_id)
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating trader metrics: {str(e)}"
        )

@router.get("/trader/{user_id}/performance", response_model=TraderPerformanceSummary)
async def get_trader_performance(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive trader performance summary"""
    # Users can view their own performance, admins can view any
    if str(current_user.id) != user_id:
        verify_role(current_user, ["admin", "super_admin"])
    
    try:
        performance = AnalyticsService.get_trader_performance_summary(db, user_id)
        return performance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting trader performance: {str(e)}"
        )

@router.post("/calculate-all", response_model=dict)
async def calculate_all_trader_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calculate metrics for all traders (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        result = AnalyticsService.calculate_all_trader_metrics(db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating all trader metrics: {str(e)}"
        )

# Leaderboard Endpoints
@router.get("/leaderboard/{period}", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    period: str = "all_time",
    limit: int = Query(100, ge=1, le=1000),
    use_cache: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get leaderboard for a specific period"""
    try:
        if use_cache and LeaderboardService.should_update_leaderboard(db):
            # Update cache if needed
            LeaderboardService.update_leaderboard_cache(db)
        
        if use_cache:
            leaderboard = LeaderboardService.get_cached_leaderboard(db, period, limit)
        else:
            leaderboard = LeaderboardService.generate_leaderboard(db, period, limit)
        
        return leaderboard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting leaderboard: {str(e)}"
        )

@router.get("/leaderboard/user/{user_id}", response_model=Optional[LeaderboardEntry])
async def get_user_ranking(
    user_id: str,
    period: str = Query("all_time"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific user's ranking"""
    # Users can view their own ranking, admins can view any
    if str(current_user.id) != user_id:
        verify_role(current_user, ["admin", "super_admin"])
    
    try:
        ranking = LeaderboardService.get_user_ranking(db, user_id, period)
        return ranking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting user ranking: {str(e)}"
        )

@router.post("/leaderboard/update-cache", response_model=dict)
async def update_leaderboard_cache(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Force update leaderboard cache (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        result = LeaderboardService.update_leaderboard_cache(db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating leaderboard cache: {str(e)}"
        )

@router.get("/leaderboard/statistics", response_model=dict)
async def get_leaderboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get leaderboard statistics"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        stats = LeaderboardService.get_leaderboard_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting leaderboard statistics: {str(e)}"
        )

# Platform Analytics Endpoints
@router.get("/platform/overview", response_model=PlatformOverview)
async def get_platform_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get platform overview statistics"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        overview = AnalyticsService.get_platform_overview(db)
        return overview
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting platform overview: {str(e)}"
        )

@router.post("/platform/generate-metrics", response_model=dict)
async def generate_platform_metrics(
    target_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate platform metrics for a specific date (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        metrics = AnalyticsService.generate_platform_metrics(db, target_date)
        return {
            "success": True,
            "message": "Platform metrics generated successfully",
            "metrics_id": str(metrics.id),
            "metric_date": metrics.metric_date
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating platform metrics: {str(e)}"
        )

@router.get("/analytics-status", response_model=AnalyticsStatus)
async def get_analytics_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get analytics system status"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # Get last metrics calculation
        last_metrics = db.query(PlatformMetrics).order_by(
            PlatformMetrics.created_at.desc()
        ).first()
        
        # Get leaderboard status
        leaderboard_stats = LeaderboardService.get_leaderboard_statistics(db)
        
        return AnalyticsStatus(
            is_running=True,
            last_metrics_calculation=last_metrics.created_at if last_metrics else None,
            last_leaderboard_update=leaderboard_stats.get('last_updated'),
            next_scheduled_run=datetime.utcnow() + timedelta(hours=1),
            traders_processed=db.query(TraderMetrics).count(),
            leaderboard_entries=sum(
                stats['entry_count'] 
                for stats in leaderboard_stats.get('periods', {}).values()
            ),
            platform_metrics_entries=db.query(PlatformMetrics).count(),
            settings=AnalyticsSettings()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting analytics status: {str(e)}"
        )
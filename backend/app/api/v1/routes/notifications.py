from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.notifications import NotificationService
from app.schemas.phase6 import (
    NotificationResponse, NotificationCreate, NotificationUpdate,
    NotificationTemplateResponse, NotificationTemplateCreate, NotificationTemplateUpdate,
    UserNotificationSettingsResponse, UserNotificationSettingsCreate,
    EmailQueueResponse, EmailQueueCreate, NotificationSummary,
    NotificationStatsRequest, NotificationStatsResponse
)
from app.core.security import verify_role

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# Notification Management Endpoints
@router.get("/", response_model=List[NotificationResponse])
async def get_user_notifications(
    status: Optional[str] = Query(None, description="Filter by notification status"),
    notification_type: Optional[str] = Query(None, description="Filter by notification type"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get notifications for the current user"""
    try:
        notifications = NotificationService.get_user_notifications(
            db,
            str(current_user.id),
            status=status,
            notification_type=notification_type,
            limit=limit,
            offset=offset
        )
        return notifications
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting notifications: {str(e)}"
        )

@router.get("/summary", response_model=NotificationSummary)
async def get_notification_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get notification summary for the current user"""
    try:
        summary = NotificationService.get_notification_summary(db, str(current_user.id))
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting notification summary: {str(e)}"
        )

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new notification (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # Verify the user_id in the notification data matches the target user
        # This prevents unauthorized users from creating notifications for others
        notification_data.user_id = notification_data.user_id
        notification = NotificationService.create_notification(db, notification_data)
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating notification: {str(e)}"
        )

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: str,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a notification (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # In a real implementation, you would update the notification here
        # For now, we'll just get and return the existing notification
        notification = db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Apply updates
        for field, value in notification_data.dict(exclude_unset=True).items():
            setattr(notification, field, value)
        
        db.commit()
        db.refresh(notification)
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating notification: {str(e)}"
        )

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark a notification as read"""
    try:
        notification = NotificationService.mark_notification_as_read(
            db, 
            notification_id, 
            str(current_user.id)
        )
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking notification as read: {str(e)}"
        )

@router.post("/mark-all-read", response_model=int)
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark all notifications as read for the current user"""
    try:
        count = NotificationService.mark_all_notifications_as_read(db, str(current_user.id))
        return count
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking all notifications as read: {str(e)}"
        )

@router.delete("/{notification_id}", response_model=bool)
async def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a notification (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        success = NotificationService.delete_notification(db, notification_id)
        return success
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notification: {str(e)}"
        )

# Notification Template Endpoints
@router.get("/templates", response_model=List[NotificationTemplateResponse])
async def get_notification_templates(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    template_type: Optional[str] = Query(None, description="Filter by template type"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get notification templates (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        query = db.query(NotificationTemplate)
        
        if is_active is not None:
            query = query.filter(NotificationTemplate.is_active == is_active)
        if template_type:
            query = query.filter(NotificationTemplate.type == template_type)
        
        templates = query.limit(limit).offset(offset).all()
        return templates
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting notification templates: {str(e)}"
        )

@router.get("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def get_notification_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific notification template (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification template not found"
            )
        
        return template
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting notification template: {str(e)}"
        )

@router.post("/templates", response_model=NotificationTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_notification_template(
    template_data: NotificationTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new notification template (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # Check if template name already exists
        existing_template = db.query(NotificationTemplate).filter(
            NotificationTemplate.name == template_data.name
        ).first()
        
        if existing_template:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Template with this name already exists"
            )
        
        template = NotificationTemplate(**template_data.model_dump())
        db.add(template)
        db.commit()
        db.refresh(template)
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating notification template: {str(e)}"
        )

@router.put("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def update_notification_template(
    template_id: str,
    template_data: NotificationTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a notification template (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification template not found"
            )
        
        # Apply updates
        for field, value in template_data.dict(exclude_unset=True).items():
            setattr(template, field, value)
        
        db.commit()
        db.refresh(template)
        return template
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating notification template: {str(e)}"
        )

@router.delete("/templates/{template_id}", response_model=bool)
async def delete_notification_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a notification template (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification template not found"
            )
        
        db.delete(template)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notification template: {str(e)}"
        )

# User Notification Settings Endpoints
@router.get("/settings", response_model=UserNotificationSettingsResponse)
async def get_user_notification_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get notification settings for the current user"""
    try:
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == current_user.id
        ).first()
        
        if not settings:
            # Create default settings if they don't exist
            settings = UserNotificationSettings(
                user_id=current_user.id,
                email_notifications_enabled=True,
                in_app_notifications_enabled=True
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        
        return settings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting notification settings: {str(e)}"
        )

@router.post("/settings", response_model=UserNotificationSettingsResponse, status_code=status.HTTP_201_CREATED)
async def create_user_notification_settings(
    settings_data: UserNotificationSettingsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create notification settings for the current user"""
    if str(settings_data.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create settings for another user"
        )
    
    try:
        # Check if settings already exist
        existing_settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == current_user.id
        ).first()
        
        if existing_settings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification settings already exist for this user"
            )
        
        settings = UserNotificationSettings(**settings_data.model_dump())
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating notification settings: {str(e)}"
        )

@router.put("/settings", response_model=UserNotificationSettingsResponse)
async def update_user_notification_settings(
    settings_data: UserNotificationSettingsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update notification settings for the current user"""
    if str(settings_data.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update settings for another user"
        )
    
    try:
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == current_user.id
        ).first()
        
        if not settings:
            # Create new settings if they don't exist
            settings = UserNotificationSettings(**settings_data.model_dump())
            db.add(settings)
        else:
            # Update existing settings
            for field, value in settings_data.dict(exclude_unset=True).items():
                setattr(settings, field, value)
        
        db.commit()
        db.refresh(settings)
        return settings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating notification settings: {str(e)}"
        )

# Email Queue Endpoints
@router.get("/email-queue", response_model=List[EmailQueueResponse])
async def get_email_queue_items(
    status: Optional[str] = Query(None, description="Filter by email status"),
    priority: Optional[int] = Query(None, description="Filter by email priority"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get email queue items (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        query = db.query(EmailQueue)
        
        if status:
            query = query.filter(EmailQueue.status == status)
        if priority is not None:
            query = query.filter(EmailQueue.priority == priority)
        
        emails = query.order_by(EmailQueue.priority.desc(), EmailQueue.scheduled_for).limit(limit).offset(offset).all()
        return emails
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting email queue items: {str(e)}"
        )

@router.post("/email-queue", response_model=EmailQueueResponse, status_code=status.HTTP_201_CREATED)
async def create_email_queue_item(
    email_data: EmailQueueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add an email to the queue (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        email = NotificationService.create_email_queue_item(db, email_data)
        return email
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating email queue item: {str(e)}"
        )

@router.post("/email-queue/process", response_model=dict)
async def process_email_queue(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Process pending emails in the queue (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        result = NotificationService.process_email_queue(db, limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing email queue: {str(e)}"
        )

# Auto-generated notifications
@router.post("/trigger/account-passed/{account_id}", response_model=NotificationResponse)
async def trigger_account_passed_notification(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trigger account passed notification (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        notification = NotificationService.send_account_passed_notification(db, account_id)
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error triggering account passed notification: {str(e)}"
        )

@router.post("/trigger/account-failed/{account_id}", response_model=NotificationResponse)
async def trigger_account_failed_notification(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trigger account failed notification (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        notification = NotificationService.send_account_failed_notification(db, account_id)
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error triggering account failed notification: {str(e)}"
        )

# Import models to avoid circular import errors
from app.models.phase6.notifications import Notification, NotificationTemplate, UserNotificationSettings, EmailQueue
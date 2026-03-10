from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional
from app.models.phase6.notifications import (
    Notification, NotificationTemplate, EmailQueue, UserNotificationSettings,
    NotificationTypeEnum, NotificationPriorityEnum, NotificationStatusEnum,
    NotificationChannelEnum
)
from app.models.user import User
from app.models.phase2.account import Account
from app.schemas.phase6 import (
    NotificationCreate, NotificationUpdate, NotificationTemplateCreate,
    NotificationTemplateUpdate, UserNotificationSettingsCreate,
    EmailQueueCreate, NotificationSummary, NotificationStatsResponse
)
from app.core.config import settings
from app.core.logger import get_logger
import json
import uuid
from jinja2 import Template

logger = get_logger(__name__)

class NotificationService:
    """Service for handling notifications and alerts"""
    
    @staticmethod
    def create_notification(db: Session, notification_data: NotificationCreate) -> Notification:
        """Create a new notification"""
        try:
            # Verify user exists
            user = db.query(User).filter(User.id == notification_data.user_id).first()
            if not user:
                raise ValueError(f"User {notification_data.user_id} not found")
            
            # Verify account exists if provided
            if notification_data.account_id:
                account = db.query(Account).filter(
                    Account.id == notification_data.account_id,
                    Account.user_id == notification_data.user_id
                ).first()
                if not account:
                    raise ValueError(f"Account {notification_data.account_id} not found for user")
            
            # Get user notification settings
            user_settings = NotificationService._get_user_settings(db, notification_data.user_id)
            
            # Check if user wants this type of notification
            if not NotificationService._should_send_notification(user_settings, notification_data.type):
                logger.info(f"Notification suppressed for user {user.username} - {notification_data.type}")
                return None
            
            # Check quiet hours
            if NotificationService._is_quiet_hours(user_settings):
                # Schedule for after quiet hours
                notification_data.scheduled_for = NotificationService._get_next_delivery_time(user_settings)
            
            # Create notification
            notification = Notification(
                user_id=notification_data.user_id,
                account_id=notification_data.account_id,
                type=notification_data.type,
                title=notification_data.title,
                message=notification_data.message,
                priority=notification_data.priority,
                channels=json.dumps(notification_data.channels),
                scheduled_for=notification_data.scheduled_for,
                expires_at=notification_data.expires_at,
                data=json.dumps(notification_data.data) if notification_data.data else None,
                status=NotificationStatusEnum.PENDING
            )
            
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
            # Process notification based on channels
            NotificationService._process_notification_channels(db, notification, user_settings)
            
            logger.info(f"Notification created for user {user.username}: {notification.title}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def create_notification_from_template(
        db: Session, 
        template_name: str, 
        user_id: str, 
        context: Dict = None,
        account_id: str = None
    ) -> Notification:
        """Create notification using a template"""
        try:
            # Get template
            template = db.query(NotificationTemplate).filter(
                NotificationTemplate.name == template_name,
                NotificationTemplate.is_active == True
            ).first()
            
            if not template:
                raise ValueError(f"Active template '{template_name}' not found")
            
            # Get user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Render templates with context
            context = context or {}
            context.update({
                'user': user,
                'username': user.username,
                'email': user.email
            })
            
            if account_id:
                account = db.query(Account).filter(Account.id == account_id).first()
                if account:
                    context['account'] = account
                    context['account_number'] = account.account_number
            
            title_template = Template(template.title_template)
            message_template = Template(template.message_template)
            
            title = title_template.render(**context)
            message = message_template.render(**context)
            
            # Parse data template if exists
            data = None
            if template.data_template:
                data_template = Template(template.data_template)
                data_str = data_template.render(**context)
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    data = {"template_data": data_str}
            
            # Create notification
            notification = NotificationCreate(
                user_id=user_id,
                account_id=account_id,
                type=template.type.value,
                title=title,
                message=message,
                priority=template.default_priority.value,
                channels=json.loads(template.default_channels),
                data=data
            )
            
            # Create the notification
            result = NotificationService.create_notification(db, notification)
            
            # Update template usage stats
            template.use_count += 1
            template.last_used_at = datetime.utcnow()
            db.commit()
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating notification from template: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def send_account_passed_notification(db: Session, account_id: str) -> Notification:
        """Send notification when account passes challenge"""
        try:
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                raise ValueError(f"Account {account_id} not found")
            
            return NotificationService.create_notification_from_template(
                db,
                "account_passed",
                account.user_id,
                {
                    "account_number": account.account_number,
                    "balance": float(account.current_balance or 0)
                },
                account_id
            )
            
        except Exception as e:
            logger.error(f"Error sending account passed notification: {str(e)}")
            raise

    @staticmethod
    def send_account_failed_notification(db: Session, account_id: str) -> Notification:
        """Send notification when account fails challenge"""
        try:
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                raise ValueError(f"Account {account_id} not found")
            
            return NotificationService.create_notification_from_template(
                db,
                "account_failed",
                account.user_id,
                {
                    "account_number": account.account_number
                },
                account_id
            )
            
        except Exception as e:
            logger.error(f"Error sending account failed notification: {str(e)}")
            raise

    @staticmethod
    def send_risk_violation_notification(db: Session, account_id: str, violation_type: str) -> Notification:
        """Send notification for risk violations"""
        try:
            account = db.query(Account).filter(Account.id == account_id).first()
            if not account:
                raise ValueError(f"Account {account_id} not found")
            
            return NotificationService.create_notification_from_template(
                db,
                "risk_violation",
                account.user_id,
                {
                    "account_number": account.account_number,
                    "violation_type": violation_type
                },
                account_id
            )
            
        except Exception as e:
            logger.error(f"Error sending risk violation notification: {str(e)}")
            raise

    @staticmethod
    def get_user_notifications(
        db: Session, 
        user_id: str, 
        status: str = None,
        notification_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """Get notifications for a user"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)
            
            if status:
                query = query.filter(Notification.status == status)
            
            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            notifications = query.order_by(desc(Notification.created_at)).limit(limit).offset(offset).all()
            return notifications
            
        except Exception as e:
            logger.error(f"Error getting user notifications: {str(e)}")
            raise

    @staticmethod
    def get_notification_summary(db: Session, user_id: str) -> NotificationSummary:
        """Get notification summary for a user"""
        try:
            # Total count
            total_count = db.query(func.count(Notification.id)).filter(
                Notification.user_id == user_id
            ).scalar()
            
            # Unread count
            unread_count = db.query(func.count(Notification.id)).filter(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.status.in_([NotificationStatusEnum.SENT, NotificationStatusEnum.DELIVERED])
            ).scalar()
            
            # Counts by type
            type_counts = dict(
                db.query(Notification.type, func.count(Notification.id)).filter(
                    Notification.user_id == user_id
                ).group_by(Notification.type).all()
            )
            
            # Counts by priority
            priority_counts = dict(
                db.query(Notification.priority, func.count(Notification.id)).filter(
                    Notification.user_id == user_id
                ).group_by(Notification.priority).all()
            )
            
            # Counts by status
            status_counts = dict(
                db.query(Notification.status, func.count(Notification.id)).filter(
                    Notification.user_id == user_id
                ).group_by(Notification.status).all()
            )
            
            return NotificationSummary(
                unread_count=unread_count,
                total_count=total_count,
                counts_by_type=type_counts,
                counts_by_priority=priority_counts,
                counts_by_status=status_counts
            )
            
        except Exception as e:
            logger.error(f"Error getting notification summary: {str(e)}")
            raise

    @staticmethod
    def mark_notification_as_read(db: Session, notification_id: str, user_id: str = None) -> Notification:
        """Mark notification as read"""
        try:
            query = db.query(Notification).filter(Notification.id == notification_id)
            if user_id:
                query = query.filter(Notification.user_id == user_id)
            
            notification = query.first()
            if not notification:
                raise ValueError(f"Notification {notification_id} not found")
            
            if not notification.is_read:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
                db.commit()
                db.refresh(notification)
            
            return notification
            
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def mark_all_notifications_as_read(db: Session, user_id: str) -> int:
        """Mark all notifications as read for a user"""
        try:
            updated_count = db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).update({
                Notification.is_read: True,
                Notification.read_at: datetime.utcnow()
            })
            
            db.commit()
            return updated_count
            
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def delete_notification(db: Session, notification_id: str, user_id: str = None) -> bool:
        """Delete a notification"""
        try:
            query = db.query(Notification).filter(Notification.id == notification_id)
            if user_id:
                query = query.filter(Notification.user_id == user_id)
            
            notification = query.first()
            if not notification:
                raise ValueError(f"Notification {notification_id} not found")
            
            db.delete(notification)
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting notification: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def create_email_queue_item(db: Session, email_data: EmailQueueCreate) -> EmailQueue:
        """Create an email queue item"""
        try:
            email_queue = EmailQueue(
                recipient_email=email_data.recipient_email,
                recipient_name=email_data.recipient_name,
                subject=email_data.subject,
                body_html=email_data.body_html,
                body_text=email_data.body_text,
                template_id=email_data.template_id,
                sender_email=email_data.sender_email,
                sender_name=email_data.sender_name,
                priority=email_data.priority,
                max_retries=email_data.max_retries,
                scheduled_for=datetime.utcnow()  # Send immediately
            )
            
            db.add(email_queue)
            db.commit()
            db.refresh(email_queue)
            
            logger.info(f"Email queued for {email_data.recipient_email}: {email_data.subject}")
            return email_queue
            
        except Exception as e:
            logger.error(f"Error creating email queue item: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def process_email_queue(db: Session, limit: int = 100) -> dict:
        """Process pending emails in queue"""
        try:
            # Get pending emails
            pending_emails = db.query(EmailQueue).filter(
                EmailQueue.status == "pending",
                EmailQueue.scheduled_for <= datetime.utcnow(),
                EmailQueue.retry_count < EmailQueue.max_retries
            ).order_by(EmailQueue.priority.desc(), EmailQueue.scheduled_for).limit(limit).all()
            
            processed_count = 0
            failed_count = 0
            
            for email in pending_emails:
                try:
                    # Send email (simulated)
                    success = NotificationService._send_email(email)
                    
                    if success:
                        email.status = "sent"
                        email.sent_at = datetime.utcnow()
                        processed_count += 1
                        logger.info(f"Email sent successfully to {email.recipient_email}")
                    else:
                        email.retry_count += 1
                        email.status = "failed" if email.retry_count >= email.max_retries else "pending"
                        failed_count += 1
                        logger.error(f"Failed to send email to {email.recipient_email}")
                
                except Exception as e:
                    email.retry_count += 1
                    email.status = "failed" if email.retry_count >= email.max_retries else "pending"
                    email.failure_reason = str(e)
                    failed_count += 1
                    logger.error(f"Error processing email for {email.recipient_email}: {str(e)}")
            
            db.commit()
            
            return {
                "processed": processed_count,
                "failed": failed_count,
                "total": len(pending_emails)
            }
            
        except Exception as e:
            logger.error(f"Error processing email queue: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def _get_user_settings(db: Session, user_id: str) -> UserNotificationSettings:
        """Get or create user notification settings"""
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()
        
        if not settings:
            settings = UserNotificationSettings(
                user_id=user_id,
                email_notifications_enabled=True,
                in_app_notifications_enabled=True
            )
            db.add(settings)
            db.commit()
        
        return settings

    @staticmethod
    def _should_send_notification(user_settings: UserNotificationSettings, notification_type: str) -> bool:
        """Check if notification should be sent based on user settings"""
        # Check global settings
        if not user_settings.email_notifications_enabled and not user_settings.in_app_notifications_enabled:
            return False
        
        # Check specific notification type settings
        type_settings_map = {
            "account_update": user_settings.account_update_enabled,
            "trade_alert": user_settings.trade_alert_enabled,
            "risk_violation": user_settings.risk_violation_enabled,
            "system_alert": user_settings.system_alert_enabled,
            "account_passed": user_settings.account_update_enabled,
            "account_failed": user_settings.account_update_enabled,
            "payment_confirmed": user_settings.account_update_enabled
        }
        
        return type_settings_map.get(notification_type, True)

    @staticmethod
    def _is_quiet_hours(user_settings: UserNotificationSettings) -> bool:
        """Check if current time is within user's quiet hours"""
        if not user_settings.quiet_hours_start or not user_settings.quiet_hours_end:
            return False
        
        try:
            current_time = datetime.now().time()
            start_time = datetime.strptime(user_settings.quiet_hours_start, "%H:%M").time()
            end_time = datetime.strptime(user_settings.quiet_hours_end, "%H:%M").time()
            
            # Handle overnight quiet hours (e.g., 22:00 to 08:00)
            if start_time > end_time:
                return current_time >= start_time or current_time <= end_time
            else:
                return start_time <= current_time <= end_time
                
        except Exception:
            return False

    @staticmethod
    def _get_next_delivery_time(user_settings: UserNotificationSettings) -> datetime:
        """Get next delivery time after quiet hours"""
        if not user_settings.quiet_hours_end:
            return datetime.utcnow()
        
        try:
            end_time = datetime.strptime(user_settings.quiet_hours_end, "%H:%M").time()
            next_delivery = datetime.combine(datetime.utcnow().date(), end_time)
            
            # If end time has passed today, schedule for tomorrow
            if next_delivery < datetime.utcnow():
                next_delivery += timedelta(days=1)
            
            return next_delivery
        except Exception:
            return datetime.utcnow()

    @staticmethod
    def _process_notification_channels(db: Session, notification: Notification, user_settings: UserNotificationSettings) -> None:
        """Process notification through specified channels"""
        try:
            channels = json.loads(notification.channels)
            
            # Process email channel
            if "email" in channels and user_settings.email_notifications_enabled:
                NotificationService._queue_email_notification(db, notification, user_settings)
            
            # Process in-app channel
            if "in_app" in channels and user_settings.in_app_notifications_enabled:
                notification.status = NotificationStatusEnum.SENT
                notification.sent_at = datetime.utcnow()
            
            # Process SMS channel (if enabled)
            if "sms" in channels and user_settings.sms_notifications_enabled:
                # SMS implementation would go here
                pass
            
            # Process push channel (if enabled)
            if "push" in channels and user_settings.push_notifications_enabled:
                # Push notification implementation would go here
                pass
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error processing notification channels: {str(e)}")
            db.rollback()

    @staticmethod
    def _queue_email_notification(db: Session, notification: Notification, user_settings: UserNotificationSettings) -> None:
        """Queue email notification"""
        try:
            user = db.query(User).filter(User.id == notification.user_id).first()
            if not user:
                return
            
            email_queue = EmailQueueCreate(
                recipient_email=user.email,
                recipient_name=user.full_name,
                subject=notification.title,
                body_html=f"<h2>{notification.title}</h2><p>{notification.message}</p>",
                body_text=notification.message,
                sender_email=settings.EMAIL_FROM or "noreply@propfirm.com",
                sender_name=settings.EMAIL_FROM_NAME or "Prop Firm Platform",
                priority=1 if notification.priority == "urgent" else 0
            )
            
            NotificationService.create_email_queue_item(db, email_queue)
            
        except Exception as e:
            logger.error(f"Error queuing email notification: {str(e)}")

    @staticmethod
    def _send_email(email_queue: EmailQueue) -> bool:
        """Simulate sending email (replace with actual email service)"""
        # In real implementation, integrate with email service like SMTP, SendGrid, etc.
        try:
            # Simulate email sending
            import time
            time.sleep(0.1)  # Simulate network delay
            
            # Simulate 95% success rate
            import random
            return random.random() < 0.95
            
        except Exception:
            return False
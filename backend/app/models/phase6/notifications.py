from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from datetime import datetime
from enum import Enum
import uuid

class NotificationTypeEnum(str, Enum):
    ACCOUNT_UPDATE = "account_update"
    TRADE_ALERT = "trade_alert"
    RISK_VIOLATION = "risk_violation"
    SYSTEM_ALERT = "system_alert"
    ACCOUNT_PASSED = "account_passed"
    ACCOUNT_FAILED = "account_failed"
    PAYMENT_CONFIRMED = "payment_confirmed"
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_REPORT = "weekly_report"
    PLATFORM_ANNOUNCEMENT = "platform_announcement"

class NotificationPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationStatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class NotificationChannelEnum(str, Enum):
    EMAIL = "email"
    IN_APP = "in_app"
    SMS = "sms"
    PUSH = "push"

class Notification(BaseModel):
    __tablename__ = "notifications"
    
    # References
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))  # Optional account reference
    
    # Notification Content
    type = Column(SQLEnum(NotificationTypeEnum), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(Text)  # JSON string for additional data
    
    # Delivery Settings
    priority = Column(SQLEnum(NotificationPriorityEnum), default=NotificationPriorityEnum.MEDIUM, nullable=False)
    channels = Column(Text, nullable=False)  # JSON array of channels: ["email", "in_app"]
    scheduled_for = Column(DateTime(timezone=True))  # For future notifications
    expires_at = Column(DateTime(timezone=True))  # Auto-expire after this time
    
    # Status Tracking
    status = Column(SQLEnum(NotificationStatusEnum), default=NotificationStatusEnum.PENDING, nullable=False)
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    
    # Delivery Attempts
    delivery_attempts = Column(Numeric, default=0, nullable=False)
    last_delivery_attempt = Column(DateTime(timezone=True))
    failure_reason = Column(Text)
    
    # User Interaction
    is_read = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    is_dismissed = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    account = relationship("Account", back_populates="notifications")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_notifications_user_status', 'user_id', 'status'),
        Index('ix_notifications_type_priority', 'type', 'priority'),
        Index('ix_notifications_scheduled_for', 'scheduled_for'),
        Index('ix_notifications_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Notification(user_id='{self.user_id}', type='{self.type}', status='{self.status}')>"

class NotificationTemplate(BaseModel):
    __tablename__ = "notification_templates"
    
    # Template Identification
    name = Column(String(100), nullable=False, unique=True)
    type = Column(SQLEnum(NotificationTypeEnum), nullable=False)
    
    # Template Content
    subject = Column(String(200))  # For email notifications
    title_template = Column(Text, nullable=False)  # Jinja2 template
    message_template = Column(Text, nullable=False)  # Jinja2 template
    data_template = Column(Text)  # JSON template for data field
    
    # Channel Configuration
    default_channels = Column(Text, nullable=False)  # Default JSON array of channels
    default_priority = Column(SQLEnum(NotificationPriorityEnum), default=NotificationPriorityEnum.MEDIUM, nullable=False)
    
    # Template Settings
    is_active = Column(Boolean, default=True, nullable=False)
    allow_customization = Column(Boolean, default=True, nullable=False)  # Can users modify template
    
    # Metadata
    description = Column(Text)
    tags = Column(Text)  # JSON array of tags for categorization
    version = Column(String(20), default="1.0", nullable=False)
    
    # Usage Statistics
    use_count = Column(Numeric, default=0, nullable=False)
    last_used_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<NotificationTemplate(name='{self.name}', type='{self.type}')>"

class EmailQueue(BaseModel):
    __tablename__ = "email_queue"
    
    # Email Content
    recipient_email = Column(String(255), nullable=False)
    recipient_name = Column(String(100))
    subject = Column(String(200), nullable=False)
    body_html = Column(Text)
    body_text = Column(Text)
    
    # Sending Configuration
    template_id = Column(UUID(as_uuid=True), ForeignKey("notification_templates.id"))
    sender_email = Column(String(255), nullable=False)
    sender_name = Column(String(100))
    
    # Status Tracking
    status = Column(String(20), default="pending", nullable=False)  # pending, sent, failed
    priority = Column(Numeric, default=1, nullable=False)  # Higher numbers = higher priority
    scheduled_for = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Delivery Information
    sent_at = Column(DateTime(timezone=True))
    delivery_confirmed_at = Column(DateTime(timezone=True))
    failure_reason = Column(Text)
    retry_count = Column(Numeric, default=0, nullable=False)
    max_retries = Column(Numeric, default=3, nullable=False)
    
    # Metadata
    message_id = Column(String(255))  # External email service message ID
    tracking_data = Column(Text)  # JSON for tracking opens/clicks
    
    # Relationships
    template = relationship("NotificationTemplate")
    
    # Indexes
    __table_args__ = (
        Index('ix_email_queue_status_priority', 'status', 'priority'),
        Index('ix_email_queue_scheduled_for', 'scheduled_for'),
        Index('ix_email_queue_template_id', 'template_id'),
    )
    
    def __repr__(self):
        return f"<EmailQueue(to='{self.recipient_email}', subject='{self.subject}', status='{self.status}')>"

class UserNotificationSettings(BaseModel):
    __tablename__ = "user_notification_settings"
    
    # User Reference
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    
    # Global Settings
    email_notifications_enabled = Column(Boolean, default=True, nullable=False)
    in_app_notifications_enabled = Column(Boolean, default=True, nullable=False)
    sms_notifications_enabled = Column(Boolean, default=False, nullable=False)
    push_notifications_enabled = Column(Boolean, default=True, nullable=False)
    
    # Notification Preferences by Type
    account_update_enabled = Column(Boolean, default=True, nullable=False)
    trade_alert_enabled = Column(Boolean, default=True, nullable=False)
    risk_violation_enabled = Column(Boolean, default=True, nullable=False)
    system_alert_enabled = Column(Boolean, default=True, nullable=False)
    marketing_enabled = Column(Boolean, default=False, nullable=False)  # Promotional emails
    
    # Timing Preferences
    daily_summary_enabled = Column(Boolean, default=True, nullable=False)
    weekly_report_enabled = Column(Boolean, default=False, nullable=False)
    quiet_hours_start = Column(String(5))  # HH:MM format
    quiet_hours_end = Column(String(5))  # HH:MM format
    timezone = Column(String(50), default="UTC", nullable=False)
    
    # Delivery Preferences
    email_frequency = Column(String(20), default="immediate")  # immediate, hourly, daily
    batch_notifications = Column(Boolean, default=False, nullable=False)  # Group notifications
    
    # Relationships
    user = relationship("User", back_populates="notification_settings")
    
    def __repr__(self):
        return f"<UserNotificationSettings(user_id='{self.user_id}')>"

# Update User model to include notification relationships
from app.models.user import User
from app.models.phase2.account import Account

User.notifications = relationship("Notification", back_populates="user")
User.notification_settings = relationship("UserNotificationSettings", back_populates="user", uselist=False)
Account.notifications = relationship("Notification", back_populates="account")
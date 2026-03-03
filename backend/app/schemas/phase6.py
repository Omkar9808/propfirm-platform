from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID

# MT5 Integration Schemas
class MT5ServerBase(BaseModel):
    name: str = Field(..., max_length=100)
    host: str = Field(..., max_length=100)
    port: int = Field(..., gt=0, lt=65536)
    username: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_primary: bool = False
    max_connections: int = Field(100, gt=0)

class MT5ServerCreate(MT5ServerBase):
    pass

class MT5ServerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    host: Optional[str] = Field(None, max_length=100)
    port: Optional[int] = Field(None, gt=0, lt=65536)
    username: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_primary: Optional[bool] = None
    max_connections: Optional[int] = Field(None, gt=0)
    status: Optional[str] = None

class MT5ServerResponse(MT5ServerBase):
    id: UUID
    status: str
    current_connections: int
    version: Optional[str] = None
    last_heartbeat: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MT5AccountBase(BaseModel):
    mt5_login: str = Field(..., max_length=50)
    mt5_password: str = Field(..., max_length=100)
    mt5_investor_password: Optional[str] = Field(None, max_length=100)
    server_id: UUID
    platform_account_id: UUID
    currency: str = Field("USD", max_length=3)
    leverage: int = Field(100, gt=0)
    is_demo: bool = True
    sync_interval_seconds: int = Field(60, gt=0)

class MT5AccountCreate(MT5AccountBase):
    user_id: UUID

class MT5AccountUpdate(BaseModel):
    mt5_password: Optional[str] = Field(None, max_length=100)
    mt5_investor_password: Optional[str] = Field(None, max_length=100)
    server_id: Optional[UUID] = None
    currency: Optional[str] = Field(None, max_length=3)
    leverage: Optional[int] = Field(None, gt=0)
    is_demo: Optional[bool] = None
    sync_interval_seconds: Optional[int] = Field(None, gt=0)
    status: Optional[str] = None

class MT5AccountResponse(MT5AccountBase):
    id: UUID
    user_id: UUID
    status: str
    balance: Decimal = Field(default=0)
    equity: Decimal = Field(default=0)
    margin: Decimal = Field(default=0)
    free_margin: Decimal = Field(default=0)
    margin_level: Decimal = Field(default=0)
    last_sync_time: Optional[datetime] = None
    next_sync_time: Optional[datetime] = None
    error_count: int
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MT5TradeBase(BaseModel):
    mt5_ticket: str = Field(..., max_length=50)
    symbol: str = Field(..., max_length=20)
    direction: str
    volume: Decimal
    price_open: Decimal
    time_open: datetime
    sl: Optional[Decimal] = None
    tp: Optional[Decimal] = None
    comment: Optional[str] = Field(None, max_length=255)
    magic_number: Optional[int] = None
    is_external: bool = False

class MT5TradeCreate(MT5TradeBase):
    account_id: UUID

class MT5TradeUpdate(BaseModel):
    price_close: Optional[Decimal] = None
    time_close: Optional[datetime] = None
    time_update: Optional[datetime] = None
    status: Optional[str] = None
    reason: Optional[str] = Field(None, max_length=50)
    profit: Optional[Decimal] = None
    swap: Optional[Decimal] = None
    commission: Optional[Decimal] = None

class MT5TradeResponse(MT5TradeBase):
    id: UUID
    account_id: UUID
    platform_trade_id: Optional[UUID] = None
    price_close: Optional[Decimal] = None
    time_close: Optional[datetime] = None
    time_update: Optional[datetime] = None
    status: str
    reason: Optional[str] = None
    profit: Decimal = Field(default=0)
    swap: Decimal = Field(default=0)
    commission: Decimal = Field(default=0)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# MT5 Connection and Sync Schemas
class MT5ConnectionStatus(BaseModel):
    server_id: UUID
    server_name: str
    status: str
    connected_accounts: int
    last_heartbeat: Optional[datetime] = None
    next_scheduled_sync: Optional[datetime] = None

class MT5SyncRequest(BaseModel):
    account_id: Optional[UUID] = None
    server_id: Optional[UUID] = None
    sync_type: str = Field("full", max_length=20)  # full, incremental, trades_only

class MT5SyncResponse(BaseModel):
    success: bool
    accounts_processed: int
    trades_imported: int
    sync_duration_ms: int
    error_message: Optional[str] = None
    next_sync_scheduled: Optional[datetime] = None

class MT5BalanceUpdate(BaseModel):
    account_id: UUID
    balance: Decimal
    equity: Decimal
    margin: Decimal = Field(default=0)
    free_margin: Decimal = Field(default=0)
    margin_level: Decimal = Field(default=0)
    timestamp: datetime

# Notification Schemas
class NotificationBase(BaseModel):
    type: str = Field(..., max_length=50)
    title: str = Field(..., max_length=200)
    message: str
    priority: str = "medium"
    channels: List[str] = ["email", "in_app"]
    scheduled_for: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    user_id: UUID
    account_id: Optional[UUID] = None

class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    message: Optional[str] = None
    status: Optional[str] = None
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_dismissed: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    account_id: Optional[UUID] = None
    status: str
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    delivery_attempts: int
    failure_reason: Optional[str] = None
    is_read: bool
    is_archived: bool
    is_dismissed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class NotificationTemplateBase(BaseModel):
    name: str = Field(..., max_length=100)
    type: str = Field(..., max_length=50)
    subject: Optional[str] = Field(None, max_length=200)
    title_template: str
    message_template: str
    data_template: Optional[str] = None
    default_channels: List[str] = ["email", "in_app"]
    default_priority: str = "medium"
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    subject: Optional[str] = Field(None, max_length=200)
    title_template: Optional[str] = None
    message_template: Optional[str] = None
    data_template: Optional[str] = None
    default_channels: Optional[List[str]] = None
    default_priority: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
    allow_customization: Optional[bool] = None

class NotificationTemplateResponse(NotificationTemplateBase):
    id: UUID
    is_active: bool
    allow_customization: bool
    use_count: int
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserNotificationSettingsBase(BaseModel):
    email_notifications_enabled: bool = True
    in_app_notifications_enabled: bool = True
    sms_notifications_enabled: bool = False
    push_notifications_enabled: bool = True
    account_update_enabled: bool = True
    trade_alert_enabled: bool = True
    risk_violation_enabled: bool = True
    system_alert_enabled: bool = True
    marketing_enabled: bool = False
    daily_summary_enabled: bool = True
    weekly_report_enabled: bool = False
    quiet_hours_start: Optional[str] = Field(None, pattern=r'^([01]\d|2[0-3]):[0-5]\d$')
    quiet_hours_end: Optional[str] = Field(None, pattern=r'^([01]\d|2[0-3]):[0-5]\d$')
    timezone: str = "UTC"
    email_frequency: str = "immediate"
    batch_notifications: bool = False

class UserNotificationSettingsCreate(UserNotificationSettingsBase):
    user_id: UUID

class UserNotificationSettingsResponse(UserNotificationSettingsBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmailQueueBase(BaseModel):
    recipient_email: EmailStr
    recipient_name: Optional[str] = Field(None, max_length=100)
    subject: str = Field(..., max_length=200)
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    sender_email: EmailStr
    sender_name: Optional[str] = Field(None, max_length=100)
    priority: int = 1
    max_retries: int = 3

class EmailQueueCreate(EmailQueueBase):
    template_id: Optional[UUID] = None

class EmailQueueResponse(EmailQueueBase):
    id: UUID
    status: str
    scheduled_for: datetime
    sent_at: Optional[datetime] = None
    delivery_confirmed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    retry_count: int
    message_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# MT5 Account Management Schemas
class MT5AccountConnectRequest(BaseModel):
    mt5_login: str = Field(..., max_length=50)
    mt5_password: str = Field(..., max_length=100)
    server_id: UUID
    is_demo: bool = True

class MT5AccountConnectionResponse(BaseModel):
    account_id: UUID
    status: str
    balance: Decimal = Field(default=0)
    equity: Decimal = Field(default=0)
    error_message: Optional[str] = None
    connected_at: datetime

# Notification Summary Schemas
class NotificationSummary(BaseModel):
    unread_count: int
    total_count: int
    counts_by_type: Dict[str, int]
    counts_by_priority: Dict[str, int]
    counts_by_status: Dict[str, int]

class NotificationStatsRequest(BaseModel):
    user_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    group_by: str = "day"  # day, week, month

class NotificationStatsResponse(BaseModel):
    period: str
    total_sent: int
    total_delivered: int
    delivery_rate: Decimal = Field(default=0)
    average_daily_count: int
    counts_by_type: Dict[str, int]
    counts_by_channel: Dict[str, int]
    details: Optional[List[Dict[str, Any]]] = None
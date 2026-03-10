from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.phase2 import (
    PaymentRepository, RevenueLedgerRepository, 
    AccountRepository, AccountRuleSnapshotRepository,
    ChallengeRepository, ChallengeRuleVersionRepository
)
from app.models.user import User
from app.models.phase2.payment import PaymentStatusEnum, RevenueTypeEnum
from app.models.phase2.account import AccountStatusEnum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import uuid

class PaymentService:
    """Service for payment-related operations"""
    
    @staticmethod
    def create_payment(db: Session, user: User, payment_data: dict) -> dict:
        """Create a new payment"""
        # Verify challenge exists and is active
        challenge = ChallengeRepository.get_challenge_by_id(db, payment_data['challenge_id'])
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found"
            )
        
        if challenge.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge is not available for purchase"
            )
        
        # Create payment record
        payment_record = PaymentRepository.create_payment(db, {
            "user_id": user.id,
            "challenge_id": payment_data['challenge_id'],
            "amount": payment_data['amount'],
            "currency": payment_data.get('currency', 'USD'),
            "payment_method": payment_data['payment_method'],
            "status": PaymentStatusEnum.PENDING
        })
        
        # For simulated payments, we can mark as completed immediately
        if payment_data['payment_method'] == 'simulated':
            PaymentService._process_simulated_payment(db, payment_record)
        
        return {
            "payment_id": payment_record.id,
            "status": payment_record.status,
            "client_secret": payment_record.client_secret,  # For real payment providers
            "amount": payment_record.amount
        }
    
    @staticmethod
    def complete_payment(db: Session, payment_id: UUID, transaction_id: str = None) -> dict:
        """Complete a payment and trigger account creation"""
        payment = PaymentRepository.get_payment_by_id(db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        if payment.status != PaymentStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment is not in pending status"
            )
        
        # Update payment status
        PaymentRepository.update_payment_status(
            db, 
            payment_id, 
            PaymentStatusEnum.COMPLETED,
            transaction_id,
            datetime.utcnow()
        )
        
        # Create revenue ledger entry
        RevenueLedgerRepository.create_revenue_entry(db, {
            "payment_id": payment_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "revenue_type": RevenueTypeEnum.CHALLENGE_SALE
        })
        
        # Create account
        account_data = AccountService.create_account_from_payment(db, payment)
        
        return {
            "payment_id": payment_id,
            "status": PaymentStatusEnum.COMPLETED,
            "account_id": account_data["account_id"],
            "account_number": account_data["account_number"]
        }
    
    @staticmethod
    def _process_simulated_payment(db: Session, payment) -> None:
        """Process simulated payment immediately"""
        # Generate fake transaction ID for simulation
        transaction_id = f"sim_{uuid.uuid4().hex[:12]}"
        
        # Complete the payment
        PaymentService.complete_payment(db, payment.id, transaction_id)
    
    @staticmethod
    def get_user_payments(db: Session, user: User) -> list:
        """Get all payments for a user"""
        payments = PaymentRepository.get_payments_by_user(db, user.id)
        return [payment.to_dict() for payment in payments]

class AccountService:
    """Service for account-related operations"""
    
    @staticmethod
    def create_account_from_payment(db: Session, payment) -> dict:
        """Create account when payment is completed"""
        # Get the latest active rule version for the challenge
        rule_version = ChallengeRuleVersionRepository.get_latest_active_rule_version(
            db, payment.challenge_id
        )
        
        if not rule_version:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No active rule version found for challenge"
            )
        
        # Create account
        account = AccountRepository.create_account(db, {
            "user_id": payment.user_id,
            "payment_id": payment.id,
            "name": f"{payment.challenge.name} Account",
            "starting_balance": payment.amount * Decimal('100'),  # Convert price to account balance
            "current_balance": payment.amount * Decimal('100'),
            "daily_start_balance": payment.amount * Decimal('100'),
            "highest_balance": payment.amount * Decimal('100'),
            "equity": payment.amount * Decimal('100'),
            "status": AccountStatusEnum.PENDING,
            "is_demo": True
        })
        
        # Create rule snapshot
        AccountRuleSnapshotRepository.create_snapshot(db, {
            "account_id": account.id,
            "rule_version_id": rule_version.id,
            "max_daily_loss": rule_version.max_daily_loss,
            "max_total_loss": rule_version.max_total_loss,
            "profit_target": rule_version.profit_target,
            "max_positions": rule_version.max_positions,
            "max_lot_size": rule_version.max_lot_size,
            "allowed_instruments": rule_version.allowed_instruments,
            "trading_hours_start": rule_version.trading_hours_start,
            "trading_hours_end": rule_version.trading_hours_end,
            "snapshot_version": rule_version.version,
            "notes": f"Snapshot created from rule version {rule_version.version}"
        })
        
        return {
            "account_id": account.id,
            "account_number": account.account_number,
            "status": account.status
        }
    
    @staticmethod
    def get_user_accounts(db: Session, user: User) -> list:
        """Get all accounts for a user"""
        accounts = AccountRepository.get_accounts_by_user(db, user.id)
        return [account.to_dict() for account in accounts]
    
    @staticmethod
    def get_account_details(db: Session, user: User, account_id: UUID) -> dict:
        """Get detailed account information"""
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Verify user owns the account
        if account.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this account"
            )
        
        # Get rule snapshot
        rule_snapshot = AccountRuleSnapshotRepository.get_snapshot_by_account(db, account_id)
        
        return {
            "account": account.to_dict(),
            "rule_snapshot": rule_snapshot.to_dict() if rule_snapshot else None
        }
    
    @staticmethod
    def activate_account(db: Session, account_id: UUID) -> dict:
        """Activate an account (set to ACTIVE status)"""
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        if account.status != AccountStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is not in pending status"
            )
        
        # Update account status
        AccountRepository.update_account_status(
            db, 
            account_id, 
            AccountStatusEnum.ACTIVE,
            locked_at=datetime.utcnow()
        )
        
        return {"account_id": account_id, "status": AccountStatusEnum.ACTIVE}
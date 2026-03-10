from sqlalchemy.orm import Session
from app.models.phase2.challenge import Challenge, ChallengeRuleVersion
from app.models.phase2.payment import Payment, RevenueLedger
from app.models.phase2.account import Account, AccountRuleSnapshot
from uuid import UUID
from typing import List, Optional
from decimal import Decimal

class ChallengeRepository:
    """Repository for challenge-related database operations"""
    
    @staticmethod
    def get_challenge_by_id(db: Session, challenge_id: UUID) -> Optional[Challenge]:
        return db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    @staticmethod
    def get_active_challenges(db: Session) -> List[Challenge]:
        return db.query(Challenge).filter(Challenge.status == "active").all()
    
    @staticmethod
    def get_featured_challenges(db: Session) -> List[Challenge]:
        return db.query(Challenge).filter(
            Challenge.status == "active", 
            Challenge.is_featured == True
        ).order_by(Challenge.sort_order).all()
    
    @staticmethod
    def create_challenge(db: Session, challenge_data: dict) -> Challenge:
        db_challenge = Challenge(**challenge_data)
        db.add(db_challenge)
        db.commit()
        db.refresh(db_challenge)
        return db_challenge

class ChallengeRuleVersionRepository:
    """Repository for challenge rule version operations"""
    
    @staticmethod
    def get_rule_version_by_id(db: Session, rule_version_id: UUID) -> Optional[ChallengeRuleVersion]:
        return db.query(ChallengeRuleVersion).filter(ChallengeRuleVersion.id == rule_version_id).first()
    
    @staticmethod
    def get_active_rule_versions_for_challenge(db: Session, challenge_id: UUID) -> List[ChallengeRuleVersion]:
        return db.query(ChallengeRuleVersion).filter(
            ChallengeRuleVersion.challenge_id == challenge_id,
            ChallengeRuleVersion.is_active == True
        ).all()
    
    @staticmethod
    def get_latest_active_rule_version(db: Session, challenge_id: UUID) -> Optional[ChallengeRuleVersion]:
        return db.query(ChallengeRuleVersion).filter(
            ChallengeRuleVersion.challenge_id == challenge_id,
            ChallengeRuleVersion.is_active == True
        ).order_by(ChallengeRuleVersion.created_at.desc()).first()
    
    @staticmethod
    def create_rule_version(db: Session, rule_version_data: dict) -> ChallengeRuleVersion:
        db_rule_version = ChallengeRuleVersion(**rule_version_data)
        db.add(db_rule_version)
        db.commit()
        db.refresh(db_rule_version)
        return db_rule_version

class PaymentRepository:
    """Repository for payment-related database operations"""
    
    @staticmethod
    def get_payment_by_id(db: Session, payment_id: UUID) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()
    
    @staticmethod
    def get_payments_by_user(db: Session, user_id: UUID) -> List[Payment]:
        return db.query(Payment).filter(Payment.user_id == user_id).all()
    
    @staticmethod
    def get_completed_payments_by_user(db: Session, user_id: UUID) -> List[Payment]:
        from app.models.phase2.payment import PaymentStatusEnum
        return db.query(Payment).filter(
            Payment.user_id == user_id,
            Payment.status == PaymentStatusEnum.COMPLETED
        ).all()
    
    @staticmethod
    def create_payment(db: Session, payment_data: dict) -> Payment:
        db_payment = Payment(**payment_data)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    
    @staticmethod
    def update_payment_status(db: Session, payment_id: UUID, status: str, 
                            transaction_id: str = None, processed_at = None) -> Payment:
        payment = PaymentRepository.get_payment_by_id(db, payment_id)
        if payment:
            payment.status = status
            if transaction_id:
                payment.transaction_id = transaction_id
            if processed_at:
                payment.processed_at = processed_at
            db.commit()
            db.refresh(payment)
        return payment

class RevenueLedgerRepository:
    """Repository for revenue ledger operations"""
    
    @staticmethod
    def create_revenue_entry(db: Session, revenue_data: dict) -> RevenueLedger:
        db_revenue = RevenueLedger(**revenue_data)
        db.add(db_revenue)
        db.commit()
        db.refresh(db_revenue)
        return db_revenue
    
    @staticmethod
    def get_revenue_entries_by_payment(db: Session, payment_id: UUID) -> List[RevenueLedger]:
        return db.query(RevenueLedger).filter(RevenueLedger.payment_id == payment_id).all()
    
    @staticmethod
    def mark_revenue_as_processed(db: Session, revenue_id: UUID, processed_at = None) -> RevenueLedger:
        revenue = db.query(RevenueLedger).filter(RevenueLedger.id == revenue_id).first()
        if revenue:
            revenue.is_processed = True
            if processed_at:
                revenue.processed_at = processed_at
            db.commit()
            db.refresh(revenue)
        return revenue

class AccountRepository:
    """Repository for account-related database operations"""
    
    @staticmethod
    def get_account_by_id(db: Session, account_id: UUID) -> Optional[Account]:
        return db.query(Account).filter(Account.id == account_id).first()
    
    @staticmethod
    def get_account_by_number(db: Session, account_number: str) -> Optional[Account]:
        return db.query(Account).filter(Account.account_number == account_number).first()
    
    @staticmethod
    def get_accounts_by_user(db: Session, user_id: UUID) -> List[Account]:
        return db.query(Account).filter(Account.user_id == user_id).all()
    
    @staticmethod
    def get_active_accounts_by_user(db: Session, user_id: UUID) -> List[Account]:
        from app.models.phase2.account import AccountStatusEnum
        return db.query(Account).filter(
            Account.user_id == user_id,
            Account.status.in_([AccountStatusEnum.ACTIVE, AccountStatusEnum.PENDING])
        ).all()
    
    @staticmethod
    def create_account(db: Session, account_data: dict) -> Account:
        # Generate unique account number
        account_number = AccountRepository._generate_account_number(db)
        account_data['account_number'] = account_number
        
        db_account = Account(**account_data)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    
    @staticmethod
    def update_account_balance(db: Session, account_id: UUID, 
                             current_balance: Decimal, equity: Decimal, 
                             highest_balance: Decimal = None) -> Account:
        account = AccountRepository.get_account_by_id(db, account_id)
        if account:
            account.current_balance = current_balance
            account.equity = equity
            if highest_balance and highest_balance > account.highest_balance:
                account.highest_balance = highest_balance
            db.commit()
            db.refresh(account)
        return account
    
    @staticmethod
    def update_account_status(db: Session, account_id: UUID, status: str,
                            locked_by: UUID = None, locked_reason: str = None,
                            locked_at = None) -> Account:
        account = AccountRepository.get_account_by_id(db, account_id)
        if account:
            account.status = status
            if status == "locked":
                account.locked_by = locked_by
                account.locked_reason = locked_reason
                account.locked_at = locked_at
            db.commit()
            db.refresh(account)
        return account
    
    @staticmethod
    def _generate_account_number(db: Session) -> str:
        """Generate unique account number"""
        import random
        while True:
            account_number = f"ACC{random.randint(10000, 99999)}"
            if not AccountRepository.get_account_by_number(db, account_number):
                return account_number

class AccountRuleSnapshotRepository:
    """Repository for account rule snapshot operations"""
    
    @staticmethod
    def create_snapshot(db: Session, snapshot_data: dict) -> AccountRuleSnapshot:
        db_snapshot = AccountRuleSnapshot(**snapshot_data)
        db.add(db_snapshot)
        db.commit()
        db.refresh(db_snapshot)
        return db_snapshot
    
    @staticmethod
    def get_snapshot_by_account(db: Session, account_id: UUID) -> Optional[AccountRuleSnapshot]:
        return db.query(AccountRuleSnapshot).filter(AccountRuleSnapshot.account_id == account_id).first()
# Prop Firm Practice Platform - Risk Engine Specification

##🎯 Core Risk Engine Principles

**Status**: Production Hardening Specification  
**Purpose**: Mathematically precise, concurrency-safe, fraud-resistant risk evaluation  
**Core IP**: The risk engine is the fundamental value proposition of the platform

##🧠 Formalized Drawdown Calculation Logic

### 1️⃣ Daily Drawdown (Reset Daily at 00:00 UTC)
```
daily_drawdown = daily_start_balance - current_equity

Where:
- daily_start_balance = equity at 00:00 UTC each day
- current_equity = latest committed equity value (including floating PnL)
- Reset mechanism: UTC midnight boundary
```

**Implementation Rules**:
-✅ **Equity-based calculation** (not balance-only)
- ✅ **Floating PnL included** in current equity
- ✅ **UTC timezone enforcement** for all calculations
- ✅ **Atomic reset** at daily boundary

### 2️⃣ Maximum Drawdown (Static Model)
```
max_drawdown = initial_balance - lowest_equity_recorded

Where:
- initial_balance = account starting balance at creation
- lowest_equity_recorded = minimum equity value ever recorded
- Static = never resets, lifetime calculation
```

### 3️⃣ Trailing Drawdown (Optional Mode)
```
trailing_drawdown_limit = highest_balance - (highest_balance * max_drawdown_percent)

Where:
- highest_balance = maximum equity achieved since account creation
- max_drawdown_percent = challenge rule parameter (e.g., 5%)
- Dynamic = adjusts as equity grows
```

**Mode Selection**:
- Each challenge rule snapshot defines drawdown mode
- Modes stored in `account_rule_snapshots.drawdown_mode`
- Options: `DAILY`, `MAXIMUM`, `TRAILING`
- No mixing of calculation logic allowed

##⚖️ Risk Rule Precedence Hierarchy

### Priority 1: Hard Violations (Immediate Fail)
1. **Max Total Loss Exceeded**
   - Rule: `current_balance < (starting_balance - max_total_loss)`
   - Action: Immediate account FAIL
   - No recovery possible

2. **Trailing Drawdown Breach**
   - Rule: `current_equity < (highest_balance - trailing_limit)`
   - Action: Immediate account FAIL
   - Only applicable in TRAILING mode

3. **Max Lot Size Breach**
   - Rule: `trade_volume > max_lot_size`
   - Action: Immediate account FAIL
   - Per-trade violation

4. **Copy Trading Detection**
   - Rule: Pattern matching against known copy trading signatures
   - Action: Immediate account FAIL
   - Fraud prevention mechanism

### Priority 2: Daily Violations
1. **Daily Loss Exceeded**
   - Rule: `daily_drawdown > max_daily_loss`
   - Action: Daily violation recorded
   - Account continues unless hard violation occurs

2. **Position Limit Exceeded**
   - Rule: `open_positions > max_positions`
   - Action: Violation recorded
   - Risk score impact

### Priority 3: Soft Warnings
1. **News Trading Violation**
   - Rule: Trades during restricted news periods
   - Action: Warning recorded
   - Educational feedback only

2. **Trading Hour Violation**
   - Rule: Trades outside allowed trading hours
   - Action: Warning recorded
   - Minor risk score impact

### Priority 4: Success Conditions
1. **Profit Target Achievement**
   - Rule: `current_balance >= (starting_balance + profit_target)`
   - Action: Account PASS
   - **Precedence**: Only evaluated if no hard violations present
   - **Conflict Resolution**: If profit target AND violation occur in same evaluation cycle, violation takes precedence

##🔒 Concurrency Protection Mechanisms

### Database-Level Locking
**Option A: SELECT FOR UPDATE**
```sql
BEGIN;
SELECT * FROM accounts WHERE id = ? FOR UPDATE;
-- Risk evaluation logic
UPDATE accounts SET status = ?, ...;
INSERT INTO violations (...);
COMMIT;
```

**Option B: Optimistic Locking**
```python
# Account model includes version column
account_version = account.version
# Evaluation logic
if account.version != account_version:
    # Retry evaluation
    raise ConcurrencyError("Version mismatch, retry required")
```

### Race Condition Prevention
1. **Equity Update First**: MT5 sync always updates equity before risk evaluation
2. **Timestamp Tracking**: 
   - `last_equity_update` in Account model
   - `last_evaluation_at` in Account model
   - Skip evaluation if recently processed
3. **Evaluation Window**: Minimum time between evaluations (configurable)

##🛡️ Evaluation Safeguards

### Idempotent Processing
- **Unique Violation Constraint**: `(account_id, violation_type, evaluation_window)`
- **Status Change Protection**: Check current status before modification
- **Atomic Operations**: Entire evaluation wrapped in database transaction
- **Duplicate Prevention**: No double violation insertion

### Transaction Safety
```python
with db.begin():
    # All operations in single transaction
    account = get_account_with_lock(account_id)
    violations = evaluate_risk(account)
    if violations:
        insert_violations(violations)
        update_account_status(account, new_status)
        insert_status_history(account, violations)
    # Commit only if all operations succeed
```

##🕵️ Fraud Detection Framework

### Structural Hooks (No ML Required)
1. **IP Pattern Analysis**
   - Log IP addresses for all account activities
   - Flag suspicious geographic patterns
   - Multiple account access from same IP

2. **Device Fingerprinting**
   - Browser/user-agent tracking
   - Session pattern analysis
   - Unusual device switching

3. **Trade Pattern Detection**
   - Identical trade timing between users
   - Copy trading signature matching
   - Abnormal correlation patterns

4. **Behavioral Anomalies**
   - Unusual trading hour patterns
   - Sudden strategy changes
   - Risk profile inconsistencies

##📊 Risk Evaluation Cycle

### Standard Evaluation Flow
1. **Pre-check**: Verify account status and last evaluation time
2. **Data Lock**: Acquire appropriate concurrency protection
3. **Metric Calculation**: Compute all risk metrics
4. **Rule Evaluation**: Apply precedence hierarchy
5. **Violation Processing**: Handle violations according to type
6. **Status Update**: Apply account status changes
7. **History Recording**: Log all changes
8. **Notification**: Trigger appropriate alerts
9. **Cleanup**: Release locks and resources

### Error Handling
- **Recovery Mechanisms**: Automatic retry on concurrency conflicts
- **Fallback Logic**: Graceful degradation on system errors
- **Audit Trail**: Complete logging of all evaluation attempts
- **Monitoring**: Real-time health checks and alerts

##📈 Risk Scoring System

### Weighted Violation Scoring
```
risk_score = base_score + 
    (hard_violations * 100) +
    (daily_violations * 25) + 
    (warnings * 5) +
    (time_factor * days_active)

Where:
- base_score = 0 (clean account)
- hard_violations = immediate fail weight
- daily_violations = accumulating penalty
- warnings = minor deduction
- time_factor = account age adjustment
```

### Account Grading
- **A+**: 0 violations, consistent performance
- **A**: Minor warnings only
- **B**: Some daily violations
- **C**: Multiple violations, near limits
- **F**: Hard violation or max loss exceeded

##🔄 Continuous Evaluation

### Automated Scheduling
- **Real-time**: MT5 sync triggers immediate evaluation
- **Periodic**: Scheduled evaluations every X minutes
- **Boundary**: Daily/weekly reset evaluations
- **Manual**: Admin-initiated evaluations

### Performance Monitoring
- **Evaluation Metrics**: Processing time, success rate
- **Accuracy Tracking**: False positive/negative rates
- **System Health**: Resource utilization, error rates
- **Business Impact**: Pass/fail rates, revenue effects

##🔐 Security and Compliance

### Data Integrity
- **Immutable History**: All evaluations permanently recorded
- **Audit Trail**: Complete change logging
- **Access Control**: Role-based evaluation permissions
- **Encryption**: Sensitive data protection

### Regulatory Considerations
- **Fair Processing**: Transparent rule application
- **Appeal Process**: Manual override procedures
- **Documentation**: Complete evaluation records
- **Compliance**: Industry standard practices

---

*This specification ensures the risk engine operates with mathematical precision, concurrency safety, and fraud resistance while maintaining the platform's core value proposition.*
# Prompt: Restructure Services Folder to Match Module Organization

## Objective

Restructure `app/services/` to use nested subfolders matching the pattern used in `app/pages/`, `app/components/`, and `app/states/` for architectural consistency.

## Background

The dashboard state cleanup task is complete:
- `app/states/dashboard/` has been deleted
- Module-specific states exist with proper subfolder organization
- No legacy imports remain

However, the services layer still uses a **flat structure** while all other layers use **nested subfolders**:

**Current (Flat):**
```
app/services/
├── __init__.py
├── compliance_service.py
├── database_service.py
├── emsx_service.py
├── finance_service.py
├── market_data_service.py
├── notification_service.py
├── pnl_service.py
├── portfolio_service.py
├── position_service.py
├── risk_service.py
└── user_service.py
```

**Other Layers (Nested):**
```
app/states/pnl/pnl_state.py
app/pages/pnl/pnl_change_page.py
app/components/pnl/pnl_views.py
```

## Target Structure

```
app/services/
├── __init__.py                     # Re-export all services
├── shared/
│   ├── __init__.py
│   ├── database_service.py         # Shared database operations
│   └── finance_service.py          # Shared finance utilities
├── pnl/
│   ├── __init__.py
│   └── pnl_service.py
├── positions/
│   ├── __init__.py
│   └── position_service.py
├── risk/
│   ├── __init__.py
│   └── risk_service.py
├── compliance/
│   ├── __init__.py
│   └── compliance_service.py
├── portfolio/
│   ├── __init__.py
│   └── portfolio_service.py
├── portfolio_tools/
│   ├── __init__.py
│   └── portfolio_tools_service.py  # Create if needed
├── market_data/
│   ├── __init__.py
│   └── market_data_service.py
├── instruments/
│   ├── __init__.py
│   └── instrument_service.py       # Create if needed
├── events/
│   ├── __init__.py
│   └── events_service.py           # Create if needed
├── operations/
│   ├── __init__.py
│   └── operations_service.py       # Create if needed
├── reconciliation/
│   ├── __init__.py
│   └── reconciliation_service.py   # Create if needed
├── emsx/
│   ├── __init__.py
│   └── emsx_service.py
├── notifications/
│   ├── __init__.py
│   └── notification_service.py
└── user/
    ├── __init__.py
    └── user_service.py
```

## Migration Tasks

### Phase 1: Create Folder Structure

1. Create subdirectories matching module names
2. Create `__init__.py` in each subdirectory

### Phase 2: Move Existing Services

| Current Location | New Location |
|------------------|--------------|
| `services/pnl_service.py` | `services/pnl/pnl_service.py` |
| `services/position_service.py` | `services/positions/position_service.py` |
| `services/risk_service.py` | `services/risk/risk_service.py` |
| `services/compliance_service.py` | `services/compliance/compliance_service.py` |
| `services/portfolio_service.py` | `services/portfolio/portfolio_service.py` |
| `services/market_data_service.py` | `services/market_data/market_data_service.py` |
| `services/emsx_service.py` | `services/emsx/emsx_service.py` |
| `services/notification_service.py` | `services/notifications/notification_service.py` |
| `services/user_service.py` | `services/user/user_service.py` |
| `services/database_service.py` | `services/shared/database_service.py` |
| `services/finance_service.py` | `services/shared/finance_service.py` |

### Phase 3: Update Root `__init__.py`

Update `app/services/__init__.py` to re-export all services for backward compatibility:

```python
# app/services/__init__.py
"""Services layer - all domain services re-exported for convenience."""

from app.services.pnl.pnl_service import PnLService
from app.services.positions.position_service import PositionService
from app.services.risk.risk_service import RiskService
from app.services.compliance.compliance_service import ComplianceService
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.market_data.market_data_service import MarketDataService
from app.services.emsx.emsx_service import EMSXService
from app.services.notifications.notification_service import NotificationService
from app.services.user.user_service import UserService
from app.services.shared.database_service import DatabaseService
from app.services.shared.finance_service import FinanceService

__all__ = [
    "PnLService",
    "PositionService",
    "RiskService",
    "ComplianceService",
    "PortfolioService",
    "MarketDataService",
    "EMSXService",
    "NotificationService",
    "UserService",
    "DatabaseService",
    "FinanceService",
]
```

### Phase 4: Update Imports Throughout Codebase

Search and update imports in state files. Two options:

**Option A (Recommended):** Keep using root `__init__.py` re-exports
```python
# No changes needed - imports from app.services still work
from app.services import PnLService
```

**Option B:** Update to module-specific imports
```python
# More explicit, matches folder structure
from app.services.pnl.pnl_service import PnLService
```

### Phase 5: Create Missing Services (Optional)

The following modules have states but may lack dedicated services:
- `portfolio_tools/portfolio_tools_service.py`
- `instruments/instrument_service.py`
- `events/events_service.py`
- `operations/operations_service.py`
- `reconciliation/reconciliation_service.py`

Review each state file to determine if a dedicated service is needed or if they use existing services.

## Verification

1. Run `uv run reflex run` and verify app compiles
2. Test that all routes load data correctly
3. Verify no import errors in console
4. Check that service methods are callable from states

## Benefits

1. **Consistency**: Services folder matches pages/components/states organization
2. **Discoverability**: Easy to find related files (pnl_state → pnl_service)
3. **Scalability**: Easy to add service-level mixins or utilities per module
4. **Separation**: Shared services (database, finance) clearly separated from domain services

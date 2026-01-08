# State-Service Architecture Analysis

## Executive Summary

This document analyzes all state files under `app/states` to verify they call functions from `app/services`, ensuring clean separation of concerns for the upcoming server-side implementation replacement.

> [!IMPORTANT]
> **Key Finding**: Most state files are **NOT** using the service layer defined in `app/services`. Instead, they use either:
> - Hardcoded mock data directly in the state
> - A separate `finance_service.py` module (not a service class)
> - No external data sources at all

## Current Service Layer Architecture

### Available Service Classes (`app/services/`)

The following service classes are available but **underutilized**:

1. **[DatabaseService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/database_service.py)** - Database connectivity
2. **[MarketDataService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/market_data_service.py)** - Market data fetching
3. **[PositionService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/position_service.py)** - Position data management
4. **[PnLService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/pnl_service.py)** - P&L calculations
5. **[RiskService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/risk_service.py)** - Risk metrics
6. **[EMSXService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/emsx_service.py)** - Bloomberg EMSX orders
7. **[NotificationService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/notification_service.py)** - Notifications
8. **[UserService](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/user_service.py)** - User management

### Additional Service Module

- **[finance_service.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/finance_service.py)** - A module (not a class) using `yfinance` for real-time stock data. This is currently being used by some states.

---

## Detailed State-by-State Analysis

### ✅ States Using Service Layer Correctly

#### 1. [notification_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/notification_state.py)

**Status**: ✅ **GOOD** - Properly uses `NotificationService`

**Service Integration**:
```python
from app.services import NotificationService

async def load_notifications(self):
    service = NotificationService()
    self.notifications = await service.get_notifications(category=category_filter)
```

**Methods using services**:
- `load_notifications()` - Fetches notifications via `NotificationService`
- `mark_all_read()` - Uses `NotificationService.mark_all_as_read()`
- `clear_all()` - Uses `NotificationService.delete_all()`
- `mark_read()` - Uses `NotificationService.mark_as_read()`

**Verdict**: This is the **gold standard** - when you replace server implementation, you only need to update `NotificationService`.

---

### ⚠️ States Using finance_service Module (Not Service Classes)

#### 2. [dashboard_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/dashboard/dashboard_state.py)

**Status**: ⚠️ **PARTIAL** - Uses `finance_service` module, not service classes

**Current Implementation**:
```python
from app.services import finance_service  # This is a module, not a class

async def refresh_prices(self):
    stock_data = finance_service.fetch_multiple_stocks(symbols)
```

**Issues**:
- Hardcoded mock holdings data (lines 33-124)
- Uses `finance_service` module instead of `MarketDataService` or `PositionService`
- Only one method (`refresh_prices()`) fetches external data

**Recommendation**: 
- Replace hardcoded holdings with `PositionService.get_positions()`
- Replace `finance_service` with `MarketDataService.get_realtime_market_data()`

---

#### 3. [watchlist_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/watchlist_state.py)

**Status**: ⚠️ **PARTIAL** - Uses `finance_service` module

**Current Implementation**:
```python
from app.services import finance_service

async def set_search_query(self, query: str):
    data = finance_service.fetch_stock_data(query.upper())

async def refresh_watchlist(self):
    results = finance_service.fetch_multiple_stocks(symbols)
```

**Issues**:
- Hardcoded watchlist data (lines 40-76)
- Uses `finance_service` module instead of `MarketDataService`

**Recommendation**:
- Replace `finance_service` calls with `MarketDataService`

---

#### 4. [research_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/research/research_state.py)

**Status**: ⚠️ **PARTIAL** - Uses `finance_service` module

**Current Implementation**:
```python
from app.services import finance_service

async def set_search_query(self, query: str):
    data = finance_service.fetch_stock_data(query.upper())

async def generate_chart_data(self, symbol: str):
    history = finance_service.fetch_stock_history(symbol, period="1mo")
```

**Issues**:
- Hardcoded stock data (lines 43-142)
- Uses `finance_service` module

**Recommendation**:
- Replace with `MarketDataService`

---

#### 5. [reports_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/reports/reports_state.py)

**Status**: ⚠️ **PARTIAL** - Uses `finance_service` module

**Current Implementation**:
```python
from app.services import finance_service

async def generate_performance_data(self):
    benchmark_data = finance_service.fetch_stock_history("SPY", period=yf_period)
```

**Issues**:
- Hardcoded performance metrics and allocation analysis
- Uses `finance_service` for benchmark only

**Recommendation**:
- Add `PortfolioService` or use `PnLService` for performance data
- Replace `finance_service` with `MarketDataService`

---

### ❌ States NOT Using Any Services

#### 6. [portfolio_dashboard_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/dashboard/portfolio_dashboard_state.py)

**Status**: ❌ **PROBLEMATIC** - 2,769 lines of hardcoded mock data generators

**Current Implementation**:
- Entire file contains mock data generators (e.g., `_generate_pnl_change_data()`, `_generate_pnl_summary_data()`)
- No service integration whatsoever
- Represents the **main portfolio dashboard** with critical data

**Sample Issues**:
```python
def _generate_pnl_change_data() -> list[PnLChangeItem]:
    tickers = ["AAPL", "MSFT", "GOOGL", ...]  # Hardcoded
    # ...mock data generation
```

**Recommendation**: 
- Replace ALL mock generators with service calls:
  - `PositionService.get_positions()` for position data
  - `PnLService.get_pnl_changes()` for P&L data
  - `RiskService.get_delta_changes()` for risk data
  - `MarketDataService` for market data
  - `EMSXService` for order data

---

#### 7. [portfolio_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/portfolio_state.py)

**Status**: ❌ **NO SERVICES**

**Current Implementation**:
- Hardcoded portfolio data (lines 36-108)
- All transaction/dividend data is mock
- No external service calls

**Recommendation**:
- Add `PortfolioService` or extend `PositionService`
- Store transactions in database via `DatabaseService`

---

#### 8. [goals_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/goals_state.py)

**Status**: ❌ **NO SERVICES**

**Current Implementation**:
- Hardcoded goals (lines 27-72)
- All data is local state only

**Recommendation**:
- Add `GoalsService` or extend `UserService`
- Persist goals to database

---

#### 9. [profile_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/user/profile_state.py)

**Status**: ❌ **NO SERVICES**

**Current Implementation**:
- Hardcoded user profile data
- No integration with `UserService` (which exists!)

**Recommendation**:
- Use existing `UserService` for profile management

---

#### 10. [settings_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/user/settings_state.py)

**Status**: ❌ **NO SERVICES**

**Current Implementation**:
- Hardcoded settings
- No persistence

**Recommendation**:
- Use `UserService` for settings persistence

---

#### 11. [notification_pagination_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/notification_pagination_state.py)

**Status**: ❌ **NO SERVICES** (UI helper state only)

**Note**: This is just a pagination helper state, likely acceptable.

---

#### 12. [mobile_nav_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/navigation/mobile_nav_state.py)

**Status**: ❌ **NO SERVICES** (UI helper state only)

**Note**: Navigation state, no data services needed.

---

## Summary Table

| State File | Uses Services? | Service Used | Status |
|------------|---------------|--------------|--------|
| `notification_state.py` | ✅ Yes | `NotificationService` | ✅ GOOD |
| `dashboard_state.py` | ⚠️ Partial | `finance_service` (module) | ⚠️ NEEDS REFACTOR |
| `watchlist_state.py` | ⚠️ Partial | `finance_service` (module) | ⚠️ NEEDS REFACTOR |
| `research_state.py` | ⚠️ Partial | `finance_service` (module) | ⚠️ NEEDS REFACTOR |
| `reports_state.py` | ⚠️ Partial | `finance_service` (module) | ⚠️ NEEDS REFACTOR |
| `portfolio_dashboard_state.py` | ❌ No | None | ❌ CRITICAL |
| `portfolio_state.py` | ❌ No | None | ❌ NEEDS REFACTOR |
| `goals_state.py` | ❌ No | None | ❌ NEEDS REFACTOR |
| `profile_state.py` | ❌ No | None | ❌ NEEDS REFACTOR |
| `settings_state.py` | ❌ No | None | ❌ NEEDS REFACTOR |
| `notification_pagination_state.py` | N/A | N/A | ✅ UI Only |
| `mobile_nav_state.py` | N/A | N/A | ✅ UI Only |

---

## Recommendations for Onboarding

### Priority 1: Critical Refactoring Needed

**[portfolio_dashboard_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/dashboard/portfolio_dashboard_state.py)** (2,769 lines)

This is the **most critical** file. It needs complete refactoring to use:
- `PositionService` for position data
- `PnLService` for P&L data  
- `RiskService` for risk metrics
- `MarketDataService` for market data
- `EMSXService` for order data

### Priority 2: Standardize on Service Classes

Replace all uses of `finance_service` module with proper service classes:
- `dashboard_state.py`
- `watchlist_state.py`
- `research_state.py`
- `reports_state.py`

**Migration Pattern**:
```python
# OLD (using module)
from app.services import finance_service
data = finance_service.fetch_stock_data(symbol)

# NEW (using service class)
from app.services import MarketDataService
service = MarketDataService()
data = await service.get_realtime_market_data([symbol])
```

### Priority 3: Add Service Integration

Add service calls to states with hardcoded data:
- `portfolio_state.py` → Use `PositionService` or create `PortfolioService`
- `goals_state.py` → Use `UserService` or create `GoalsService`
- `profile_state.py` → Use existing `UserService`
- `settings_state.py` → Use existing `UserService`

---

## Action Items for Server Implementation

When replacing the server-side implementation:

### ✅ States Ready for Easy Replacement

1. **[notification_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/notification_state.py)** - Just update `NotificationService`

### ⚠️ States Needing Minor Updates

2. **finance_service users** - Migrate from `finance_service` module to service classes:
   - [dashboard_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/dashboard/dashboard_state.py)
   - [watchlist_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/watchlist_state.py)
   - [research_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/research/research_state.py)
   - [reports_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/reports/reports_state.py)

### ❌ States Needing Major Refactoring

3. **[portfolio_dashboard_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/dashboard/portfolio_dashboard_state.py)** - Complete rewrite needed (2,769 lines of mock data)

4. **Other states** - Add service integration:
   - [portfolio_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/portfolio_state.py)
   - [goals_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/portfolio/goals_state.py)
   - [profile_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/user/profile_state.py)
   - [settings_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/user/settings_state.py)

---

## Conclusion

> [!CAUTION]
> **Current State**: Only 1 out of 12 state files properly uses the service layer architecture. Most states have hardcoded mock data.

> [!IMPORTANT]
> **What This Means**: When you replace the server-side implementation, you'll need to:
> 1. Refactor most state files to use service classes
> 2. Update service class implementations to call real databases/APIs
> 3. The largest effort will be `portfolio_dashboard_state.py` (2,769 lines)

**Best Practice Moving Forward**:
- Follow the pattern in [notification_state.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/notification_state.py)
- Always use service classes, not modules
- Keep all business logic and data access in the service layer
- States should only manage UI state and call services

Refer to the [onboarding.md](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/docs/onboarding.md) Section 7 "Using Services in Reflex States" for implementation patterns.

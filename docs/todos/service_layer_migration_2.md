# Service Layer Migration — Phase 2

> **Status**: Pending  
> **Prerequisite**: [Phase 1](./service_layer_migration.md) ✅ Completed  
> **Date**: 2026-02-10

## Objective

Extract all remaining business/backend service logic from `app/services/` into `pmt_core_pkg/pmt_core/services/`, completing the three-layer pattern:

```
app/states/{domain}/mixins/ → app/services/{domain}/ → pmt_core/services/{domain}/
```

Phase 1 migrated 14 mixins across 4 domains (operations, instruments, reconciliation, events). This phase covers the **remaining 6 domains plus cleanup**.

---

## Current State Audit

### Already Migrated (Phase 1) ✅

| pmt_core Service | app Wrapper | Status |
|---|---|---|
| `OperationsService` | ✅ thin re-export | Done |
| `InstrumentsService` | ✅ thin re-export | Done |
| `ReconciliationService` | ✅ thin re-export | Done |
| `EventCalendarService` | ✅ thin re-export | Done |
| `EventStreamService` | ✅ thin re-export | Done |
| `ReverseInquiryService` | ✅ thin re-export | Done (reference impl) |

### Already in pmt_core (Pre-existing) ✅

| pmt_core Service | app Wrapper | Notes |
|---|---|---|
| `ComplianceService` | ✅ delegates to core | Core delegates to `ComplianceRepository` |
| `PositionService` | ✅ delegates to core | Core delegates to `PositionRepository`; app has mock `get_trade_summary` |
| `PnLService` | ⚠️ partial delegation | Core has `get_pnl_changes`, `get_pnl_summary`, `calculate_daily_pnl`; app has ~400 lines of mock data for `get_pnl_summary`, `get_pnl_by_currency`, `get_pnl_full`, `get_kpi_metrics` |
| `PricingService` | ❌ no app wrapper | Core has skeleton; no app-layer consumer yet |
| `ReportService` | ❌ no app wrapper | Core has skeleton; no app-layer consumer yet |

### Needs Full Migration to pmt_core ❌

| app Service | Lines | Business Logic | pmt_core Exists? |
|---|---|---|---|
| `MarketDataService` | 866 | Yahoo Finance integration, mock data for market data/FX/top movers/trading calendar/market hours/ticker data, historical data with caching | ❌ |
| `RiskService` | 299 | Mock risk metrics (delta changes, risk measures, risk inputs, VaR, gamma, scenarios) | ❌ |
| `EMSXService` | 240 | Mock Bloomberg EMSX order/route management, order CRUD operations | ❌ |
| `PortfolioToolsService` | 380 | Mock portfolio tools data (pay-to-hold, stock borrow, settlement, deal indication, resets, installments, excess amount) | ❌ |
| `UserService` | 294 | Mock user profiles, settings, portfolios, goals CRUD | ❌ |

### Needs Partial Migration ⚠️

| app Service | Issue | What needs moving |
|---|---|---|
| `PnLService` | ~400 lines of mock data in app layer | Move `get_pnl_summary`, `get_pnl_by_currency`, `get_kpi_metrics`, `get_pnl_full` mock data into core `PnLService` |
| `PositionService` | ~20 lines of mock data in app layer | Move `get_trade_summary` mock data into core `PositionService` |
| `DatabaseService` | ~100 lines of compliance mock data | Move `get_restricted_list`, `get_undertakings`, `get_beneficial_ownership`, `get_monthly_exercise_limits` into core `ComplianceService` (via `ComplianceRepository`) |

### App-Layer Only (No Migration Needed) ✅

These services coordinate UI-specific or cross-cutting concerns and should stay in `app/services/`:

| Service | Reason |
|---|---|
| `NotificationService` | Aggregates from `NotificationRegistry`; UI-layer orchestration |
| `NotificationRegistry` | Pub/sub pattern for app-level notification providers |
| `notification_constants.py` | UI enums (`NotificationCategory`, `NotificationIcon`, `NotificationColor`) |
| `PerformanceHeaderService` | Aggregates from `MarketDataService` for header component; UI-layer |
| `finance_service.py` (shared) | Deprecated utility functions; use `MarketDataService` instead |
| `DatabaseService` (core connectivity) | DB connection management stays in app layer; only mock data methods need migration |

---

## Migration Tasks

### Task 1: MarketDataService → pmt_core

**Priority**: High (6 consuming mixins + 1 state)  
**Effort**: Large (866 lines)

#### Consuming mixins (7 consumers):
- `app/states/market_data/mixins/market_data_mixin.py`
- `app/states/market_data/mixins/fx_data_mixin.py`
- `app/states/market_data/mixins/historical_data_mixin.py`
- `app/states/market_data/mixins/ticker_data_mixin.py`
- `app/states/market_data/mixins/trading_calendar_mixin.py`
- `app/states/market_data/mixins/market_hours_mixin.py`
- `app/states/reports/reports_state.py`

#### Methods to migrate to pmt_core:
| Method | Type | Lines |
|---|---|---|
| `get_market_data()` | mock data | ~20 |
| `get_fx_data()` | mock data | ~18 |
| `get_fx_rates()` | mock data | ~28 |
| `get_top_movers()` | mock data | ~165 |
| `get_trading_calendar()` | mock data | ~65 |
| `get_market_hours()` | mock data | ~15 |
| `get_ticker_data()` | mock data | ~18 |
| `get_realtime_market_data()` | wrapper + mock | ~36 |
| `get_historical_data()` | caching + mock | ~80 |

#### Methods that stay in app layer:
| Method | Reason |
|---|---|
| `fetch_stock_data()` | Yahoo Finance integration (external API) |
| `fetch_multiple_stocks()` | Yahoo Finance integration |
| `fetch_stock_history()` | Yahoo Finance integration |
| `fetch_stock_news()` | Yahoo Finance integration |
| `_extract_stock_info()` | Helper for Yahoo Finance |
| `subscribe_to_tickers()` | Bloomberg subscription (app-specific) |
| Notification providers | Uses `NotificationRegistry` (app-layer) |

#### Files to create:
- `pmt_core_pkg/pmt_core/services/market_data/__init__.py`
- `pmt_core_pkg/pmt_core/services/market_data/market_data_service.py`

#### Files to modify:
- `app/services/market_data/market_data_service.py` — delegate mock data methods to core
- `pmt_core_pkg/pmt_core/services/__init__.py` — add re-export
- `app/services/__init__.py` — already exports `MarketDataService`

---

### Task 2: RiskService → pmt_core

**Priority**: High (3 consuming mixins)  
**Effort**: Medium (299 lines)

#### Consuming mixins:
- `app/states/risk/mixins/delta_change_mixin.py`
- `app/states/risk/mixins/risk_measures_mixin.py`
- `app/states/risk/mixins/risk_inputs_mixin.py`

#### Methods to migrate to pmt_core:
| Method | Type | Lines |
|---|---|---|
| `get_delta_changes()` | mock data | ~50 |
| `get_risk_measures()` | mock data | ~45 |
| `get_risk_inputs()` | mock data | ~48 |
| `get_gamma_exposure()` | mock data | ~15 |
| `calculate_portfolio_var()` | mock data | ~27 |
| `get_risk_scenarios()` | mock data | ~15 |

#### Methods that stay in app layer:
| Method | Reason |
|---|---|
| Notification providers | Uses `NotificationRegistry` (app-layer) |

#### Files to create:
- `pmt_core_pkg/pmt_core/services/risk/__init__.py`
- `pmt_core_pkg/pmt_core/services/risk/risk_service.py`

#### Files to modify:
- `app/services/risk/risk_service.py` — delegate to core
- `pmt_core_pkg/pmt_core/services/__init__.py` — add re-export
- `app/services/__init__.py` — already exports `RiskService`

---

### Task 3: PortfolioToolsService → pmt_core

**Priority**: High (8 consuming mixins)  
**Effort**: Medium (380 lines)

#### Consuming mixins:
- `app/states/portfolio_tools/mixins/pay_to_hold_mixin.py`
- `app/states/portfolio_tools/mixins/short_ecl_mixin.py`
- `app/states/portfolio_tools/mixins/stock_borrow_mixin.py`
- `app/states/portfolio_tools/mixins/po_settlement_mixin.py`
- `app/states/portfolio_tools/mixins/deal_indication_mixin.py`
- `app/states/portfolio_tools/mixins/reset_dates_mixin.py`
- `app/states/portfolio_tools/mixins/coming_resets_mixin.py`
- `app/states/portfolio_tools/mixins/cb_installments_mixin.py`
- `app/states/portfolio_tools/mixins/excess_amount_mixin.py`

#### Methods to migrate:
| Method | Type | Lines |
|---|---|---|
| `get_pay_to_hold()` | mock data | ~21 |
| `get_short_ecl()` | mock data | ~18 |
| `get_stock_borrow()` | mock data | ~16 |
| `get_po_settlement()` | mock data | ~19 |
| `get_deal_indication()` | mock data | ~19 |
| `get_reset_dates()` | mock data | ~19 |
| `get_coming_resets()` | mock data | ~17 |
| `get_cb_installments()` | mock data | ~19 |
| `get_excess_amount()` | mock data | ~17 |
| `get_portfolios()` | mock CRUD | ~28 |
| `get_portfolio()` | mock CRUD | ~14 |
| `create_portfolio()` | mock CRUD | ~24 |
| `add_transaction()` | mock CRUD | ~18 |
| `get_transactions()` | mock CRUD | ~15 |
| `add_dividend()` | mock CRUD | ~18 |
| `get_dividends()` | mock CRUD | ~15 |
| `update_portfolio_cash()` | mock CRUD | ~17 |

#### Files to create:
- `pmt_core_pkg/pmt_core/services/portfolio_tools/__init__.py`
- `pmt_core_pkg/pmt_core/services/portfolio_tools/portfolio_tools_service.py`

#### Files to modify:
- `app/services/portfolio_tools/portfolio_tools_service.py` — delegate to core
- `pmt_core_pkg/pmt_core/services/__init__.py` — add re-export

---

### Task 4: EMSXService → pmt_core

**Priority**: Medium (2 consuming mixins)  
**Effort**: Medium (240 lines)

#### Consuming mixins:
- `app/states/emsx/mixins/emsa_order_mixin.py`
- `app/states/emsx/mixins/emsa_route_mixin.py`

#### Methods to migrate:
| Method | Type | Lines |
|---|---|---|
| `get_emsx_orders()` | mock data | ~52 |
| `get_emsx_routes()` | mock data | ~27 |
| `create_emsx_order()` | mock CRUD | ~34 |
| `cancel_emsx_order()` | mock CRUD | ~19 |
| `modify_emsx_order()` | mock CRUD | ~21 |
| `subscribe_to_orders()` | stub | ~14 |

#### Files to create:
- `pmt_core_pkg/pmt_core/services/emsx/__init__.py`
- `pmt_core_pkg/pmt_core/services/emsx/emsx_service.py`

#### Files to modify:
- `app/services/emsx/emsx_service.py` — delegate to core
- `pmt_core_pkg/pmt_core/services/__init__.py` — add re-export

---

### Task 5: PnLService — Complete Migration

**Priority**: Medium (4 consuming mixins)  
**Effort**: Small (move mock data to core)

#### Consuming mixins:
- `app/states/pnl/mixins/pnl_summary_mixin.py`
- `app/states/pnl/mixins/pnl_full_mixin.py`
- `app/states/pnl/mixins/pnl_currency_mixin.py`
- `app/states/pnl/mixins/pnl_change_mixin.py`

#### Methods to add to core `PnLService`:
| Method | Type | Lines |
|---|---|---|
| `get_pnl_summary()` | mock data | ~90 (replace empty return in core) |
| `get_pnl_by_currency()` | mock data | ~75 (new method in core) |
| `get_pnl_full()` | mock data | ~200 (new method in core) |
| `get_kpi_metrics()` | mock data | ~18 (new method in core) |

#### Files to modify:
- `pmt_core_pkg/pmt_core/services/pnl/pnl_service.py` — add missing methods with mock data
- `app/services/pnl/pnl_service.py` — remove inline mock data, delegate to core

---

### Task 6: PositionService — Complete Migration

**Priority**: Low (trade summary only)  
**Effort**: Small

#### What to move:
- `get_trade_summary()` mock data (~20 lines) from `app/services/positions/position_service.py` into core `PositionService`

#### Files to modify:
- `pmt_core_pkg/pmt_core/services/positions/position_service.py` — add `get_trade_summary()`
- `app/services/positions/position_service.py` — delegate to core

---

### Task 7: DatabaseService Compliance Cleanup

**Priority**: Low (already delegated via `ComplianceService`)  
**Effort**: Small

#### What to move:
The compliance mock data methods in `DatabaseService` are already consumed indirectly via `ComplianceRepository`. However, `DatabaseService` still has ~100 lines of these methods that should be removed once `ComplianceRepository` has its own mock data.

| Method in `DatabaseService` | Already in `ComplianceRepository`? |
|---|---|
| `get_restricted_list()` | ✅ Yes (repo has mock) |
| `get_undertakings()` | ✅ Yes (repo has mock) |
| `get_beneficial_ownership()` | ✅ Yes (repo has mock) |
| `get_monthly_exercise_limits()` | ✅ Yes (repo has mock) |

#### Action:
- Remove these 4 methods (~100 lines) from `app/services/shared/database_service.py`
- Verify `ComplianceRepository` still provides data correctly
- `DatabaseService` should then only contain core DB connectivity logic

---

### Task 8: UserService → pmt_core

**Priority**: Low (no consuming mixins currently)  
**Effort**: Small (294 lines)

No state mixins currently consume `UserService` — it may be used directly by state classes or not yet wired up.

#### Methods to migrate:
| Method | Type |
|---|---|
| `get_user_profile()` | mock data |
| `update_user_profile()` | mock CRUD |
| `get_user_settings()` | mock data |
| `update_user_settings()` | mock CRUD |
| `get_user_portfolios()` | mock data |
| `create_portfolio()` | mock CRUD |
| `get_goals()` | mock data |
| `save_goal()` | mock CRUD |
| `delete_goal()` | mock CRUD |

#### Files to create:
- `pmt_core_pkg/pmt_core/services/user/__init__.py`
- `pmt_core_pkg/pmt_core/services/user/user_service.py`

#### Files to modify:
- `app/services/user/user_service.py` — delegate to core
- `pmt_core_pkg/pmt_core/services/__init__.py` — add re-export

---

## Migration Summary

| # | Task | New pmt_core Service | Consuming Mixins | Priority | Effort |
|---|---|---|---|---|---|
| 1 | MarketData | `MarketDataService` | 7 | High | Large |
| 2 | Risk | `RiskService` | 3 | High | Medium |
| 3 | PortfolioTools | `PortfolioToolsService` | 9 | High | Medium |
| 4 | EMSX | `EMSXService` | 2 | Medium | Medium |
| 5 | PnL (complete) | Update existing `PnLService` | 4 | Medium | Small |
| 6 | Positions (complete) | Update existing `PositionService` | 0 | Low | Small |
| 7 | DatabaseService cleanup | N/A (remove dead code) | 0 | Low | Small |
| 8 | User | `UserService` | 0 | Low | Small |

**Total**: ~2,400 lines of business logic to extract, 25+ consuming mixins, 5 new + 2 updated pmt_core services.

---

## Design Decisions

1. **Notification providers stay in app layer** — They use `NotificationRegistry` and `app.ag_grid_constants.GridId`, which are UI-layer concerns. The notification functions (`_get_risk_notifications`, `_get_market_data_notifications`, etc.) remain alongside their app service files.

2. **Yahoo Finance integration stays in app layer** — `MarketDataService.fetch_stock_data/history/news` etc. use `yfinance` which is an external data provider. Only the mock data methods that return static data move to pmt_core.

3. **`PerformanceHeaderService` stays in app layer** — It depends on `MarketDataService` and `app.states.types` (Reflex-specific TypedDicts). It's a UI-layer aggregation service.

4. **`finance_service.py` stays (deprecated)** — Already deprecated in favor of `MarketDataService`. No action needed; will be removed in a future cleanup.

5. **Pattern unchanged** — Same three-layer pattern as Phase 1:
   - Core service in `pmt_core_pkg/pmt_core/services/{domain}/`
   - App wrapper in `app/services/{domain}/`  
   - State mixins import from `app/services/`

---

## Verification Plan

Same approach as Phase 1:
1. Import checks: `uv run python -c "from pmt_core.services import {Service}"`
2. Grep check: `grep -r "DatabaseService" app/states/` should return zero results after all tasks
3. App compilation: `uv run reflex run` — should compile 264/264 with no errors
4. Browser testing: Navigate to all migrated AG Grid pages and verify data renders

# Service Layer Migration: DatabaseService → Domain Services

Migrate all state mixins in `app/states/` that currently call `DatabaseService` directly, refactoring them to call dedicated domain services following the three-layer pattern:

```
app/states/{domain}/mixins/{mixin}.py  →  app/services/{domain}/{service}.py  →  pmt_core_pkg/pmt_core/services/{domain}/{service}.py
```

## Reference Implementation

The `ReverseInquiryService` migration serves as the canonical example:
- Core service: `pmt_core_pkg/pmt_core/services/events/reverse_inquiry_service.py`
- App-layer re-export: `app/services/events/reverse_inquiry_service.py`
- Mixin consumer: `app/states/events/mixins/reverse_inquiry_mixin.py` (imports `from app.services import ReverseInquiryService`)

## What Needs Migrating (16 mixins still calling `DatabaseService`)

| Domain | Mixin | `DatabaseService` method(s) used | Target pmt_core service |
|---|---|---|---|
| **operations** | `daily_procedures_mixin.py` | `get_daily_procedures()` | `OperationsService` (NEW) |
| **operations** | `operation_processes_mixin.py` | `get_operation_processes()` | `OperationsService` (NEW) |
| **instruments** | `stock_screener_mixin.py` | `get_stock_screener()` | `InstrumentsService` (NEW) |
| **instruments** | `ticker_data_mixin.py` | `get_ticker_data()` | `InstrumentsService` (NEW) |
| **instruments** | `special_terms_mixin.py` | `get_special_terms()` | `InstrumentsService` (NEW) |
| **instruments** | `instrument_data_mixin.py` | `get_instrument_data()` | `InstrumentsService` (NEW) |
| **instruments** | `instrument_terms_mixin.py` | `get_instrument_terms()` | `InstrumentsService` (NEW) |
| **reconciliation** | `pps_recon_mixin.py` | `get_pps_recon()` | `ReconciliationService` (NEW) |
| **reconciliation** | `settlement_recon_mixin.py` | `get_settlement_recon()` | `ReconciliationService` (NEW) |
| **reconciliation** | `failed_trades_mixin.py` | `get_failed_trades()` | `ReconciliationService` (NEW) |
| **reconciliation** | `pnl_recon_mixin.py` | `get_pnl_recon()` | `ReconciliationService` (NEW) |
| **reconciliation** | `risk_input_recon_mixin.py` | `get_risk_input_recon()` | `ReconciliationService` (NEW) |
| **events** | `event_calendar_mixin.py` | `get_event_calendar()` | `EventCalendarService` (NEW) |
| **events** | `event_stream_mixin.py` | `get_event_stream()` | `EventStreamService` (NEW) |

## Already Migrated (no changes needed)

compliance, market_data, pnl, positions, risk, portfolio_tools, emsx, events/reverse_inquiry — these already use dedicated services.

## Migration Steps Per Domain

For each domain that needs migration:

1. Create `pmt_core_pkg/pmt_core/services/{domain}/{service_name}.py` — move the mock data methods from `DatabaseService` into the new service class
2. Create `pmt_core_pkg/pmt_core/services/{domain}/__init__.py` — re-export
3. Add to `pmt_core_pkg/pmt_core/services/__init__.py` re-exports
4. Create `app/services/{domain}/{service_name}.py` — thin wrapper re-exporting from pmt_core
5. Update `app/services/{domain}/__init__.py` — re-export
6. Add to `app/services/__init__.py` re-exports
7. Update each mixin in `app/states/{domain}/mixins/` — replace `from app.services import DatabaseService` → `from app.services import {ServiceName}`
8. Remove the corresponding methods from `app/services/shared/database_service.py`

## Design Decisions

- **Group by domain:** one service per domain (e.g. `InstrumentsService` with 5 methods, not 5 separate services)
- **Keep mock data identical** — just move it to the new service, no logic changes
- **Compliance check:** the compliance mixins (`restricted_list`, `undertakings`, `beneficial_ownership`, `monthly_exercise_limits`) currently call `ComplianceService` which wraps `DatabaseService` internally — check if `ComplianceService` also needs its mock data moved from `DatabaseService` to `pmt_core_pkg`
- **End state:** after all migrations, `DatabaseService` should only contain database connectivity methods (`get_connection`, `execute_query`, `execute_stored_proc`, `test_connection`) — all mock data methods should be removed

## Verification

After each domain migration, run `reflex run` and confirm the app compiles without errors. Search for remaining `DatabaseService` references in `app/states/` to track progress.

> [!NOTE]
> **Status: ✅ Archived** — 2026-02-19
> C1, C2, I1, I4 resolved. I2 (mock data audit) and I3 (type alignment) tracked in `service_layer_migration_2.md`.

# Pre-Integration Review: Reflex Python Backend

Comprehensive review of the `app/` and `pmt_core_pkg/pmt_core/` layers before real backend integration.

---

## Executive Summary

The architecture is **well-designed** — dual-package separation, mixin-based state management, thin service adapters, and proper TypedDict deduplication are solid foundations. There are **2 critical issues** and **4 important improvements** identified. C1 is resolved; C2 and I1–I4 remain.

---

## 🚨 Critical Issues (Must Fix)

### ~~C1. Inline Imports in Exception Handlers~~ ✅ RESOLVED

Fixed via automated script — 69 `import logging` + 32 `import random` moved to module level across 47 files.

---

### C2. Field Name Typos Between UI Types and Core Models 🔴

Critical typos in UI TypedDicts that will cause **silent data loss** when real data flows through:

| UI Type (app/states) | UI Field | Core Model (pmt_core) | Core Field | Impact |
|---|---|---|---|---|
| `RiskMeasureItem` | `national` | `RiskRecord` | `notional` | 💥 Silent key miss |
| `RiskMeasureItem` | `national_used` | `RiskRecord` | `notional_used` | 💥 Silent key miss |
| `RiskMeasureItem` | `national_current` | `RiskRecord` | `notional_current` | 💥 Silent key miss |
| `RestrictedListItem` | `in_emdx` | `ComplianceRecord` | `in_emsx` | 💥 Silent key miss |
| `DeltaChangeItem` | `pos_g` | `RiskRecord` | `pos_gamma` | 💥 Silent key miss |
| `StockPositionItem` | `position_location` | `PositionRecord` | `pos_loc` | 💥 Silent key miss |

Additionally, `RiskInputItem` has the same 3 `national` → `notional` typos.

**Fix**: Rename UI TypedDict fields to match core model field names. Update column definitions and mock data generators accordingly.

---

## ⚠️ Important Improvements (Should Fix)

### I1. Service Instantiation Pattern ✅ RESOLVED

**Scope**: **86+ instantiations** across all mixins — every method call created `service = XxxService()`.

**Fix**: Created `app/services/registry.py` — `ServiceRegistry` with `@cached_property` accessors for all 17 services. Refactored 52 files to use `services.xxx.method()` pattern. Zero remaining per-call instantiations.

---

### I2. Mock Data Audit — TODO Inventory

**77+ TODO comments** across 17 service/repository files. Breakdown by category:

| Category | Count | Example Files |
|---|---|---|
| `Replace with DB query` | 30+ | pnl_service, reconciliation_service, portfolio_tools_service |
| `Replace mock data` | 8 | user_service, risk_service, operations_service |
| `Implement logic` | 10 | report_service (5), risk_service (2), bond_pricer, warrant_pricer |
| `Update database` | 5 | notification_service (3), user_service (2) |
| `Replace with orchestration` | 2 | operations_service |

Mock data currently lives in repositories (compliance, positions, pnl, etc.) — good separation. The `mock_mode` toggle in `DatabaseRepository` supports seamless transition.

---

### I3. Type Alignment Analysis

**Architecture**: UI uses per-view TypedDicts (e.g., `PnLChangeItem`, `PnLFullItem`), core uses single union records (e.g., `PnLRecord`). The mapping is **intentional** — UI types are projections of core records.

**Field name typos** are promoted to C2 (critical). Additional structural mismatches:
- UI types use plain `str` everywhere; core uses `Optional[str]` — no runtime issue since mock data always populates, but real DB data with NULLs may cause TypedDict validation warnings
- `ComplianceRecord` is a single union type; UI splits into 4 TypedDicts (`RestrictedListItem`, `UndertakingItem`, `BeneficialOwnershipItem`, `MonthlyExerciseLimitItem`) — this is correct design but needs careful field mapping

**Recommendation**: Fix C2 typos first, then add explicit `Optional` annotations to UI types for nullable fields.

---

### I4. Repository Interface Design ✅ RESOLVED

**Fix**: Created `pmt_core/repositories/protocols.py` with 6 `@runtime_checkable` Protocol interfaces. Updated type hints in `PnLService`, `PositionService`, and `ComplianceService` from concrete to Protocol types. Remaining 3 services (Operations, Events, Recon) have protocols ready for when repository DI is wired.

---

## ✅ What's Already Good

| Area | Status | Notes |
|------|--------|-------|
| **Dual-package separation** | ✅ Solid | `app/` for UI, `pmt_core/` for business logic |
| **Background task pattern** | ✅ Correct | All 34 mixins use `while True` + `async with self` — matches [official Reflex docs](https://reflex.dev/docs/events/background-events/) |
| **Exception hierarchy** | ✅ Complete | 6 exception types with rich metadata, re-exported cleanly |
| **TypedDict deduplication** | ✅ Done | Per-module types with backward-compatible re-exports |
| **Mixin architecture** | ✅ Clean | ~50 mixins with consistent patterns |
| **Service adapter pattern** | ✅ Working | `app/services/` → thin re-exports from `pmt_core` |
| **State patterns** | ✅ Consistent | `is_loading`, `error`, `last_updated`, `auto_refresh` on every mixin |
| **AG Grid factory** | ✅ Mature | Standard factory, toolbar, cell flash, column persistence |
| **Notification system** | ✅ Complete | Pub/Sub registry, cross-module navigation |
| **Documentation** | ✅ Extensive | `AGENTS.md`, `docs/index.md`, milestone checklists, prompt templates |
| **`.env.example`** | ✅ Exists | All required env vars documented |
| **Editable install** | ✅ Working | `pmt_core` via `uv` workspace with editable path |
| **`rxconfig.py`** | ✅ Production-ready | Redis state manager, configurable ports, reverse proxy support |

---

## 📋 Pre-Integration Checklist

### Phase 0: Critical Fixes (Before Any Integration)

- [x] **C1**: Move inline imports to module level in all mixins

### Phase 1: Infrastructure Readiness

- [x] **I1**: Audit service instantiation scope (86+ per-call instantiations found)
- [x] **I2**: Audit all `TODO: Replace with DB query` in `pmt_core` (77+ TODOs inventoried)
- [x] **I3**: Verify field name alignment (6 critical typos found → promoted to C2)
- [x] **I4**: Audit repository interfaces (0/8 have Protocol/ABC)
- [x] **C2**: Fix field name typos in UI TypedDicts (9 renames across 8 files)
- [x] Implement singleton service pattern or connection pooling
- [x] Define Protocol interfaces for each repository
- [ ] Verify database connectivity (`ODBC Driver 17`, connection string)
- [ ] Add connection pooling configuration

### Phase 2: Integration Swap

- [ ] Replace mock data in repositories with real DB queries
- [ ] Ensure `asyncio.to_thread` wrapping for blocking DB calls
- [ ] Add integration tests with test database
- [ ] Update `app/states/*/types.py` if field names change

### Phase 3: Stability Verification

- [ ] Run `uv run reflex run` — app starts without errors
- [ ] Navigate all 11 module pages
- [ ] Check browser console for JS errors
- [ ] Check terminal for Python exceptions
- [ ] Verify auto-refresh ticking works on all grids
- [ ] Run `uv run pytest` — all tests pass

---

## Existing Milestone Status

The following milestone documents already exist but are **largely unchecked**:

| Document | Items | Status |
|----------|-------|--------|
| [milestone-0-preparation-checklist.md](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/docs/todos/milestone-0-preparation-checklist.md) | 43 items | Not Started |
| [milestone-1-pre-integration-checklist.md](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/docs/todos/milestone-1-pre-integration-checklist.md) | 38 items | In Progress (mostly BLOCKED) |

> [!NOTE]
> This review supplements (not replaces) those milestones.


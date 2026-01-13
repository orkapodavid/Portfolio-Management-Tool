# Design: Dashboard State Cleanup and Migration to Route-Based Architecture

## Objective

Clean up the `app/states/dashboard/` folder by migrating all domain-specific logic to their corresponding module state files following the route-based architecture pattern. After migration, delete the entire dashboard state folder to eliminate redundancy and maintain a single source of truth.

## Background

The application currently has a hybrid architecture:

1. **Legacy Dashboard States**: `app/states/dashboard/` contains:
   - `portfolio_dashboard_state.py` - 955 lines with 11 mixins for all modules
   - `dashboard_state.py` - 232 lines for portfolio-specific logic
   - Individual module states: `pnl_state.py`, `positions_state.py`, `risk_state.py`, etc.
   - `mixins/` folder with 12 mixin files

2. **Modern Module States**: Separate state folders already exist:
   - `app/states/pnl/` - PnL-specific state
   - `app/states/positions/` - Positions-specific state
   - `app/states/market_data/` - Market data state
   - `app/states/portfolio/` - Portfolio state
   - Others: notifications, research, reports, user, navigation

3. **Route Structure**: The application uses route-based navigation (implemented) but still relies on dashboard state for data and UI coordination.

## Problem Statement

Current issues with the dashboard folder:

1. **Duplication**: Logic exists in both `app/states/dashboard/` and module-specific state folders
2. **Tight Coupling**: 25+ files import from `app.states.dashboard`
3. **Unclear Ownership**: Uncertain which state file owns which data
4. **Maintenance Burden**: Changes require updating multiple locations
5. **Anti-Pattern**: Violates Reflex best practice of flat, focused state structure
6. **Migration Incomplete**: Route-based architecture partially implemented but dashboard state still exists

## Design Principles

Following the patterns from `generic_prompts.md`:

1. **Flat State Structure**: One state class per module, directly inheriting from `rx.State`
2. **Separation of Concerns**: Each module state handles only its own data and logic
3. **Service Layer Integration**: States delegate to services, contain no business logic
4. **Mixin Pattern for Sub-pages**: Use mixins within each module for sub-page logic
5. **Single Source of Truth**: Each piece of data lives in exactly one place

## Target Architecture

### State Organization Pattern

```
app/states/
├── pnl/
│   ├── pnl_state.py              # Main state inheriting mixins
│   ├── mixins/
│   │   ├── change_mixin.py       # PnL Change logic
│   │   ├── summary_mixin.py      # PnL Summary logic
│   │   ├── currency_mixin.py     # PnL Currency logic
│   │   └── full_mixin.py         # PnL Full logic
│   └── types.py                  # PnLChangeItem, PnLSummaryItem, etc.
├── positions/
│   ├── positions_state.py        # Main state
│   ├── mixins/
│   │   ├── stock_mixin.py
│   │   ├── warrant_mixin.py
│   │   ├── bond_mixin.py
│   │   └── trade_summary_mixin.py
│   └── types.py
├── risk/
│   ├── risk_state.py
│   ├── mixins/
│   │   ├── delta_change_mixin.py
│   │   ├── risk_measures_mixin.py
│   │   └── risk_inputs_mixin.py
│   └── types.py
├── compliance/
│   ├── compliance_state.py
│   ├── mixins/
│   │   ├── restricted_list_mixin.py
│   │   ├── undertakings_mixin.py
│   │   ├── beneficial_ownership_mixin.py
│   │   └── monthly_exercise_limit_mixin.py
│   └── types.py
├── portfolio_tools/
│   ├── portfolio_tools_state.py
│   ├── mixins/               # 9 mixins for sub-pages
│   └── types.py
├── instruments/
│   ├── instruments_state.py
│   ├── mixins/
│   └── types.py
├── events/
│   ├── events_state.py
│   ├── mixins/
│   └── types.py
├── operations/
│   ├── operations_state.py
│   ├── mixins/
│   └── types.py
├── reconciliation/
│   ├── reconciliation_state.py
│   ├── mixins/
│   └── types.py
├── emsx/
│   ├── emsx_state.py
│   ├── mixins/
│   └── types.py
├── navigation/
│   └── navigation_state.py   # Global nav state
└── ui/
    └── ui_state.py           # Shared UI state
```

### Data Ownership Map

| Data Category | Current Location | Target Location | Rationale |
|---------------|------------------|-----------------|-----------|
| PnL data (change, summary, currency, full) | `dashboard/mixins/pnl_mixin.py` | `pnl/pnl_state.py` + mixins | Domain-specific, route-specific |
| Position data (stocks, warrants, bonds) | `dashboard/mixins/positions_mixin.py` | `positions/positions_state.py` + mixins | Domain-specific |
| Risk data (delta, measures, inputs) | `dashboard/mixins/risk_mixin.py` | `risk/risk_state.py` + mixins | Domain-specific |
| Compliance data | `dashboard/mixins/compliance_mixin.py` | `compliance/compliance_state.py` + mixins | Domain-specific |
| Market data | `dashboard/mixins/market_data_mixin.py` | `market_data/market_data_state.py` | Already exists, migrate remaining |
| Portfolio Tools data | `dashboard/mixins/portfolio_tools_mixin.py` | `portfolio_tools/portfolio_tools_state.py` | Domain-specific |
| Instruments data | `dashboard/mixins/instruments_mixin.py` | `instruments/instruments_state.py` | Domain-specific |
| Events data | `dashboard/mixins/events_mixin.py` | `events/events_state.py` | Domain-specific |
| Operations data | `dashboard/mixins/operations_mixin.py` | `operations/operations_state.py` | Domain-specific |
| Reconciliation data | `dashboard/mixins/reconciliation_mixin.py` | `reconciliation/reconciliation_state.py` | Domain-specific |
| EMSX/Orders data | `dashboard/mixins/emsx_mixin.py` | `emsx/emsx_state.py` (new folder) | Domain-specific |
| Portfolio holdings, allocation | `dashboard/dashboard_state.py` | `portfolio/portfolio_state.py` | Already exists, migrate remaining |
| Navigation (active module, subtabs) | `dashboard/portfolio_dashboard_state.py` | `navigation/navigation_state.py` | Cross-cutting concern |
| UI state (sidebar, pagination, sorting) | `dashboard/mixins/ui_mixin.py` | `ui/ui_state.py` (new folder) | Shared across all modules |
| KPI metrics | `dashboard/portfolio_dashboard_state.py` | `pnl/pnl_state.py` | KPIs derived from PnL data |
| Top movers | `dashboard/portfolio_dashboard_state.py` | `market_data/market_data_state.py` | Market data-derived |
| Notifications | `dashboard/portfolio_dashboard_state.py` | `notifications/notifications_state.py` | Already exists, migrate remaining |

## Migration Strategy

### Phase 1: Analysis and Preparation

**Action Items:**

1. Audit all imports from `app.states.dashboard` across the codebase (25+ files identified)
2. Document current dependencies and data flows
3. Verify existing module state structures
4. Create missing module folders and state files
5. Identify shared utilities and helper functions

**Files to Audit:**
- All component files (17 files)
- All page files (8+ files)
- `app.py` route configuration

### Phase 2: Create Target State Structure

**Create Missing Module State Folders:**

1. **EMSX/Orders State** (new):
   - Create `app/states/emsx/`
   - Create `emsx_state.py` with `EMSXMixin` content
   - Create `types.py` with `EMSAOrderItem`, `EMSXRouteItem`

2. **Reconciliation State** (extend existing):
   - Verify `app/states/reconciliation/` exists
   - Create `reconciliation_state.py` if missing
   - Create mixins for each sub-page
   - Create `types.py` with recon types

3. **Compliance State** (new):
   - Create `app/states/compliance/`
   - Create `compliance_state.py`
   - Create mixins for 4 sub-pages
   - Create `types.py`

4. **Risk State** (new):
   - Create `app/states/risk/`
   - Create `risk_state.py`
   - Create mixins for delta, measures, inputs
   - Create `types.py`

5. **Portfolio Tools State** (new):
   - Create `app/states/portfolio_tools/`
   - Create `portfolio_tools_state.py`
   - Create 9 mixins (one per sub-page)
   - Create `types.py`

6. **Instruments State** (extend existing):
   - Extend `app/states/instruments/`
   - Create mixins if needed
   - Migrate types

7. **Events State** (new):
   - Create `app/states/events/`
   - Create `events_state.py`
   - Create mixins for 3 sub-pages
   - Create `types.py`

8. **Operations State** (new):
   - Create `app/states/operations/`
   - Create `operations_state.py`
   - Create mixins for 2 sub-pages
   - Create `types.py`

9. **Shared UI State** (new):
   - Create `app/states/ui/`
   - Create `ui_state.py` with pagination, sorting, filtering logic
   - Extract from `ui_mixin.py`

10. **Navigation State** (extend existing):
    - Extend `app/states/navigation/navigation_state.py`
    - Add module navigation logic
    - Add subtab tracking

### Phase 3: Migrate Data and Logic Module by Module

For each module, follow this pattern:

**Module State Template:**

```
# app/states/{module}/{module}_state.py
import reflex as rx
from app.states.{module}.mixins.{subpage1}_mixin import {Subpage1}Mixin
from app.states.{module}.mixins.{subpage2}_mixin import {Subpage2}Mixin
from app.services import {Module}Service

class {Module}State(
    {Subpage1}Mixin,
    {Subpage2}Mixin,
    rx.State,
):
    """Main {Module} state with all sub-page mixins."""
    
    # Module-level shared state
    active_{module}_tab: str = "Default"
    is_loading_{module}: bool = False
    {module}_error: str = ""
    
    async def on_load(self):
        """Load data when module first accessed."""
        await self.load_{subpage1}_data()
    
    # Coordination methods if needed
    async def refresh_active_tab(self):
        """Refresh data for currently active tab."""
        if self.active_{module}_tab == "{Subpage1}":
            await self.load_{subpage1}_data()
        elif self.active_{module}_tab == "{Subpage2}":
            await self.load_{subpage2}_data()
```

**Sub-page Mixin Template:**

```
# app/states/{module}/mixins/{subpage}_mixin.py
import reflex as rx
from app.states.{module}.types import {DataItem}
from app.services import {Service}

class {Subpage}Mixin(rx.State, mixin=True):
    """State mixin for {Subpage} sub-page."""
    
    # State variables
    {subpage}_data: list[{DataItem}] = []
    is_loading_{subpage}: bool = False
    {subpage}_error: str = ""
    
    # Data loading
    async def load_{subpage}_data(self):
        """Load data when page accessed."""
        self.is_loading_{subpage} = True
        self.{subpage}_error = ""
        try:
            service = {Service}()
            self.{subpage}_data = await service.get_{subpage}()
        except Exception as e:
            self.{subpage}_error = str(e)
        finally:
            self.is_loading_{subpage} = False
    
    # Computed vars
    @rx.var(cache=True)
    def filtered_{subpage}_data(self) -> list[{DataItem}]:
        """Apply filters to data."""
        return self.{subpage}_data
```

**Migration Order (by priority):**

1. **PnL Module** (already has state folder, extend it)
2. **Positions Module** (already has state folder, extend it)
3. **Market Data Module** (already has state folder, extend it)
4. **Risk Module** (create new)
5. **Compliance Module** (create new)
6. **Portfolio Tools Module** (create new)
7. **Instruments Module** (extend existing)
8. **Events Module** (create new)
9. **Operations Module** (create new)
10. **Reconciliation Module** (create new)
11. **EMSX/Orders Module** (create new)
12. **Shared UI State** (create new)
13. **Navigation State** (extend existing)

### Phase 4: Update Component Imports

For each component and page file importing from `app.states.dashboard`:

**Pattern - Before:**
```python
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState

def my_component():
    return rx.box(
        rx.text(PortfolioDashboardState.pnl_change_list)
    )
```

**Pattern - After:**
```python
from app.states.pnl.pnl_state import PnLState

def my_component():
    return rx.box(
        rx.text(PnLState.pnl_change_list)
    )
```

**Files to Update (25+ files):**

| File Path | Current Import | New Import |
|-----------|---------------|------------|
| `app/app.py` | `PortfolioDashboardState` | Keep for global nav, remove others |
| `components/pnl/pnl_views.py` | `PortfolioDashboardState` | `PnLState` |
| `components/positions/positions_views.py` | `PortfolioDashboardState` | `PositionsState` |
| `components/risk/risk_views.py` | `PortfolioDashboardState` | `RiskState` |
| `components/compliance/compliance_views.py` | `PortfolioDashboardState` | `ComplianceState` |
| `components/portfolio_tools/portfolio_tools_views.py` | `PortfolioDashboardState` | `PortfolioToolsState` |
| `components/market_data/market_data_views.py` | `PortfolioDashboardState` | `MarketDataState` |
| `components/instruments/instrument_views.py` | `PortfolioDashboardState` | `InstrumentsState` |
| `components/emsa/emsa_views.py` | `PortfolioDashboardState` | `EMSXState` |
| `components/operations/operations_views.py` | `PortfolioDashboardState` | `OperationsState` |
| `components/reconciliation/reconciliation_views.py` | `PortfolioDashboardState` | `ReconciliationState` |
| `components/portfolio/allocation_chart.py` | `DashboardState` | `PortfolioState` |
| `components/portfolio/holdings_table.py` | `DashboardState` | `PortfolioState` |
| `components/portfolio/summary_cards.py` | `DashboardState` | `PortfolioState` |
| `components/shared/contextual_workspace.py` | `PortfolioDashboardState` | `NavigationState` + `UIState` |
| `components/shared/notification_sidebar.py` | `PortfolioDashboardState` | `NotificationsState` |
| `components/shared/performance_header.py` | `PortfolioDashboardState` | `PnLState` (for KPIs) |
| `components/shared/top_navigation.py` | `PortfolioDashboardState` | `NavigationState` |
| All page files in `/pages` | Module-specific | Module-specific state |

**Cross-State Access Pattern:**

When a component needs data from multiple states, use `get_state()`:

```python
from app.states.pnl.pnl_state import PnLState
from app.states.positions.positions_state import PositionsState

class MyComponentState(rx.State):
    async def load_combined_data(self):
        pnl_state = await self.get_state(PnLState)
        positions_state = await self.get_state(PositionsState)
        
        # Use data from both states
        combined = pnl_state.pnl_change_list + positions_state.positions
```

### Phase 5: Update Route Configuration

Update `app/app.py` route handlers to use module-specific states:

**Pattern - Before:**
```python
app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    on_load=[
        PnLState.load_pnl_change_data,
        lambda: PnLState.set_pnl_subtab("PnL Change"),
        lambda: PortfolioDashboardState.set_module("PnL"),  # Dashboard state call
    ],
)
```

**Pattern - After:**
```python
app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    on_load=[
        PnLState.load_pnl_change_data,
        lambda: PnLState.set_pnl_subtab("PnL Change"),
        lambda: NavigationState.set_active_module("PnL"),  # Navigation state call
    ],
)
```

**Changes:**
- Replace `PortfolioDashboardState` with module-specific states for data loading
- Replace dashboard navigation calls with `NavigationState` calls
- Remove global `on_load` handler from index route if no longer needed

### Phase 6: Handle Shared State

**Navigation State (`app/states/navigation/navigation_state.py`):**

Responsibilities:
- Track active module
- Track active subtab per module
- Module configuration (icons, categories, subtabs)
- Navigation event handlers

Migration source: `portfolio_dashboard_state.py` lines 178-341

**UI State (`app/states/ui/ui_state.py`):**

Responsibilities:
- Pagination (page, page size, page controls)
- Sorting (column, direction)
- Filtering (search, date, auto-refresh)
- UI toggles (sidebar, mobile menu, export dropdown)
- Selected row tracking

Migration source: `ui_mixin.py` and `portfolio_dashboard_state.py` lines 181-208

**Shared Pattern:**

Components access shared state alongside module state:

```python
from app.states.pnl.pnl_state import PnLState
from app.states.ui.ui_state import UIState
from app.states.navigation.navigation_state import NavigationState

def pnl_table():
    return rx.box(
        # Data from PnL state
        rx.data_table(PnLState.pnl_change_list),
        # Pagination from UI state
        rx.hstack(
            rx.button("Previous", on_click=UIState.prev_page),
            rx.text(f"Page {UIState.current_page}"),
            rx.button("Next", on_click=UIState.next_page),
        )
    )
```

### Phase 7: Migrate Type Definitions

Move type definitions from `dashboard/types.py` to module-specific `types.py` files:

**Type Ownership:**

| Type | Current Location | Target Location |
|------|------------------|-----------------|
| `PositionItem`, `StockPositionItem`, etc. | `dashboard/types.py` | `positions/types.py` |
| `PnLChangeItem`, `PnLSummaryItem`, etc. | `dashboard/types.py` | `pnl/types.py` |
| `DeltaChangeItem`, `RiskMeasureItem`, etc. | `dashboard/types.py` | `risk/types.py` |
| `RestrictedListItem`, `UndertakingItem`, etc. | `dashboard/types.py` | `compliance/types.py` |
| `PayToHoldItem`, `ShortECLItem`, etc. | `dashboard/types.py` | `portfolio_tools/types.py` |
| `MarketDataItem`, `FXDataItem`, etc. | `dashboard/types.py` | `market_data/types.py` |
| `InstrumentDataItem`, `TickerDataItem`, etc. | `dashboard/types.py` | `instruments/types.py` |
| `EventCalendarItem`, `EventStreamItem`, etc. | `dashboard/types.py` | `events/types.py` |
| `DailyProcedureItem`, `OperationProcessItem` | `dashboard/types.py` | `operations/types.py` |
| `PPSReconItem`, `SettlementReconItem`, etc. | `dashboard/types.py` | `reconciliation/types.py` |
| `EMSAOrderItem` | `dashboard/types.py` | `emsx/types.py` |
| `KPIMetric`, `TopMover` | `dashboard/types.py` | `shared/types.py` (new) |
| `NotificationItem` | `dashboard/types.py` | `notifications/types.py` |
| `Holding`, `AssetAllocation`, `Performer` | `dashboard_state.py` | `portfolio/types.py` |

**Shared Types:**

Create `app/states/shared/types.py` for types used across multiple modules:
- `KPIMetric` (used in header, from PnL data)
- `TopMover` (used in sidebar, from market data)
- Common pagination/sorting types if needed

### Phase 8: Delete Dashboard Folder

After all migrations are complete and tested:

**Pre-deletion Checklist:**

1. ✓ All 25+ imports updated to use new state locations
2. ✓ All component files use module-specific states
3. ✓ All page files use module-specific states
4. ✓ All route handlers use module-specific states
5. ✓ All type definitions moved to module-specific types.py
6. ✓ No references to `app.states.dashboard` in entire codebase
7. ✓ Application runs without errors
8. ✓ All routes accessible and functional
9. ✓ Data loads correctly in all views
10. ✓ Navigation works as expected

**Deletion Command:**

```bash
# Verify no imports remain
grep -r "from app.states.dashboard" app/

# If clean, delete the folder
rm -rf app/states/dashboard/
```

**Files to be Deleted:**

```
app/states/dashboard/
├── mixins/
│   ├── __init__.py
│   ├── compliance_mixin.py       → compliance/compliance_state.py
│   ├── emsx_mixin.py            → emsx/emsx_state.py
│   ├── events_mixin.py          → events/events_state.py
│   ├── instruments_mixin.py     → instruments/instruments_state.py
│   ├── market_data_mixin.py     → market_data/market_data_state.py
│   ├── operations_mixin.py      → operations/operations_state.py
│   ├── pnl_mixin.py             → pnl/pnl_state.py
│   ├── portfolio_tools_mixin.py → portfolio_tools/portfolio_tools_state.py
│   ├── positions_mixin.py       → positions/positions_state.py
│   ├── reconciliation_mixin.py  → reconciliation/reconciliation_state.py
│   ├── risk_mixin.py            → risk/risk_state.py
│   └── ui_mixin.py              → ui/ui_state.py
├── __init__.py
├── compliance_state.py          → compliance/compliance_state.py
├── dashboard_state.py           → portfolio/portfolio_state.py
├── emsx_state.py                → emsx/emsx_state.py
├── market_data_state.py         → market_data/market_data_state.py
├── pnl_state.py                 → pnl/pnl_state.py
├── portfolio_dashboard_state.py → ELIMINATED (was aggregator)
├── positions_state.py           → positions/positions_state.py
├── reconciliation_state.py      → reconciliation/reconciliation_state.py
├── risk_state.py                → risk/risk_state.py
└── types.py                     → module-specific types.py files
```

Total: 12 mixin files + 10 state files + 2 metadata files = **24 files deleted**

## Testing Strategy

After each phase, validate:

### Unit-Level Testing

1. **State Integrity**: Each state loads data correctly
2. **Mixin Composition**: Main state inherits all mixin functionality
3. **Service Integration**: States call services correctly
4. **Computed Vars**: Cached computed vars return correct values

### Integration Testing

1. **Component Rendering**: All components render with new state references
2. **Event Handlers**: All user interactions work (clicks, searches, pagination)
3. **Navigation**: Module switching updates state correctly
4. **Data Flow**: Cross-state access via `get_state()` works

### System Testing

1. **Route Access**: All routes return 200 status
2. **Deep Linking**: Direct URL navigation loads correct data
3. **Browser Navigation**: Back/forward buttons work correctly
4. **Data Loading**: `on_load` handlers execute correctly for each route
5. **Performance**: No degradation in load times or responsiveness

### Manual Testing Checklist

For each module route:

- [ ] Route accessible via URL
- [ ] Data loads without errors
- [ ] Pagination works
- [ ] Sorting works
- [ ] Filtering/search works
- [ ] Sub-tabs render correctly
- [ ] Navigation highlights active module
- [ ] No console errors

## Risk Assessment and Mitigation

### High Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Import errors causing runtime failures | High | Medium | Incremental migration, test each module |
| Data not loading in views | High | Medium | Verify service integration, test on_load |
| Reflex compilation errors | High | Low | Follow mixin pattern exactly, avoid boolean event handlers |
| Breaking shared components | High | Medium | Create backward-compatible imports initially |

### Medium Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Missed imports in obscure files | Medium | Medium | Use grep to audit, compile after each change |
| Type definition duplication | Medium | Low | Centralize shared types, clear ownership |
| Navigation state conflicts | Medium | Low | Single navigation state, clear API |
| Performance degradation | Medium | Low | Use cached computed vars, lazy loading |

### Low Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| File path typos | Low | Medium | IDE autocomplete, careful review |
| Incomplete mixin migration | Low | Low | Template-driven approach, checklist |
| Documentation gaps | Low | Medium | Document as you go, update AGENTS.md |

## Implementation Checklist

### Phase 1: Analysis
- [ ] Audit all 25+ files importing from dashboard
- [ ] Document current data flows
- [ ] Identify all module states needed
- [ ] Map type definitions to modules

### Phase 2: Structure
- [ ] Create missing module state folders
- [ ] Create main state files
- [ ] Create mixin files for sub-pages
- [ ] Create module-specific types.py files
- [ ] Create shared UI state
- [ ] Extend navigation state

### Phase 3: Migration (per module)
- [ ] PnL module
- [ ] Positions module
- [ ] Market Data module
- [ ] Risk module
- [ ] Compliance module
- [ ] Portfolio Tools module
- [ ] Instruments module
- [ ] Events module
- [ ] Operations module
- [ ] Reconciliation module
- [ ] EMSX module

### Phase 4: Update Imports
- [ ] Update component files (17 files)
- [ ] Update page files (8+ files)
- [ ] Update app.py route handlers
- [ ] Update shared components

### Phase 5: Routes
- [ ] Update all on_load handlers
- [ ] Test each route individually
- [ ] Verify navigation state updates

### Phase 6: Shared State
- [ ] Migrate navigation logic
- [ ] Migrate UI state (pagination, sorting)
- [ ] Update components using shared state

### Phase 7: Types
- [ ] Move types to module-specific files
- [ ] Create shared types file
- [ ] Update imports

### Phase 8: Cleanup
- [ ] Run full application test
- [ ] Verify no dashboard imports
- [ ] Delete dashboard folder
- [ ] Update documentation

## Success Criteria

1. **Zero References**: No `from app.states.dashboard` in codebase
2. **All Routes Work**: Every route accessible and functional
3. **Data Loads**: All views display data correctly
4. **Navigation Works**: Module switching and subtabs functional
5. **No Errors**: Application runs without console errors
6. **Performance Maintained**: No degradation in load times
7. **Dashboard Folder Deleted**: `app/states/dashboard/` no longer exists
8. **Tests Pass**: All manual and integration tests pass
9. **Clean Architecture**: Flat state structure, clear ownership
10. **Documentation Updated**: AGENTS.md reflects new structure

## Estimated Timeline

| Phase | Estimated Time | Dependencies |
|-------|----------------|--------------|
| Phase 1: Analysis | 4-6 hours | None |
| Phase 2: Structure | 6-8 hours | Phase 1 |
| Phase 3: Migration | 24-32 hours | Phase 2 (8-12 hours × 3 modules avg) |
| Phase 4: Update Imports | 8-12 hours | Phase 3 |
| Phase 5: Routes | 4-6 hours | Phase 4 |
| Phase 6: Shared State | 6-8 hours | Phase 5 |
| Phase 7: Types | 4-6 hours | Phase 6 |
| Phase 8: Cleanup | 4-6 hours | Phase 7 |
| **Total** | **60-84 hours** | Sequential |

For 11 modules:
- **Small modules** (2-3 sub-pages): 8-10 hours each
- **Medium modules** (4-5 sub-pages): 10-12 hours each
- **Large modules** (6-9 sub-pages): 12-16 hours each

## Post-Migration Benefits

1. **Clarity**: Clear ownership of data and logic
2. **Maintainability**: Changes isolated to single module
3. **Testability**: Each state independently testable
4. **Performance**: Lazy loading, only load active module data
5. **Scalability**: Easy to add new modules following pattern
6. **Reflex Best Practices**: Flat structure, focused substates
7. **Developer Experience**: Easier to navigate, understand codebase
8. **Route-Based Navigation**: Full benefits of URL-based navigation
9. **No Duplication**: Single source of truth for all data
10. **Clean Architecture**: Separation of concerns throughout

## Appendix A: Module Mapping Reference

Quick reference for where to find logic after migration:

| Functionality | Before | After |
|---------------|--------|-------|
| PnL Change data | `dashboard/mixins/pnl_mixin.py` | `pnl/mixins/change_mixin.py` |
| Stock Positions | `dashboard/mixins/positions_mixin.py` | `positions/mixins/stock_mixin.py` |
| Delta Change | `dashboard/mixins/risk_mixin.py` | `risk/mixins/delta_change_mixin.py` |
| Restricted List | `dashboard/mixins/compliance_mixin.py` | `compliance/mixins/restricted_list_mixin.py` |
| Pay-To-Hold | `dashboard/mixins/portfolio_tools_mixin.py` | `portfolio_tools/mixins/pay_to_hold_mixin.py` |
| Market Data | `dashboard/mixins/market_data_mixin.py` | `market_data/market_data_state.py` |
| EMSX Orders | `dashboard/mixins/emsx_mixin.py` | `emsx/emsx_state.py` |
| Event Calendar | `dashboard/mixins/events_mixin.py` | `events/mixins/event_calendar_mixin.py` |
| Operations | `dashboard/mixins/operations_mixin.py` | `operations/operations_state.py` |
| Reconciliation | `dashboard/mixins/reconciliation_mixin.py` | `reconciliation/reconciliation_state.py` |
| Module Navigation | `dashboard/portfolio_dashboard_state.py` | `navigation/navigation_state.py` |
| Pagination/Sorting | `dashboard/mixins/ui_mixin.py` | `ui/ui_state.py` |
| Portfolio Holdings | `dashboard/dashboard_state.py` | `portfolio/portfolio_state.py` |
| KPI Metrics | `dashboard/portfolio_dashboard_state.py` | `pnl/pnl_state.py` |
| Notifications | `dashboard/portfolio_dashboard_state.py` | `notifications/notifications_state.py` |

## Appendix B: Migration Prompt Template

Use this prompt for each module migration:

---

**Prompt: Migrate {Module} State from Dashboard to Module-Specific State**

Context: I'm migrating the dashboard state folder to follow route-based architecture. We need to move {Module} logic from `app/states/dashboard/mixins/{module}_mixin.py` to `app/states/{module}/{module}_state.py`.

Tasks:
1. Review current {Module} mixin at `app/states/dashboard/mixins/{module}_mixin.py`
2. Identify all sub-pages for {Module} (check MODULE_SUBTABS in portfolio_dashboard_state.py)
3. Create `app/states/{module}/{module}_state.py` with main state class
4. Create `app/states/{module}/mixins/` folder
5. Create one mixin per sub-page with load_*_data methods
6. Move type definitions from `dashboard/types.py` to `{module}/types.py`
7. Update service integration
8. Follow the pattern from generic_prompts.md Phase 2 and 3
9. Test that state compiles and loads data correctly

Sub-pages for {Module}:
- {List sub-pages here}

Type definitions to migrate:
- {List TypedDict types here}

Service to use: `{Module}Service`

Expected outcome:
- Clean, focused state following Reflex best practices
- Each sub-page has its own mixin
- Main state inherits all mixins
- Data loads via on_load handlers
- No references to dashboard state

---



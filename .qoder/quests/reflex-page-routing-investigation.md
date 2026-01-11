# Reflex Page Routing Investigation & Implementation Guide

## Problem Statement

The Portfolio Management Tool currently has a routing architecture issue where:

1. **Dashboard modules and tabs do not have unique URL routes** - All dashboard modules (Market Data, Positions, PnL, Risk, etc.) and their subtabs are accessible from the root path `/` only
2. **URL does not update when switching tabs** - Clicking on different modules or subtabs in the top navigation does not change the browser URL
3. **No deep linking support** - Users cannot bookmark or share links to specific dashboard views
4. **Separate portfolio pages work correctly** - Pages like `/portfolios`, `/watchlist`, `/research` have proper routing through sidebar navigation

## Current Architecture Analysis

### Root Index Page Structure

The main application entry point at `/` renders a monolithic dashboard:

| Component | Purpose | State Management |
|-----------|---------|------------------|
| `index()` function | Root page component at `/` route | Entry point in `app.py` |
| `top_navigation()` | Module selector (Market Data, Positions, PnL, etc.) | Uses `PortfolioDashboardState.set_module()` |
| `contextual_workspace()` | Dynamic content area with subtabs | Uses `PortfolioDashboardState.set_subtab()` |
| `performance_header()` | KPI metrics display | Reads from `PortfolioDashboardState` |
| `notification_sidebar()` | Notifications panel | Reads from `PortfolioDashboardState` |

### Current State-Based Navigation

Navigation currently relies entirely on **client-side state changes**:

```
User clicks module → set_module(module_name) → active_module state changes → 
contextual_workspace() re-renders → displays new content
```

**Key State Variables:**
- `active_module: str` - Current selected module (e.g., "Market Data", "Positions")
- `_active_subtabs: dict[str, str]` - Maps module to active subtab
- `MODULE_SUBTABS: dict[str, list[str]]` - Defines available subtabs per module

**State Event Handlers:**
- `set_module(module_name: str)` - Changes active module
- `set_subtab(subtab_name: str)` - Changes active subtab within current module

### Separate Page Routes (Working Correctly)

These pages are **properly registered** with dedicated routes:

| Page | Route | State | Navigation Method |
|------|-------|-------|-------------------|
| Dashboard (index) | `/` | `PortfolioDashboardState` | Top navigation modules |
| Portfolios | `/portfolios` | `PortfolioState` | Sidebar link |
| Watchlist | `/watchlist` | `WatchlistState` | Sidebar link |
| Research | `/research` | `ResearchState` | Sidebar link |
| Reports | `/reports` | `ReportsState` | Sidebar link |
| Goals | `/goals` | `GoalsState` | Sidebar link |
| Profile | `/profile` | `ProfileState` | Sidebar link |
| Notifications | `/notifications` | `NotificationState` | Sidebar link |
| Settings | `/settings` | `SettingsState` | Sidebar link |

## Root Cause Analysis

### Why Dashboard Tabs Don't Have Routes

The dashboard architecture was designed as a **Single Page Application (SPA) pattern** where:

1. **All modules share one route** (`/`) - Only the root index page is registered
2. **Module switching is state-based** - Clicking tabs triggers `set_module()` which updates component state, not URL
3. **Content is conditionally rendered** - `contextual_workspace()` uses `rx.match()` to display content based on `active_module` state
4. **No route registration for modules** - Modules are not added via `app.add_page()`, they're just UI components

### Architectural Decision Context

This pattern was likely chosen because:

- **Shared layout** - All modules share the same header, navigation, and sidebar
- **Complex state coordination** - Modules need access to shared dashboard state
- **Performance** - Avoids full page reloads when switching views
- **Initial simplicity** - Easier to implement as a single stateful component

However, this creates problems:

- Users cannot bookmark specific dashboard views
- Browser back/forward buttons don't work as expected
- No URL-based state restoration
- Difficult to implement analytics or tracking per module
- Violates user expectations for web navigation

## Solution Design

### Strategic Approach

Transform the dashboard from a **state-based SPA** to a **route-based multi-page application** while preserving the shared layout and state coordination benefits.

### Architecture Decision: Hybrid Routing Pattern

Implement a **hierarchical route structure** where:

1. **Each dashboard module becomes a dedicated route**
2. **Subtabs use URL query parameters or path segments**
3. **Shared components remain consistent across routes**
4. **State management coordinates across all dashboard routes**

### Proposed URL Structure

#### URL-to-File Structure Alignment

**Design Principle:** URLs should mirror the file system structure for easy navigation and investigation.

**Pattern:** `/{module}/{subtab}` maps to `app/pages/{module}/{subtab}_page.py`

#### Module-Level Routes

| Module | Route | File Path | State Class |
|--------|-------|-----------|-------------|
| Market Data | `/market-data/*` | `app/pages/market_data/` | `MarketDataState` |
| Positions | `/positions/*` | `app/pages/positions/` | `PositionsState` |
| PnL | `/pnl/*` | `app/pages/pnl/` | `PnLState` |
| Risk | `/risk/*` | `app/pages/risk/` | `RiskState` |
| Recon | `/recon/*` | `app/pages/recon/` | `ReconState` |
| Compliance | `/compliance/*` | `app/pages/compliance/` | `ComplianceState` |
| Portfolio Tools | `/portfolio-tools/*` | `app/pages/portfolio_tools/` | `PortfolioToolsState` |
| Instruments | `/instruments/*` | `app/pages/instruments/` | `InstrumentsState` |
| Events | `/events/*` | `app/pages/events/` | `EventsState` |
| Operations | `/operations/*` | `app/pages/operations/` | `OperationsState` |
| Orders | `/orders/*` | `app/pages/orders/` | `OrdersState` |

#### Subtab Route Examples

**PnL Module:**

| URL | File | State Mixin | Component |
|-----|------|-------------|----------|
| `/pnl/pnl-change` | `app/pages/pnl/pnl_change_page.py` | `PnLChangeMixin` | `pnl_change_table()` |
| `/pnl/pnl-full` | `app/pages/pnl/pnl_full_page.py` | `PnLFullMixin` | `pnl_full_table()` |
| `/pnl/pnl-summary` | `app/pages/pnl/pnl_summary_page.py` | `PnLSummaryMixin` | `pnl_summary_table()` |
| `/pnl/pnl-currency` | `app/pages/pnl/pnl_currency_page.py` | `PnLCurrencyMixin` | `pnl_currency_table()` |

**Positions Module:**

| URL | File | State Mixin | Component |
|-----|------|-------------|----------|
| `/positions/positions` | `app/pages/positions/positions_page.py` | `PositionsMixin` | `positions_table()` |
| `/positions/stock-position` | `app/pages/positions/stock_position_page.py` | `StockPositionMixin` | `stock_position_table()` |
| `/positions/warrant-position` | `app/pages/positions/warrant_position_page.py` | `WarrantPositionMixin` | `warrant_position_table()` |
| `/positions/bond-positions` | `app/pages/positions/bond_positions_page.py` | `BondPositionsMixin` | `bond_position_table()` |
| `/positions/trade-summary` | `app/pages/positions/trade_summary_page.py` | `TradeSummaryMixin` | `trade_summary_table()` |

**URL Design Rationale:**

1. **Direct File Mapping:** URL `/pnl/pnl-change` → File `app/pages/pnl/pnl_change_page.py`
2. **State Organization:** Each module has a main state class that inherits from all its subtab mixins
3. **Easy Navigation:** Developers can find files by looking at the URL structure
4. **Clear Hierarchy:** Module → Subtab relationship is explicit in both URL and file system
5. **Consistent Naming:** URL slugs use kebab-case, files use snake_case (standard Python convention)

### Implementation Strategy

#### Phase 1: Route Registration

Create dedicated page functions for each dashboard module:

| Task | Description | Files to Create |
|------|-------------|-----------------|
| Create module pages | One page function per module | `app/pages/dashboard/market_data_page.py`, `pnl_page.py`, etc. |
| Register routes | Add each page with `app.add_page()` | Modify `app/app.py` |
| Define base layout | Shared layout function for all dashboard pages | `app/components/dashboard/dashboard_layout.py` |

#### Phase 2: Navigation Updates

Update navigation components to use route-based links:

| Component | Change Required | Implementation Approach |
|-----------|----------------|-------------------------|
| `top_navigation.py` | Replace `on_click=set_module()` with `href="/dashboard/{module}"` | Use `rx.link()` instead of `rx.button()` |
| `contextual_workspace.py` | Update subtab buttons to change URL query param | Use `rx.link()` with query string |
| Event handlers | Update `set_module()` to use `rx.redirect()` | Redirect instead of state change |

#### Phase 3: State Synchronization

Synchronize URL with state to maintain backward compatibility:

| Mechanism | Purpose | Implementation |
|-----------|---------|----------------|
| Route detection | Set `active_module` based on current URL | Use `on_load` event handler |
| Query param parsing | Set `active_subtab` from URL query string | Parse route parameters |
| State-to-URL sync | Update URL when state changes programmatically | Use `rx.redirect()` in event handlers |

#### Phase 4: Backward Compatibility

Ensure existing functionality continues to work:

| Feature | Compatibility Concern | Solution |
|---------|----------------------|----------|
| Root path `/` | Currently shows dashboard | Redirect to `/dashboard/market-data` |
| Direct state access | Components using `PortfolioDashboardState.active_module` | Keep state variables, sync with routes |
| Mobile menu | Currently uses state switches | Update to use route links |
| Generate menu | Context-dependent actions | Read module from route context |

## Implementation Details

### State Mixin Architecture (Following Reflex Best Practices)

#### Why Use Mixins for Subtabs

Based on `reflex-state-structure.mdc` best practices:

**Advantages:**
1. **Code Reusability:** Share functionality across similar views
2. **Separation of Concerns:** Each subtab's logic is isolated
3. **Composition Over Inheritance:** Build complex states from simple mixins
4. **Maintainability:** Easy to modify or extend individual subtabs
5. **Performance:** Load only data needed for active subtab
6. **Testability:** Test each mixin independently

**Pattern:**
```
Subtab Mixin (pnl_change_mixin.py)
    ↓
Module State (pnl_state.py) inherits all subtab mixins
    ↓
Page (pnl_change_page.py) uses module state
```

#### Mixin Definition Pattern

**Location:** `app/states/{module}/mixins/{subtab}_mixin.py`

**Template:**

```python
# app/states/pnl/mixins/pnl_change_mixin.py
import reflex as rx
from app.states.pnl.types import PnLChangeItem
from app.services import PnLService

class PnLChangeMixin(rx.State, mixin=True):
    """State mixin for PnL Change subtab.
    
    Contains all state and logic specific to the PnL Change view.
    This mixin is combined with other subtab mixins in PnLState.
    """
    
    # ===== State Variables =====
    pnl_change_list: list[PnLChangeItem] = []
    is_loading_pnl_change: bool = False
    pnl_change_error: str = ""
    
    # Filters specific to this view
    pnl_change_search: str = ""
    pnl_change_sort_column: str = ""
    pnl_change_sort_direction: str = "asc"
    
    # ===== Data Loading =====
    async def load_pnl_change_data(self):
        """Load PnL Change data from service.
        
        Called via on_load when /pnl/pnl-change page is accessed.
        """
        self.is_loading_pnl_change = True
        self.pnl_change_error = ""
        
        try:
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_change()
        except Exception as e:
            self.pnl_change_error = str(e)
            import logging
            logging.exception(f"Error loading PnL change data: {e}")
        finally:
            self.is_loading_pnl_change = False
    
    # ===== Event Handlers =====
    def set_pnl_change_search(self, query: str):
        """Update search filter."""
        self.pnl_change_search = query
    
    def sort_pnl_change(self, column: str):
        """Toggle sort for column."""
        if self.pnl_change_sort_column == column:
            self.pnl_change_sort_direction = (
                "desc" if self.pnl_change_sort_direction == "asc" else "asc"
            )
        else:
            self.pnl_change_sort_column = column
            self.pnl_change_sort_direction = "asc"
    
    # ===== Computed Vars =====
    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        """Apply search and sort to PnL change data."""
        data = self.pnl_change_list
        
        # Apply search
        if self.pnl_change_search:
            query = self.pnl_change_search.lower()
            data = [
                item for item in data
                if query in item.get("ticker", "").lower()
            ]
        
        # Apply sort
        if self.pnl_change_sort_column:
            data = sorted(
                data,
                key=lambda x: x.get(self.pnl_change_sort_column, ""),
                reverse=(self.pnl_change_sort_direction == "desc")
            )
        
        return data
```

#### Module State Composition

**Location:** `app/states/{module}/{module}_state.py`

**Template:**

```python
# app/states/pnl/pnl_state.py
import reflex as rx

# Import all subtab mixins
from app.states.pnl.mixins.pnl_change_mixin import PnLChangeMixin
from app.states.pnl.mixins.pnl_full_mixin import PnLFullMixin
from app.states.pnl.mixins.pnl_summary_mixin import PnLSummaryMixin
from app.states.pnl.mixins.pnl_currency_mixin import PnLCurrencyMixin

# Import types for type hints
from app.states.pnl.types import (
    PnLChangeItem,
    PnLFullItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)

class PnLState(
    PnLChangeMixin,      # /pnl/pnl-change logic
    PnLFullMixin,        # /pnl/pnl-full logic
    PnLSummaryMixin,     # /pnl/pnl-summary logic
    PnLCurrencyMixin,    # /pnl/pnl-currency logic
    rx.State,            # Base state
):
    """Main PnL module state.
    
    Inherits from all PnL subtab mixins to provide unified interface.
    Each mixin handles one subtab's state and logic.
    
    This follows Reflex best practices for state organization:
    - Flat structure (all mixins at same level)
    - Separation of concerns (one mixin per subtab)
    - Code reusability (mixins can be shared)
    - Performance (only load active subtab's data)
    """
    
    # ===== Module-Level State =====
    # Shared across all PnL subtabs
    
    active_pnl_subtab: str = "PnL Change"
    pnl_date_filter: str = ""
    pnl_currency_filter: str = "USD"
    
    # ===== Module-Level Event Handlers =====
    
    def set_pnl_date_filter(self, date: str):
        """Set date filter for all PnL views."""
        self.pnl_date_filter = date
        # Could trigger reload of active subtab if needed
    
    def set_pnl_currency_filter(self, currency: str):
        """Set currency filter for all PnL views."""
        self.pnl_currency_filter = currency
    
    async def refresh_active_subtab(self):
        """Refresh data for currently active subtab."""
        if self.active_pnl_subtab == "PnL Change":
            await self.load_pnl_change_data()
        elif self.active_pnl_subtab == "PnL Full":
            await self.load_pnl_full_data()
        elif self.active_pnl_subtab == "PnL Summary":
            await self.load_pnl_summary_data()
        elif self.active_pnl_subtab == "PnL Currency":
            await self.load_pnl_currency_data()
    
    # ===== Route Synchronization =====
    
    async def sync_from_route(self):
        """Sync state from URL path.
        
        Called via on_load to set active_pnl_subtab based on current route.
        """
        current_path = self.router.page.path
        
        # Parse: "/pnl/pnl-change" -> "PnL Change"
        if "/pnl-change" in current_path:
            self.active_pnl_subtab = "PnL Change"
        elif "/pnl-full" in current_path:
            self.active_pnl_subtab = "PnL Full"
        elif "/pnl-summary" in current_path:
            self.active_pnl_subtab = "PnL Summary"
        elif "/pnl-currency" in current_path:
            self.active_pnl_subtab = "PnL Currency"
```

**Key Architecture Decisions:**

1. **Flat Mixin Inheritance:** All mixins inherit from `rx.State` directly, not from each other
2. **No Deep Hierarchy:** Avoids performance issues from loading parent states
3. **Module State as Coordinator:** Main state class coordinates between subtabs
4. **Independent Data Loading:** Each mixin loads its own data when accessed
5. **Shared Module State:** Common filters/settings in main state class

#### Benefits of This Architecture

**Performance:**
- Only active subtab's data is loaded
- Flat structure = faster state loading
- Computed vars cached per subtab

**Maintainability:**
- One file per subtab's logic
- Easy to find and modify code
- Clear separation of concerns

**Scalability:**
- Add new subtabs by creating new mixin
- No changes to existing mixins
- Module state grows linearly

**Testability:**
- Test each mixin independently
- Mock service layer
- Isolated unit tests

### File Structure Changes

**Design Philosophy:** Organize files to mirror URL structure with proper state mixin pattern.

#### Complete Directory Structure

```
app/
├── pages/
│   ├── market_data/
│   │   ├── __init__.py
│   │   ├── market_data_page.py          # /market-data/market-data
│   │   ├── fx_data_page.py              # /market-data/fx-data
│   │   ├── historical_data_page.py      # /market-data/historical-data
│   │   ├── trading_calendar_page.py     # /market-data/trading-calendar
│   │   └── market_hours_page.py         # /market-data/market-hours
│   ├── positions/
│   │   ├── __init__.py
│   │   ├── positions_page.py            # /positions/positions
│   │   ├── stock_position_page.py       # /positions/stock-position
│   │   ├── warrant_position_page.py     # /positions/warrant-position
│   │   ├── bond_positions_page.py       # /positions/bond-positions
│   │   └── trade_summary_page.py        # /positions/trade-summary
│   ├── pnl/
│   │   ├── __init__.py
│   │   ├── pnl_change_page.py           # /pnl/pnl-change
│   │   ├── pnl_full_page.py             # /pnl/pnl-full
│   │   ├── pnl_summary_page.py          # /pnl/pnl-summary
│   │   └── pnl_currency_page.py         # /pnl/pnl-currency
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── delta_change_page.py         # /risk/delta-change
│   │   ├── risk_measures_page.py        # /risk/risk-measures
│   │   ├── risk_inputs_page.py          # /risk/risk-inputs
│   │   ├── pricer_warrant_page.py       # /risk/pricer-warrant
│   │   └── pricer_bond_page.py          # /risk/pricer-bond
│   └── ... (other modules follow same pattern)
│
├── states/
│   ├── market_data/
│   │   ├── __init__.py
│   │   ├── market_data_state.py         # Main MarketDataState class
│   │   ├── mixins/
│   │   │   ├── __init__.py
│   │   │   ├── market_data_mixin.py     # MarketDataMixin (subtab)
│   │   │   ├── fx_data_mixin.py         # FXDataMixin (subtab)
│   │   │   ├── historical_data_mixin.py # HistoricalDataMixin (subtab)
│   │   │   ├── trading_calendar_mixin.py
│   │   │   └── market_hours_mixin.py
│   │   └── types.py                     # TypedDict definitions
│   ├── positions/
│   │   ├── __init__.py
│   │   ├── positions_state.py           # Main PositionsState class
│   │   ├── mixins/
│   │   │   ├── __init__.py
│   │   │   ├── positions_mixin.py       # PositionsMixin (subtab)
│   │   │   ├── stock_position_mixin.py  # StockPositionMixin (subtab)
│   │   │   ├── warrant_position_mixin.py
│   │   │   ├── bond_positions_mixin.py
│   │   │   └── trade_summary_mixin.py
│   │   └── types.py
│   ├── pnl/
│   │   ├── __init__.py
│   │   ├── pnl_state.py                 # Main PnLState class
│   │   ├── mixins/
│   │   │   ├── __init__.py
│   │   │   ├── pnl_change_mixin.py      # PnLChangeMixin (subtab)
│   │   │   ├── pnl_full_mixin.py        # PnLFullMixin (subtab)
│   │   │   ├── pnl_summary_mixin.py     # PnLSummaryMixin (subtab)
│   │   │   └── pnl_currency_mixin.py    # PnLCurrencyMixin (subtab)
│   │   └── types.py
│   └── ... (other modules follow same pattern)
│
├── components/
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── module_layout.py             # Shared layout wrapper
│   │   ├── top_navigation.py
│   │   ├── performance_header.py
│   │   └── notification_sidebar.py
│   ├── pnl/
│   │   ├── __init__.py
│   │   └── ... (PnL view components)
│   ├── positions/
│   │   ├── __init__.py
│   │   └── ... (Positions view components)
│   └── ... (other module components)
│
└── services/
    ├── __init__.py
    ├── pnl_service.py
    ├── position_service.py
    ├── market_data_service.py
    └── ... (other services)
```

#### State Organization Pattern

**Per-Subtab Mixin Pattern (Following Reflex Best Practices):**

Each subtab has its own mixin containing:
- Subtab-specific state variables
- Data loading methods
- Event handlers for that view
- Computed vars for that view

**Module State Composition:**

Each module's main state class:
- Inherits from ALL its subtab mixins
- Inherits from `rx.State`
- Provides unified interface
- Handles cross-subtab coordination

**Example Structure (PnL Module):**

```
PnLState
    ├─ Inherits: PnLChangeMixin
    ├─ Inherits: PnLFullMixin  
    ├─ Inherits: PnLSummaryMixin
    ├─ Inherits: PnLCurrencyMixin
    └─ Inherits: rx.State
```

**Rationale:**

1. **URL-to-File Mapping:** Clear 1:1 relationship for debugging
2. **State Isolation:** Each subtab's logic is self-contained in its mixin
3. **Code Reusability:** Mixins can be shared if needed
4. **Reflex Best Practice:** Follows mixin pattern from `reflex-state-structure.mdc`
5. **Performance:** Only load data for active subtab via `on_load` handlers
6. **Maintainability:** Easy to find and modify subtab-specific logic
7. **Scalability:** Add new subtabs by creating new mixin + page file

### Module Page Pattern

Each subtab page follows a consistent structure with proper state mixin integration.

#### Subtab Page Structure

**File:** `app/pages/pnl/pnl_change_page.py`

**Components:**

1. **Imports**
   - Module state class (main state with all mixins)
   - Shared module layout
   - Subtab-specific view component

2. **Page Function**
   - Defines the route endpoint
   - Wraps content in module layout
   - Passes module and subtab metadata

3. **On-Load Handler**
   - Registered with route
   - Loads subtab-specific data
   - Syncs state from URL

**Example Page Structure:**

```
File: app/pages/pnl/pnl_change_page.py
URL:  /pnl/pnl-change

Imports:
- PnLState (contains PnLChangeMixin)
- module_layout() from shared components
- pnl_change_table() from components

Page Function:
- Returns: module_layout(
    module="PnL",
    subtab="PnL Change",
    content=pnl_change_table()
  )

Route Registration:
- app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    on_load=PnLState.load_pnl_change_data
  )
```

#### State Mixin Pattern

**Per-Subtab Mixin (Following Reflex Mixin Best Practices):**

**File:** `app/states/pnl/mixins/pnl_change_mixin.py`

**Contents:**

1. **Mixin Definition**
   - Class with `mixin=True` parameter
   - Inherits from `rx.State`

2. **State Variables**
   - Subtab-specific data
   - Loading states
   - Error states

3. **Data Loading Methods**
   - `load_pnl_change_data()` - async method
   - Called via `on_load` when page accessed

4. **Event Handlers**
   - User interactions specific to this view
   - Filtering, sorting, etc.

5. **Computed Vars**
   - View-specific calculations
   - Filtered/sorted data

**Example Mixin:**

```
File: app/states/pnl/mixins/pnl_change_mixin.py

class PnLChangeMixin(rx.State, mixin=True):
    # State variables
    pnl_change_list: list[PnLChangeItem] = []
    is_loading_pnl_change: bool = False
    
    # Data loading
    async def load_pnl_change_data(self):
        self.is_loading_pnl_change = True
        try:
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_change()
        finally:
            self.is_loading_pnl_change = False
    
    # Computed vars
    @rx.var
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        # Apply filters
        return [item for item in self.pnl_change_list if ...]
```

#### Module State Composition

**File:** `app/states/pnl/pnl_state.py`

**Pattern:**

```
class PnLState(
    PnLChangeMixin,      # /pnl/pnl-change logic
    PnLFullMixin,        # /pnl/pnl-full logic
    PnLSummaryMixin,     # /pnl/pnl-summary logic
    PnLCurrencyMixin,    # /pnl/pnl-currency logic
    rx.State,            # Base state
):
    """Main PnL module state with all subtab mixins."""
    
    # Module-level state (shared across all subtabs)
    active_subtab: str = "PnL Change"
    date_filter: str = ""
    
    # Module-level event handlers
    def set_date_filter(self, date: str):
        self.date_filter = date
        # May need to reload active subtab data
```

**Key Points:**

1. **Multiple Mixin Inheritance:** State class inherits from all subtab mixins
2. **Flat Structure:** All mixins at same level, no deep hierarchy
3. **Separation of Concerns:** Each mixin handles ONE subtab
4. **Module-Level State:** Shared filters, settings in main state class
5. **Independent Loading:** Each subtab loads its data via its mixin's `load_*` method

#### Module Root Route Handling

**Pattern:** Module root redirects to default subtab

**File:** `app/pages/pnl/__init__.py`

```
File: app/pages/pnl/__init__.py

def pnl_root_page():
    """Redirect to default PnL subtab."""
    return rx.fragment()  # Empty, redirect happens in on_load

Registration:
app.add_page(
    pnl_root_page,
    route="/pnl",
    on_load=lambda: rx.redirect("/pnl/pnl-change")
)
```

**Alternative:** Could render default subtab directly instead of redirecting

### Module Layout Component

Create a reusable layout that wraps all module pages:

**Location:** `app/components/shared/module_layout.py`

**Components:**
- Top navigation bar (modules)
- Subtab navigation bar
- Performance header
- Notification sidebar
- Content area (slot for subtab content)

**Responsibilities:**
- Render shared UI elements
- Highlight active module in top navigation
- Highlight active subtab in subtab navigation
- Provide consistent spacing and structure
- Handle responsive behavior

**Parameters:**
- `current_module: str` - Name of active module
- `current_subtab: str` - Name of active subtab
- `content: rx.Component` - Subtab content to display

### Navigation Component Updates

#### Top Navigation Changes

**Current Implementation:**
- Buttons with `on_click` handlers
- Calls `set_module(module_name)` state event
- Changes state, triggers re-render

**New Implementation:**
- Links with `href` attributes
- Routes to `/{module-slug}`
- Triggers navigation, loads new page

**Pattern Changes:**

| Element | Current | New |
|---------|---------|-----|
| Component | `rx.el.button()` | `rx.link()` |
| Event | `on_click=PortfolioDashboardState.set_module(module_name)` | `href=f"/{module_slug}"` |
| State sync | Direct state change | State synced in `on_load` |

#### Subtab Navigation Changes

**Current Implementation:**
- Buttons calling `set_subtab(subtab_name)`
- Changes `_active_subtabs` dictionary
- Re-renders workspace content

**New Implementation:**
- Links with path segments
- Routes to `/{module-slug}/{subtab-slug}`
- Parses both from URL path in `on_load`

**Pattern Changes:**

| Element | Current | New |
|---------|---------|-----|
| Component | `rx.el.button()` | `rx.link()` |
| Event | `on_click=PortfolioDashboardState.set_subtab(name)` | `href=f"/{module_slug}/{subtab_slug}"` |
| State sync | Direct state change | Parse path segments in page |

### State Management Updates

#### Route Detection in `on_load`

Each dashboard page should detect the current route and sync state:

**Purpose:**
- Set `active_module` based on page route
- Set `active_subtab` based on query parameter
- Maintain backward compatibility with state-based logic

**Implementation Pattern:**
- Use `on_load` page event
- Access current route from Reflex router
- Parse query parameters
- Update state variables

#### Event Handler Updates

Existing event handlers that navigate should use redirects:

| Current Method | New Behavior |
|----------------|--------------|
| `set_module(module_name)` | Return `rx.redirect(f"/dashboard/{slug}")` |
| `set_subtab(subtab_name)` | Return `rx.redirect(current_path + f"?tab={slug}")` |
| Mobile menu item clicks | Return `rx.redirect()` instead of state change |

### Query Parameter Handling

#### Reading Path Segments

Reflex provides access to route path segments through the router:

**Pattern:**
- Access via `rx.State` route properties
- Parse in `on_load` event handler
- Extract module and subtab from path
- Set state based on path values

**Default Behavior:**
- If at module root (no subtab), redirect to default subtab
- If invalid subtab path, fallback to default or show 404
- Validate against `MODULE_SUBTABS` configuration

**Example Path Parsing:**
- URL: `/pnl/pnl-change`
- Parse: module = `pnl`, subtab = `pnl-change`
- Set state: `active_module = "PnL"`, `active_subtab = "PnL Change"`

#### Setting Path Segments

When user clicks subtab, construct URL with path segments:

**Pattern:**
- Build URL string: `f"/{module_slug}/{subtab_slug}"`
- Use `rx.link()` component with `href`
- Browser handles path navigation

### Module-to-Slug Mapping

Create consistent URL-friendly slugs for all modules and subtabs:

#### Module Slug Mapping

| Module Name | URL Slug |
|-------------|----------|
| Market Data | `market-data` |
| Positions | `positions` |
| PnL | `pnl` |
| Risk | `risk` |
| Recon | `recon` |
| Compliance | `compliance` |
| Portfolio Tools | `portfolio-tools` |
| Instruments | `instruments` |
| Events | `events` |
| Operations | `operations` |
| Orders | `orders` |

#### Subtab Slug Examples

**PnL Module:**
- "PnL Change" → `pnl-change`
- "PnL Full" → `pnl-full`
- "PnL Summary" → `pnl-summary`
- "PnL Currency" → `pnl-currency`

**Positions Module:**
- "Positions" → `positions` (default)
- "Stock Position" → `stock-position`
- "Warrant Position" → `warrant-position`
- "Bond Positions" → `bond-positions`
- "Trade Summary (War/Bond)" → `trade-summary`

**Pattern:**
- Lowercase all text
- Replace spaces with hyphens
- Remove special characters
- Use consistent formatting

### Root Path Behavior

#### Current: Dashboard at Root

Currently `/` shows the full dashboard with Market Data active by default.

#### Proposed: Redirect to Default Module and Subtab

When user visits `/`, redirect to the default module with its default subtab:

**Options:**

| Strategy | URL Behavior | Advantages |
|----------|--------------|------------|
| Redirect to Market Data | `/` → `/market-data/market-data` | Clear default, bookmarkable |
| Show landing page | `/` shows welcome, links to modules | Better introduction, clearer navigation |
| Redirect to last visited | `/` → last module/subtab route | Better UX, requires storage |

**Recommendation: Redirect to Market Data Default Subtab**

Rationale:
- Market Data is the logical default entry point
- Provides consistent, bookmarkable starting point
- `/market-data/market-data` is the first module + first subtab
- Aligns with new route-based architecture
- Simple to implement

**Alternative: Show Landing/Welcome Page**

Could also create a true landing page at `/` that:
- Shows overview or welcome message
- Provides module navigation cards
- Displays recent activity or quick links
- Better for first-time users

### Backward Compatibility Considerations

#### State Variables Preservation

Keep all existing state variables to avoid breaking changes:

**Variables to Maintain:**
- `active_module: str`
- `_active_subtabs: dict[str, str]`
- `MODULE_SUBTABS: dict[str, list[str]]`

**Purpose:**
- Components may still read these values
- Computed vars depend on them
- Maintains internal consistency

#### Event Handler Support

Existing event handlers should continue to work:

**Strategy:**
- Keep `set_module()` and `set_subtab()` methods for backward compatibility
- Update implementation to use `rx.redirect()` with path segments
- Return redirect event spec instead of direct state change
- State will be synced by `on_load` after redirect
- Build full path: `rx.redirect(f"/{module_slug}/{subtab_slug}")`

#### Component Compatibility

Components that reference state directly should continue working:

**Examples:**
- `active_module == "Market Data"` conditionals
- `current_subtabs` computed var usage
- `MODULE_SUBTABS` configuration access

**Strategy:**
- State is synced from URL in `on_load`
- Components read state as before
- No component changes required

## Testing & Validation Plan

### Manual Testing Checklist

| Test Case | Expected Result | Validation Method |
|-----------|----------------|-------------------|
| Click module in top nav | URL updates to `/{module}`, redirects to default subtab | Visual inspection, URL bar |
| Click subtab | URL updates to `/{module}/{subtab}` path | Visual inspection, URL bar |
| Direct URL access | Typing URL loads correct module and subtab | Browser address bar |
| Browser back button | Returns to previous module/subtab | Browser back button |
| Browser forward button | Advances to next module/subtab | Browser forward button |
| Bookmark and revisit | Same module and subtab loads | Save bookmark, close browser, reopen |
| Mobile menu navigation | Redirects to correct module route | Mobile viewport test |
| Root path `/` | Redirects to default module/subtab | Type `/` in address bar |
| Module root | Redirects to default subtab | Type `/pnl` → redirects to `/pnl/pnl-change` |
| Invalid module route | Shows 404 or redirects to default | Type `/invalid-module` |
| Invalid subtab path | Shows 404 or redirects to default | Type `/pnl/invalid-subtab` |

### Functional Requirements Validation

| Requirement | Test Approach | Success Criteria |
|-------------|---------------|------------------|
| Unique URLs for modules | Navigate to each module, check URL | Each module has distinct URL path |
| Unique URLs for subtabs | Navigate to each subtab, check URL | Full path updates with module and subtab |
| Deep linking support | Share URL with colleague, verify it loads same view | Exact module and subtab loads |
| Back/forward navigation | Click through multiple modules, use browser controls | History navigation works |
| Shared layout consistency | Switch modules, verify header/sidebar stays same | No layout flicker or reload |
| State synchronization | Check state values match URL | `active_module` matches route |
| Notification sidebar | Click module nav, check sidebar persists | Sidebar state preserved |
| Generate menu context | Switch modules, check generate menu options change | Menu adapts to module |

### Performance Validation

| Metric | Measurement Method | Acceptable Range |
|--------|-------------------|------------------|
| Route transition time | Browser DevTools Network tab | < 200ms |
| Initial page load | Lighthouse performance score | > 80 |
| State sync overhead | Measure `on_load` execution time | < 50ms |
| Memory usage | Browser Task Manager | No memory leaks |

## Implementation Sequence

### Step-by-Step Execution Plan

#### Step 1: Create Module Layout Component

**Tasks:**
- Create `app/components/shared/module_layout.py`
- Extract shared layout from `index()` function
- Accept `current_module` and `current_subtab` parameters
- Accept content component as child
- Render top navigation, subtab nav, header, and sidebar

**Files Modified:**
- New: `app/components/shared/module_layout.py`
- Update: `app/components/shared/__init__.py`

**Validation:**
- Layout renders correctly
- Top navigation highlights active module
- Subtab navigation highlights active subtab
- Content area displays passed component

#### Step 2: Create Subtab Mixins

**Tasks:**
- Create mixin files for each subtab in each module
- Implement mixin pattern with `mixin=True`
- Define subtab-specific state variables
- Implement data loading methods
- Add event handlers and computed vars
- Follow naming convention: `{Subtab}Mixin`

**Files Created (Example for PnL module):**
- New: `app/states/pnl/mixins/__init__.py`
- New: `app/states/pnl/mixins/pnl_change_mixin.py`
- New: `app/states/pnl/mixins/pnl_full_mixin.py`
- New: `app/states/pnl/mixins/pnl_summary_mixin.py`
- New: `app/states/pnl/mixins/pnl_currency_mixin.py`

**Files Created (Example for Positions module):**
- New: `app/states/positions/mixins/__init__.py`
- New: `app/states/positions/mixins/positions_mixin.py`
- New: `app/states/positions/mixins/stock_position_mixin.py`
- New: `app/states/positions/mixins/warrant_position_mixin.py`
- New: `app/states/positions/mixins/bond_positions_mixin.py`
- New: `app/states/positions/mixins/trade_summary_mixin.py`

**Mixin Template:**
```python
class {Subtab}Mixin(rx.State, mixin=True):
    # State vars
    {subtab}_data: list[dict] = []
    is_loading_{subtab}: bool = False
    
    # Data loading
    async def load_{subtab}_data(self):
        pass
    
    # Computed vars
    @rx.var
    def filtered_{subtab}(self) -> list[dict]:
        return self.{subtab}_data
```

**Validation:**
- Each mixin compiles without errors
- Mixin has `mixin=True` parameter
- Data loading methods are async
- Type hints are correct
- Service integration works

#### Step 3: Reorganize Module State Files

**Tasks:**
- Move existing state files to module directories
- Create main module state classes
- Inherit from all subtab mixins
- Add module-level shared state
- Update all import statements
- Maintain backward compatibility via re-exports

**Files Modified:**
- Move: `app/states/dashboard/pnl_state.py` → `app/states/pnl/pnl_state.py`
- Move: `app/states/dashboard/positions_state.py` → `app/states/positions/positions_state.py`
- Move: `app/states/dashboard/market_data_state.py` → `app/states/market_data/market_data_state.py`
- Move: `app/states/dashboard/types.py` → split into module-specific type files
- Update: All import statements across codebase
- New: `app/states/dashboard/__init__.py` (re-export for backward compatibility)

**Module State Pattern:**
```python
class {Module}State(
    {Subtab1}Mixin,
    {Subtab2}Mixin,
    {Subtab3}Mixin,
    rx.State,
):
    # Module-level shared state
    active_{module}_subtab: str = ""
    {module}_date_filter: str = ""
```

**Validation:**
- All imports resolve correctly
- State classes instantiate properly
- No circular import issues
- Existing components still work
- Backward compatibility maintained

#### Step 4: Create Subtab Page Functions

**Tasks:**
- Create module directories under `app/pages/`
- Create one subtab page file per subtab
- Implement redirect pages for module roots
- Implement subtab pages using module layout
- Parse path segments for module and subtab
- Implement `on_load` to sync state

**Files Modified:**
- New: `app/pages/market_data/__init__.py`
- New: `app/pages/market_data/market_data_page.py`
- New: `app/pages/market_data/fx_data_page.py`
- New: `app/pages/pnl/__init__.py`
- New: `app/pages/pnl/pnl_change_page.py`
- New: `app/pages/pnl/pnl_full_page.py`
- New: `app/pages/pnl/pnl_summary_page.py`
- New: `app/pages/pnl/pnl_currency_page.py`
- New: `app/pages/positions/__init__.py`
- New: `app/pages/positions/positions_page.py`
- New: `app/pages/positions/stock_position_page.py`
- ... (all other module/subtab pages)

**Validation:**
- Each page function returns valid component
- Path segments are parsed correctly
- State is synced on page load
- Module root redirects to default subtab

#### Step 5: Register Module and Subtab Routes

**Tasks:**
- Update `app/app.py`
- Import all subtab page functions
- Register each subtab with `app.add_page()`
- Define routes using path segments: `/{module}/{subtab}`
- Register module root routes with redirect on_load
- Add page titles and metadata for each subtab
- Register on_load handlers to call mixin's load method

**Files Modified:**
- `app/app.py`

**Registration Pattern (PnL Example):**
```python
# Module root - redirects to default
app.add_page(
    pnl_redirect,
    route="/pnl",
    on_load=lambda: rx.redirect("/pnl/pnl-change")
)

# Subtab pages with on_load calling mixin method
app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change | PMT",
    on_load=PnLState.load_pnl_change_data  # Calls mixin method
)

app.add_page(
    pnl_full_page,
    route="/pnl/pnl-full",
    title="P&L Full | PMT",
    on_load=PnLState.load_pnl_full_data  # Calls mixin method
)

app.add_page(
    pnl_summary_page,
    route="/pnl/pnl-summary",
    title="P&L Summary | PMT",
    on_load=PnLState.load_pnl_summary_data  # Calls mixin method
)

app.add_page(
    pnl_currency_page,
    route="/pnl/pnl-currency",
    title="P&L Currency | PMT",
    on_load=PnLState.load_pnl_currency_data  # Calls mixin method
)
```

**Key Points:**
- Each subtab route calls its specific mixin's load method
- Module state (PnLState) has access to all mixin methods
- Data loads only when subtab is accessed
- Page titles follow pattern: "{Subtab} | {App Name}"

**Validation:**
- All routes are accessible
- Correct page loads for each route
- on_load triggers correct mixin method
- Data loads for active subtab
- Page titles display correctly
- Module root routes redirect to default subtabs

#### Step 6: Update Top Navigation Component

**Tasks:**
- Modify `app/components/shared/top_navigation.py`
- Replace `on_click` handlers with `href` links
- Convert buttons to `rx.link()` components
- Keep active state detection logic
- Update mobile menu similarly

**Files Modified:**
- `app/components/shared/top_navigation.py`

**Validation:**
- Clicking module navigates to correct URL (module root → redirects to default subtab)
- Active module is highlighted
- Mobile menu navigation works
- Browser URL updates

#### Step 6: Update Top Navigation Component

**Tasks:**
- Modify `app/components/shared/top_navigation.py`
- Replace `on_click` handlers with `href` links
- Convert buttons to `rx.link()` components
- Link to module root (e.g., `/pnl`) which redirects to default subtab
- Keep active state detection logic
- Update mobile menu similarly

**Files Modified:**
- `app/components/shared/top_navigation.py`

**Changes:**
```python
# Old: Button with state change
rx.el.button(
    "PnL",
    on_click=PortfolioDashboardState.set_module("PnL")
)

# New: Link to module root
rx.link(
    "PnL",
    href="/pnl",  # Redirects to /pnl/pnl-change
    class_name="nav-link"
)
```

**Validation:**
- Clicking module navigates to correct URL
- Module root redirects to default subtab
- Active module is highlighted
- Mobile menu navigation works
- Browser URL updates

#### Step 7: Update Subtab Navigation

**Tasks:**
- Move subtab navigation out of `contextual_workspace.py` into `module_layout.py`
- Update `sub_tab()` function
- Replace `on_click` with `href` using path segments: `/{module}/{subtab}`
- Keep active subtab highlighting
- Preserve workspace controls functionality

**Files Modified:**
- `app/components/shared/contextual_workspace.py` (simplified)
- `app/components/shared/module_layout.py` (includes subtab nav)

**Validation:**
- Clicking subtab updates URL path
- Active subtab is highlighted
- Content switches correctly
- Back button navigates to previous subtab

#### Step 7: Update Subtab Navigation

**Tasks:**
- Move subtab navigation from `contextual_workspace.py` to `module_layout.py`
- Update subtab rendering to use module-specific subtabs
- Replace `on_click` with `href` using full path segments
- Build URLs: `/{module_slug}/{subtab_slug}`
- Keep active subtab highlighting
- Read active subtab from state (set by URL)

**Files Modified:**
- `app/components/shared/contextual_workspace.py` (simplified, no subtab nav)
- `app/components/shared/module_layout.py` (includes subtab nav)

**Subtab Navigation Pattern:**
```python
# In module_layout.py
def subtab_nav(module: str, active_subtab: str, subtabs: list[str]):
    """Render subtab navigation for a module."""
    return rx.hstack(
        rx.foreach(
            subtabs,
            lambda subtab: rx.link(
                subtab,
                href=f"/{module_to_slug(module)}/{subtab_to_slug(subtab)}",
                class_name=rx.cond(
                    subtab == active_subtab,
                    "subtab-active",
                    "subtab-inactive"
                )
            )
        )
    )
```

**Usage in Page:**
```python
def pnl_change_page():
    return module_layout(
        module="PnL",
        subtab="PnL Change",
        subtabs=["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"],
        content=pnl_change_table()
    )
```

**Validation:**
- Clicking subtab updates URL path
- Active subtab is highlighted
- Content switches correctly
- Back button navigates to previous subtab
- URL matches file structure

#### Step 8: Update State Event Handlers

**Tasks:**
- Update `set_module()` to return `rx.redirect()` with path segment
- Update `set_subtab()` to return `rx.redirect()` with full path
- Update mobile menu handlers
- Keep state variables for backward compatibility
- Update in all module state files (after reorganization)

**Files Modified:**
- `app/states/market_data/market_data_state.py`
- `app/states/positions/positions_state.py`
- `app/states/pnl/pnl_state.py`
- ... (all module state files)

**Validation:**
- Programmatic navigation still works
- State remains synchronized
- Redirects use correct path format: `/{module}/{subtab}`
- No breaking changes to dependent code

#### Step 8: Update State Event Handlers

**Tasks:**
- Update navigation event handlers in module states
- Modify `set_module()` to return `rx.redirect()` with path
- Modify `set_subtab()` to return `rx.redirect()` with full path
- Update mobile menu handlers
- Keep state variables for backward compatibility
- Update in all module state files

**Files Modified:**
- `app/states/market_data/market_data_state.py`
- `app/states/positions/positions_state.py`
- `app/states/pnl/pnl_state.py`
- ... (all module state files)

**Event Handler Pattern:**
```python
# In module state (e.g., PnLState)
class PnLState(...):
    
    def navigate_to_subtab(self, subtab_name: str):
        """Navigate to specific PnL subtab."""
        subtab_slug = subtab_to_slug(subtab_name)
        return rx.redirect(f"/pnl/{subtab_slug}")
    
    # For backward compatibility if needed
    def set_module(self, module_name: str):
        """Navigate to module root (redirects to default subtab)."""
        module_slug = module_to_slug(module_name)
        return rx.redirect(f"/{module_slug}")
```

**Module-Level Navigation (if needed):**
```python
# In a global/shared state if cross-module navigation is needed
def navigate_to_module(self, module_name: str, subtab_name: str = None):
    module_slug = module_to_slug(module_name)
    if subtab_name:
        subtab_slug = subtab_to_slug(subtab_name)
        return rx.redirect(f"/{module_slug}/{subtab_slug}")
    return rx.redirect(f"/{module_slug}")  # Redirects to default
```

**Validation:**
- Programmatic navigation still works
- State remains synchronized
- Redirects use correct path format: `/{module}/{subtab}`
- No breaking changes to dependent code
- Module state methods accessible

#### Step 9: Implement Root Path Redirect

**Tasks:**
- Modify `app/app.py`
- Update `index()` function or route handler
- Implement redirect to `/market-data/market-data` (first module, first subtab)
- Or create a proper landing page with module navigation

**Files Modified:**
- `app/app.py`

**Validation:**
- Visiting `/` redirects to default module/subtab
- Default subtab loads correctly
- No redirect loop

#### Step 9: Implement Root Path Redirect

**Tasks:**
- Create helper functions for slug generation
- Create mapping dictionaries (module → slug, subtab → slug)
- Create reverse mapping (slug → module, slug → subtab)
- Create path parsing utilities
- Validate path segments against configuration

**Files Modified:**
- New: `app/utils/route_utils.py`
- Update imports in all module state files

**Validation:**
- Slug conversion is consistent
- Invalid slugs are handled gracefully
- Reverse lookup works correctly
- Path parsing extracts module and subtab correctly

#### Step 10: Add Path Segment Utilities

**Tasks:**
- Perform manual testing (see checklist above)
- Test all module navigation paths
- Test all subtab navigation
- Test browser back/forward
- Test deep linking
- Fix any identified issues

**Files Modified:**
- Various (as needed for bug fixes)

**Validation:**
- All test cases pass
- No regressions in existing functionality
- Performance is acceptable

#### Step 11: Testing & Bug Fixes

**Tasks:**
- Update `AGENTS.md` with routing patterns
- Document new URL structure
- Update developer guidelines
- Add code comments

**Files Modified:**
- `AGENTS.md`
- `README.md`
- Code files (comments)

**Validation:**
- Documentation is clear and accurate
- Examples are provided
- Routing patterns are explained

## Technical Constraints & Considerations

### Reflex Framework Limitations

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Route parameter syntax | Limited parameter patterns | Use query strings for subtabs |
| State synchronization timing | `on_load` executes async | Ensure proper await patterns |
| Client-side routing | May conflict with server routes | Use consistent route registration |
| Shared state across routes | State persists between pages | Leverage this for continuity |

### Browser Compatibility

| Concern | Testing Required | Fallback Strategy |
|---------|------------------|-------------------|
| History API support | Test on older browsers | Graceful degradation to state-based |
| Query parameter parsing | Test special characters | URL encode/decode properly |
| Back button behavior | Test navigation history | Ensure state sync on back |

### Performance Considerations

| Factor | Expected Impact | Optimization Strategy |
|--------|----------------|----------------------|
| Route registration overhead | Minimal (startup only) | Pre-register all routes on init |
| State sync on load | < 50ms per navigation | Cache route-to-module mapping |
| Component re-rendering | Similar to current | No change in render performance |
| Bundle size increase | Small (new page files) | Code splitting if needed |

## Alternative Approaches Considered

### Alternative 1: Keep State-Based, Add URL Sync

**Approach:**
- Keep current state-based navigation
- Add event handlers to update URL when state changes
- Use browser History API to sync URL

**Advantages:**
- Minimal code changes
- Preserves existing architecture
- Easier to implement

**Disadvantages:**
- Not true routing
- Fragile URL sync logic
- Browser back/forward requires custom handling
- More complex state management

**Decision: Not Recommended**

Rationale: This creates complexity without solving the core architectural issue. True routing is cleaner and more maintainable.

### Alternative 2: Single Route with Hash Navigation

**Approach:**
- Use hash-based routing (`#/market-data`)
- Keep single page at `/`
- Parse hash to determine view

**Advantages:**
- No server-side route registration needed
- Simpler deployment
- Backward compatible

**Disadvantages:**
- Hash URLs are outdated pattern
- Poor SEO (though not critical for this app)
- Less clean URL structure
- Harder to implement deep linking

**Decision: Not Recommended**

Rationale: Hash routing is a legacy pattern. Modern frameworks support proper routing, which is cleaner and more professional.

### Alternative 3: Micro-Frontend Architecture

**Approach:**
- Split dashboard into separate mini-apps
- Each module is independent application
- Use shared component library

**Advantages:**
- Complete isolation
- Independent deployments
- Scalable architecture

**Disadvantages:**
- Massive refactoring required
- Shared state becomes complex
- Performance overhead
- Over-engineered for current needs

**Decision: Not Recommended**

Rationale: This is overkill for the current application scale. The proposed routing solution achieves the goals with far less complexity.

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Breaking existing functionality | Medium | High | Comprehensive testing, keep backward compatibility |
| Performance regression | Low | Medium | Performance benchmarks, optimize state sync |
| Increased complexity | Medium | Low | Clear documentation, consistent patterns |
| State synchronization bugs | Medium | Medium | Thorough testing of edge cases |
| Browser history issues | Low | Medium | Test back/forward extensively |
| Mobile navigation problems | Low | Medium | Mobile-specific testing |

## Success Metrics

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|-------------------|
| Unique URLs per view | 1 (root only) | 11 modules + subtabs | Route count |
| Deep linking support | No | Yes | Test URL sharing |
| Browser nav support | No | Yes | Test back/forward buttons |
| URL updates on click | No | Yes | Visual inspection |
| State sync accuracy | N/A | 100% | Automated tests |
| Navigation performance | Baseline | No degradation | Performance monitoring |

## Implementation Timeline Estimate

| Phase | Estimated Duration | Complexity | Dependencies |
|-------|-------------------|------------|--------------|
| Phase 1: Dashboard layout | 2 hours | Low | None |
| Phase 2: Create module pages | 4 hours | Medium | Phase 1 |
| Phase 3: Register routes | 1 hour | Low | Phase 2 |
| Phase 4: Update top navigation | 2 hours | Medium | Phase 3 |
| Phase 5: Update subtab navigation | 2 hours | Medium | Phase 3 |
| Phase 6: Update event handlers | 2 hours | Medium | Phase 4, 5 |
| Phase 7: Root path redirect | 1 hour | Low | Phase 3 |
| Phase 8: Utilities | 2 hours | Low | None |
| Phase 9: Testing | 4 hours | High | All phases |
| Phase 10: Documentation | 2 hours | Low | Phase 9 |
| **Total** | **22 hours** | | |

**Note:** Timeline assumes single developer working sequentially. Can be parallelized for faster delivery.

## Technical Reference

### Key Reflex Concepts

#### Route Registration

Routes are registered in `app.py` using `app.add_page()`:

**Parameters:**
- `component`: Page function that returns `rx.Component`
- `route`: URL path (e.g., `/pnl/pnl-change`)
- `title`: Browser page title
- `on_load`: Event handler called when page loads
- `meta`: Metadata for SEO

**Example Pattern:**
```
app.add_page(
    component=pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change",
    on_load=PnLState.sync_from_route
)
```

**Route Structure:**
- Pattern: `/{module-slug}/{subtab-slug}`
- Module slugs: kebab-case (e.g., `market-data`, `portfolio-tools`)
- Subtab slugs: kebab-case (e.g., `pnl-change`, `stock-position`)
- Each subtab is a separate route registration

#### Event Handlers and Redirects

Event handlers can return special events like `rx.redirect()`:

**Usage:**
- Returns navigation event spec
- Triggers client-side route change
- Updates browser URL
- Triggers `on_load` on target page

**Example Pattern:**
```
@rx.event
def set_module(self, module_name: str):
    module_slug = module_to_slug(module_name)
    # Get default subtab for this module
    default_subtab = get_default_subtab(module_name)
    subtab_slug = subtab_to_slug(default_subtab)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")

@rx.event
def set_subtab(self, subtab_name: str):
    module_slug = module_to_slug(self.active_module)
    subtab_slug = subtab_to_slug(subtab_name)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")
```

#### Page Load Events

The `on_load` handler executes when a page is navigated to:

**Characteristics:**
- Runs before page renders
- Can be async
- Access to route parameters
- Updates state before render

**Example Pattern:**
```
async def sync_from_route(self):
    current_route = self.router.page.path
    # Parse: "/pnl/pnl-change" → module="pnl", subtab="pnl-change"
    segments = current_route.strip('/').split('/')
    if len(segments) >= 2:
        module_slug, subtab_slug = segments[0], segments[1]
        self.active_module = slug_to_module(module_slug)
        self.active_subtab = slug_to_subtab(subtab_slug)
    elif len(segments) == 1:
        # Module root - redirect to default subtab
        module_slug = segments[0]
        module_name = slug_to_module(module_slug)
        default_subtab = get_default_subtab(module_name)
        return rx.redirect(f"/{module_slug}/{subtab_to_slug(default_subtab)}")
```

#### Path Segment Access

Access URL path segments through the router:

**Pattern:**
- Read from `self.router.page.path`
- Split path string by `/`
- Extract module and subtab segments
- Convert slugs back to display names
- Validate and use values

**Example:**
```
path = "/pnl/pnl-change"
segments = path.strip('/').split('/')  # ['pnl', 'pnl-change']
module_slug = segments[0]  # 'pnl'
subtab_slug = segments[1]  # 'pnl-change'
module_name = slug_to_module(module_slug)  # 'PnL'
subtab_name = slug_to_subtab(subtab_slug)  # 'PnL Change'
```

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.
| Increased complexity | Medium | Low | Clear documentation, consistent patterns |
| State synchronization bugs | Medium | Medium | Thorough testing of edge cases |
| Browser history issues | Low | Medium | Test back/forward extensively |
| Mobile navigation problems | Low | Medium | Mobile-specific testing |

## Success Metrics

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|-------------------|
| Unique URLs per view | 1 (root only) | 11 modules + subtabs | Route count |
| Deep linking support | No | Yes | Test URL sharing |
| Browser nav support | No | Yes | Test back/forward buttons |
| URL updates on click | No | Yes | Visual inspection |
| State sync accuracy | N/A | 100% | Automated tests |
| Navigation performance | Baseline | No degradation | Performance monitoring |

## Implementation Timeline Estimate

| Phase | Estimated Duration | Complexity | Dependencies |
|-------|-------------------|------------|--------------|
| Phase 1: Dashboard layout | 2 hours | Low | None |
| Phase 2: Create module pages | 4 hours | Medium | Phase 1 |
| Phase 3: Register routes | 1 hour | Low | Phase 2 |
| Phase 4: Update top navigation | 2 hours | Medium | Phase 3 |
| Phase 5: Update subtab navigation | 2 hours | Medium | Phase 3 |
| Phase 6: Update event handlers | 2 hours | Medium | Phase 4, 5 |
| Phase 7: Root path redirect | 1 hour | Low | Phase 3 |
| Phase 8: Utilities | 2 hours | Low | None |
| Phase 9: Testing | 4 hours | High | All phases |
| Phase 10: Documentation | 2 hours | Low | Phase 9 |
| **Total** | **22 hours** | | |

**Note:** Timeline assumes single developer working sequentially. Can be parallelized for faster delivery.

## Technical Reference

### Key Reflex Concepts

#### Route Registration

Routes are registered in `app.py` using `app.add_page()`:

**Parameters:**
- `component`: Page function that returns `rx.Component`
- `route`: URL path (e.g., `/pnl/pnl-change`)
- `title`: Browser page title
- `on_load`: Event handler called when page loads
- `meta`: Metadata for SEO

**Example Pattern:**
```
app.add_page(
    component=pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change",
    on_load=PnLState.sync_from_route
)
```

**Route Structure:**
- Pattern: `/{module-slug}/{subtab-slug}`
- Module slugs: kebab-case (e.g., `market-data`, `portfolio-tools`)
- Subtab slugs: kebab-case (e.g., `pnl-change`, `stock-position`)
- Each subtab is a separate route registration

#### Event Handlers and Redirects

Event handlers can return special events like `rx.redirect()`:

**Usage:**
- Returns navigation event spec
- Triggers client-side route change
- Updates browser URL
- Triggers `on_load` on target page

**Example Pattern:**
```
@rx.event
def set_module(self, module_name: str):
    module_slug = module_to_slug(module_name)
    # Get default subtab for this module
    default_subtab = get_default_subtab(module_name)
    subtab_slug = subtab_to_slug(default_subtab)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")

@rx.event
def set_subtab(self, subtab_name: str):
    module_slug = module_to_slug(self.active_module)
    subtab_slug = subtab_to_slug(subtab_name)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")
```

#### Page Load Events

The `on_load` handler executes when a page is navigated to:

**Characteristics:**
- Runs before page renders
- Can be async
- Access to route parameters
- Updates state before render

**Example Pattern:**
```
async def sync_from_route(self):
    current_route = self.router.page.path
    # Parse: "/pnl/pnl-change" → module="pnl", subtab="pnl-change"
    segments = current_route.strip('/').split('/')
    if len(segments) >= 2:
        module_slug, subtab_slug = segments[0], segments[1]
        self.active_module = slug_to_module(module_slug)
        self.active_subtab = slug_to_subtab(subtab_slug)
    elif len(segments) == 1:
        # Module root - redirect to default subtab
        module_slug = segments[0]
        module_name = slug_to_module(module_slug)
        default_subtab = get_default_subtab(module_name)
        return rx.redirect(f"/{module_slug}/{subtab_to_slug(default_subtab)}")
```

#### Path Segment Access

Access URL path segments through the router:

**Pattern:**
- Read from `self.router.page.path`
- Split path string by `/`
- Extract module and subtab segments
- Convert slugs back to display names
- Validate and use values

**Example:**
```
path = "/pnl/pnl-change"
segments = path.strip('/').split('/')  # ['pnl', 'pnl-change']
module_slug = segments[0]  # 'pnl'
subtab_slug = segments[1]  # 'pnl-change'
module_name = slug_to_module(module_slug)  # 'PnL'
subtab_name = slug_to_subtab(subtab_slug)  # 'PnL Change'
```

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.
- `meta`: Metadata for SEO

**Example Pattern:**
```
app.add_page(
    component=pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change",
    on_load=PnLState.sync_from_route
)
```

**Route Structure:**
- Pattern: `/{module-slug}/{subtab-slug}`
- Module slugs: kebab-case (e.g., `market-data`, `portfolio-tools`)
- Subtab slugs: kebab-case (e.g., `pnl-change`, `stock-position`)
- Each subtab is a separate route registration

#### Event Handlers and Redirects

Event handlers can return special events like `rx.redirect()`:

**Usage:**
- Returns navigation event spec
- Triggers client-side route change
- Updates browser URL
- Triggers `on_load` on target page

**Example Pattern:**
```
@rx.event
def set_module(self, module_name: str):
    module_slug = module_to_slug(module_name)
    # Get default subtab for this module
    default_subtab = get_default_subtab(module_name)
    subtab_slug = subtab_to_slug(default_subtab)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")

@rx.event
def set_subtab(self, subtab_name: str):
    module_slug = module_to_slug(self.active_module)
    subtab_slug = subtab_to_slug(subtab_name)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")
```

#### Page Load Events

The `on_load` handler executes when a page is navigated to:

**Characteristics:**
- Runs before page renders
- Can be async
- Access to route parameters
- Updates state before render

**Example Pattern:**
```
async def sync_from_route(self):
    current_route = self.router.page.path
    # Parse: "/pnl/pnl-change" → module="pnl", subtab="pnl-change"
    segments = current_route.strip('/').split('/')
    if len(segments) >= 2:
        module_slug, subtab_slug = segments[0], segments[1]
        self.active_module = slug_to_module(module_slug)
        self.active_subtab = slug_to_subtab(subtab_slug)
    elif len(segments) == 1:
        # Module root - redirect to default subtab
        module_slug = segments[0]
        module_name = slug_to_module(module_slug)
        default_subtab = get_default_subtab(module_name)
        return rx.redirect(f"/{module_slug}/{subtab_to_slug(default_subtab)}")
```

#### Path Segment Access

Access URL path segments through the router:

**Pattern:**
- Read from `self.router.page.path`
- Split path string by `/`
- Extract module and subtab segments
- Convert slugs back to display names
- Validate and use values

**Example:**
```
path = "/pnl/pnl-change"
segments = path.strip('/').split('/')  # ['pnl', 'pnl-change']
module_slug = segments[0]  # 'pnl'
subtab_slug = segments[1]  # 'pnl-change'
module_name = slug_to_module(module_slug)  # 'PnL'
subtab_name = slug_to_subtab(subtab_slug)  # 'PnL Change'
```

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.
- `meta`: Metadata for SEO

**Example Pattern:**
```
app.add_page(
    component=pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change",
    on_load=PnLState.sync_from_route
)
```

**Route Structure:**
- Pattern: `/{module-slug}/{subtab-slug}`
- Module slugs: kebab-case (e.g., `market-data`, `portfolio-tools`)
- Subtab slugs: kebab-case (e.g., `pnl-change`, `stock-position`)
- Each subtab is a separate route registration

#### Event Handlers and Redirects

Event handlers can return special events like `rx.redirect()`:

**Usage:**
- Returns navigation event spec
- Triggers client-side route change
- Updates browser URL
- Triggers `on_load` on target page

**Example Pattern:**
```
@rx.event
def set_module(self, module_name: str):
    module_slug = module_to_slug(module_name)
    # Get default subtab for this module
    default_subtab = get_default_subtab(module_name)
    subtab_slug = subtab_to_slug(default_subtab)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")

@rx.event
def set_subtab(self, subtab_name: str):
    module_slug = module_to_slug(self.active_module)
    subtab_slug = subtab_to_slug(subtab_name)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")
```

#### Page Load Events

The `on_load` handler executes when a page is navigated to:

**Characteristics:**
- Runs before page renders
- Can be async
- Access to route parameters
- Updates state before render

**Example Pattern:**
```
async def sync_from_route(self):
    current_route = self.router.page.path
    # Parse: "/pnl/pnl-change" → module="pnl", subtab="pnl-change"
    segments = current_route.strip('/').split('/')
    if len(segments) >= 2:
        module_slug, subtab_slug = segments[0], segments[1]
        self.active_module = slug_to_module(module_slug)
        self.active_subtab = slug_to_subtab(subtab_slug)
    elif len(segments) == 1:
        # Module root - redirect to default subtab
        module_slug = segments[0]
        module_name = slug_to_module(module_slug)
        default_subtab = get_default_subtab(module_name)
        return rx.redirect(f"/{module_slug}/{subtab_to_slug(default_subtab)}")
```

#### Path Segment Access

Access URL path segments through the router:

**Pattern:**
- Read from `self.router.page.path`
- Split path string by `/`
- Extract module and subtab segments
- Convert slugs back to display names
- Validate and use values

**Example:**
```
path = "/pnl/pnl-change"
segments = path.strip('/').split('/')  # ['pnl', 'pnl-change']
module_slug = segments[0]  # 'pnl'
subtab_slug = segments[1]  # 'pnl-change'
module_name = slug_to_module(module_slug)  # 'PnL'
subtab_name = slug_to_subtab(subtab_slug)  # 'PnL Change'
```

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.
- `meta`: Metadata for SEO

**Example Pattern:**
```
app.add_page(
    component=pnl_change_page,
    route="/pnl/pnl-change",
    title="P&L Change",
    on_load=PnLState.sync_from_route
)
```

**Route Structure:**
- Pattern: `/{module-slug}/{subtab-slug}`
- Module slugs: kebab-case (e.g., `market-data`, `portfolio-tools`)
- Subtab slugs: kebab-case (e.g., `pnl-change`, `stock-position`)
- Each subtab is a separate route registration

#### Event Handlers and Redirects

Event handlers can return special events like `rx.redirect()`:

**Usage:**
- Returns navigation event spec
- Triggers client-side route change
- Updates browser URL
- Triggers `on_load` on target page

**Example Pattern:**
```
@rx.event
def set_module(self, module_name: str):
    module_slug = module_to_slug(module_name)
    # Get default subtab for this module
    default_subtab = get_default_subtab(module_name)
    subtab_slug = subtab_to_slug(default_subtab)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")

@rx.event
def set_subtab(self, subtab_name: str):
    module_slug = module_to_slug(self.active_module)
    subtab_slug = subtab_to_slug(subtab_name)
    return rx.redirect(f"/{module_slug}/{subtab_slug}")
```

#### Page Load Events

The `on_load` handler executes when a page is navigated to:

**Characteristics:**
- Runs before page renders
- Can be async
- Access to route parameters
- Updates state before render

**Example Pattern:**
```
async def sync_from_route(self):
    current_route = self.router.page.path
    # Parse: "/pnl/pnl-change" → module="pnl", subtab="pnl-change"
    segments = current_route.strip('/').split('/')
    if len(segments) >= 2:
        module_slug, subtab_slug = segments[0], segments[1]
        self.active_module = slug_to_module(module_slug)
        self.active_subtab = slug_to_subtab(subtab_slug)
    elif len(segments) == 1:
        # Module root - redirect to default subtab
        module_slug = segments[0]
        module_name = slug_to_module(module_slug)
        default_subtab = get_default_subtab(module_name)
        return rx.redirect(f"/{module_slug}/{subtab_to_slug(default_subtab)}")
```

#### Path Segment Access

Access URL path segments through the router:

**Pattern:**
- Read from `self.router.page.path`
- Split path string by `/`
- Extract module and subtab segments
- Convert slugs back to display names
- Validate and use values

**Example:**
```
path = "/pnl/pnl-change"
segments = path.strip('/').split('/')  # ['pnl', 'pnl-change']
module_slug = segments[0]  # 'pnl'
subtab_slug = segments[1]  # 'pnl-change'
module_name = slug_to_module(module_slug)  # 'PnL'
subtab_name = slug_to_subtab(subtab_slug)  # 'PnL Change'
```

#### Component Links

Use `rx.link()` for navigation instead of buttons:

**Attributes:**
- `href`: Target URL (path segment format)
- Children: Link content
- `class_name`: Styling

**Example:**
```
rx.link(
    "P&L Change",
    href="/pnl/pnl-change",
    class_name="subtab-link"
)
```

**Advantage:**
- Standard web navigation
- Browser handles history
- Proper semantic HTML
- SEO friendly (if applicable)

### Reflex State Management

#### State Persistence

State persists across route changes within the same session:

**Implications:**
- Shared state available to all pages
- No need to reload common data
- Maintain user context during navigation

#### Computed Vars

Computed vars (`@rx.var`) recalculate when dependencies change:

**Usage for Routing:**
- Derive active state from route
- Calculate available subtabs
- Generate navigation data

### Module-Subtab Mapping Reference

Reference table for all modules and their subtabs:

| Module | Default Subtab | All Subtabs |
|--------|---------------|-------------|
| Market Data | Market Data | Market Data, FX Data, Reference Data, Historical Data, Trading Calendar, Market Hours |
| Positions | Positions | Positions, Stock Position, Warrant Position, Bond Positions, Trade Summary |
| PnL | PnL Change | PnL Change, PnL Full, PnL Summary, PnL Currency |
| Risk | Delta Change | Delta Change, Risk Measures, Risk Inputs, Pricer Warrant, Pricer Bond |
| Recon | PPS Recon | PPS Recon, Settlement Recon, Failed Trades, PnL Recon, Risk Input Recon |
| Compliance | Restricted List | Restricted List, Undertakings, Beneficial Ownership, Monthly Exercise Limit |
| Portfolio Tools | Pay-To-Hold | Pay-To-Hold, Short ECL, Stock Borrow, PO Settlement, Deal Indication, Reset Dates, Coming Resets, CB Installments, Excess Amount |
| Instruments | Ticker Data | Ticker Data, Stock Screener, Special Term, Instrument Data, Instrument Term |
| Events | Event Calendar | Event Calendar, Event Stream, Reverse Inquiry |
| Operations | Daily Procedure Check | Daily Procedure Check, Operation Process |
| Orders | EMSX Order | EMSX Order, EMSX Route |

## Conclusion

This investigation reveals that the Portfolio Management Tool's dashboard uses a state-based SPA pattern where all modules are rendered at the root path `/` with no unique URLs. While this works functionally, it prevents bookmarking, deep linking, and proper browser navigation.

The recommended solution is to implement a route-based architecture where each dashboard module has its own route under `/{module-slug}/{subtab-slug}`, with state organized into per-module folders containing per-subtab mixins.

**Current Progress:**
- ✅ PnL, Positions, and Market Data modules have been successfully migrated to the new structure
- ⏳ Risk, Compliance, Orders, Reconciliation, Events, Instruments, Operations, and Portfolio Tools modules remain in the dashboard folder
- 📋 Complete migration requires an additional 31 hours of work

**Next Steps:**
1. Complete state migration for remaining 8 modules (31 hours)
2. Create page files and register routes for all modules
3. Update navigation components to use route-based links
4. Delete deprecated dashboard folder files

The implementation is straightforward, with clear benefits: bookmarkable URLs, browser history support, better user experience, modular state organization, and alignment with web standards and Reflex best practices.

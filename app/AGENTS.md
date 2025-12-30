
# AGENTS.md - AI-to-AI Handoff Documentation

> **CRITICAL**: This is a **Reflex** application. The UI is written entirely in Python but compiles to React/Next.js. DO NOT write raw HTML, JavaScript, or React components. All UI must use `rx.*` components.

## Project Overview

This is a **professional portfolio management dashboard** reimplemented from a PyQt desktop application as a high-performance web app. It follows a strict 4-region layout architecture mimicking Bloomberg Terminal / institutional trading interfaces.

---

## Project Structure Map


app/
├── app.py                      # Main entry point - defines index() and all page routes
├── constants.py                # UI constants (colors, heights, sizes)
├── states/                     # All rx.State classes
│   ├── __init__.py
│   ├── portfolio_dashboard_state.py  # PRIMARY STATE - modules, subtabs, KPIs, tables, PnL
│   ├── dashboard_state.py            # Holdings, portfolio metrics
│   ├── portfolio_state.py            # Individual portfolio management
│   ├── watchlist_state.py            # Watchlist + alerts
│   ├── research_state.py             # Stock research data
│   ├── reports_state.py              # Performance reports
│   ├── goals_state.py                # Financial goals
│   ├── profile_state.py              # User profile
│   ├── settings_state.py             # App settings
│   ├── notification_state.py         # General notifications
│   ├── notification_pagination_state.py  # Sidebar notification pagination
│   └── mobile_nav_state.py           # Mobile navigation toggle
├── components/                 # Reusable UI components
│   ├── top_navigation.py             # Region 1 - Top nav bar (11 modules)
│   ├── performance_header.py         # Region 2 - KPIs + Top Movers
│   ├── contextual_workspace.py       # Region 3 - Main data tables
│   ├── notification_sidebar.py       # Region 4 - Alert cards
│   ├── pnl_views.py                  # PnL Change/Summary/Currency tables
│   ├── summary_cards.py              # Portfolio summary KPI cards
│   └── [other components...]
├── pages/                      # Secondary page definitions
│   ├── portfolio_page.py
│   ├── watchlist_page.py
│   ├── research_page.py
│   └── [other pages...]
├── services/
│   └── finance_service.py      # yfinance API integration
└── rxconfig.py                 # Reflex configuration (TailwindV3 plugin)


---

## State Management Strategy

### Primary State: `PortfolioDashboardState`

**Location**: `app/states/portfolio_dashboard_state.py`

This is the **central state** controlling the main dashboard. It manages:


class PortfolioDashboardState(rx.State):
    # Navigation
    active_module: str = "Market Data"          # 1 of 11 modules
    _active_subtabs: dict[str, str] = {}        # Per-module subtab memory
    
    # UI Toggles
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_generate_menu_open: bool = False
    show_top_movers: bool = False
    
    # Table State
    selected_row_id: int = -1
    current_page: int = 1
    page_size: int = 50
    is_loading: bool = False
    
    # Data
    kpi_metrics: list[KPIMetric]                # 5 KPI cards
    top_movers_*: list[TopMover]                # 5 mini-grids
    notifications: list[NotificationItem]       # Right sidebar alerts
    pnl_change_data: list[PnLChangeItem]        # PnL Change tab
    pnl_summary_data: list[PnLSummaryItem]      # PnL Summary tab
    pnl_currency_data: list[PnLCurrencyItem]    # PnL Currency tab
    _all_table_data: list[dict]                 # Main positions table
    
    # Module Configuration
    module_icons: dict[str, str]                # Module -> icon mapping
    MODULE_SUBTABS: dict[str, list[str]]        # Module -> subtabs mapping (52 total pages)


**Key Computed Vars**:

@rx.var
def current_subtabs(self) -> list[str]:        # Dynamic subtab list
@rx.var
def active_subtab(self) -> str:                 # Current subtab for module
@rx.var
def filtered_table_data(self) -> list[dict]:   # Search-filtered data
@rx.var
def paginated_table_data(self) -> list[dict]:  # Page-sliced data
@rx.var
def filtered_pnl_change(self) -> list[PnLChangeItem]:  # Filtered PnL data


### Secondary States

| State Class | Purpose | Key Vars |
|-------------|---------|----------|
| `DashboardState` | Portfolio holdings & metrics | `holdings`, `total_value`, `daily_change_value` |
| `WatchlistState` | Stock watchlist + alerts | `watchlist`, `alerts`, `news_feed`, `search_query` |
| `ResearchState` | Stock research & analysis | `all_stocks`, `selected_stock`, `chart_data` |
| `PortfolioState` | Multi-portfolio management | `portfolios`, `selected_portfolio_index`, transactions |
| `GoalsState` | Financial goals tracking | `goals`, `total_goals_value`, `goals_on_track` |
| `ReportsState` | Performance reports | `performance_data`, `allocation_analysis` |
| `ProfileState` | User profile data | `name`, `email`, `linked_accounts` |
| `NotificationPaginationState` | Sidebar pagination | Accesses `PortfolioDashboardState` via `get_state()` |

### Cross-State Communication Pattern


# CORRECT: Use async + get_state() for cross-state access
class NotificationPaginationState(rx.State):
    @rx.var
    async def paginated_notifications(self) -> list[NotificationItem]:
        dashboard = await self.get_state(PortfolioDashboardState)
        return dashboard.notifications[start:end]


---

## Database Models

**IMPORTANT**: This application uses **in-memory mock data** with TypedDict patterns. There is **NO database** or sqlmodel integration.

### TypedDict Definitions (Data Contracts)


# Core position data
class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool

class TopMover(TypedDict):
    ticker: str
    name: str
    value: str
    change: str
    is_positive: bool

class NotificationItem(TypedDict):
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str        # "alert" | "warning" | "info"
    read: bool

# PnL view data
class PnLChangeItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: str
    pnl_chg_1d: str
    sparkline_svg: str      # SVG polyline points
    sparkline_color: str    # "#059669" or "#DC2626"
    is_reconciled: bool

class PnLSummaryItem(TypedDict):
    # Price, FX rates, volume data
    
class PnLCurrencyItem(TypedDict):
    # Currency exposure data


### Data Generation

Mock data is generated at module load time:

_all_table_data: list[dict] = _generate_mock_data()  # 400 rows
pnl_change_data = _generate_pnl_change_data()        # 20 rows


---

## Key Patterns

### 1. Conditional Rendering (`rx.cond`)

**NEVER use Python if/else in component functions**. Always use `rx.cond`:


# ✅ CORRECT
rx.cond(
    State.is_positive,
    rx.el.span("Positive", class_name="text-green-500"),
    rx.el.span("Negative", class_name="text-red-500"),
)

# ✅ Conditional styling
class_name=rx.cond(
    State.is_active,
    "bg-blue-500 text-white",
    "bg-gray-100 text-gray-600",
)

# ❌ WRONG - Never use Python if/else
if state.is_positive:  # BREAKS COMPILATION
    return rx.el.span("Positive")


### 2. List Iteration (`rx.foreach`)

**NEVER use Python for loops or list comprehensions**:


# ✅ CORRECT
rx.foreach(State.items, render_item)
rx.foreach(State.items, lambda item: render_item(item, key=item["id"]))

# ❌ WRONG
[render_item(item) for item in State.items]  # BREAKS


### 3. Multi-Condition Rendering (`rx.match`)

For 3+ conditions:

rx.match(
    notification["type"],
    ("alert", rx.el.div(class_name="bg-amber-100")),
    ("warning", rx.el.div(class_name="bg-yellow-100")),
    ("info", rx.el.div(class_name="bg-blue-100")),
    rx.el.div(class_name="bg-gray-100"),  # default
)


### 4. Module/Subtab Navigation Pattern


# State stores mapping
MODULE_SUBTABS: dict[str, list[str]] = {
    "Market Data": ["Market Data", "FX Data", "Reference Data", ...],
    "PnL": ["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"],
    ...
}

# Computed var returns dynamic subtabs
@rx.var
def current_subtabs(self) -> list[str]:
    return self.MODULE_SUBTABS.get(self.active_module, [])

# UI renders based on active module + subtab
rx.match(
    PortfolioDashboardState.active_module,
    ("PnL", rx.match(
        PortfolioDashboardState.active_subtab,
        ("PnL Change", pnl_change_table()),
        ("PnL Summary", pnl_summary_table()),
        ...
    )),
    ...
)


### 5. Pagination State Pattern


# State vars
current_page: int = 1
page_size: int = 50

@rx.var
def total_pages(self) -> int:
    return (len(self.filtered_data) + self.page_size - 1) // self.page_size

@rx.var
def paginated_data(self) -> list[dict]:
    start = (self.current_page - 1) * self.page_size
    end = start + self.page_size
    return self.filtered_data[start:end]

@rx.event
def next_page(self):
    if self.current_page < self.total_pages:
        self.current_page += 1


### 6. Sparkline SVG Generation


# Generate SVG polyline points from data
points = []
for idx, val in enumerate(sparkline_data):
    x = idx * step
    y = height - normalized * (height - 4)
    points.append(f"{x:.1f},{y:.1f}")
sparkline_svg = " ".join(points)

# Render in component
rx.el.svg(
    rx.el.svg.polyline(
        points=item["sparkline_svg"],
        stroke=item["sparkline_color"],
        fill="none",
    ),
    view_box="0 0 80 24",
)


---

## UI Architecture: 4-Region Layout


┌─────────────────────────────────────────────────────────────────┐
│                    REGION 1: TOP NAVIGATION                      │
│  [Market Data] [Positions] [PnL] [Risk] [Recon] ... (11 modules) │
├─────────────────────────────────────────────────────────────────┤
│                 REGION 2: PERFORMANCE HEADER                     │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐            │
│  │Daily PnL│Pos FX   │CCY Hedged│YTD Disc │YTD R/U  │ [KPI Row]  │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘            │
│  [▼ Show Top Movers - Collapsible 5 mini-grids]                 │
├─────────────────────────────────────────────────────┬───────────┤
│              REGION 3: CONTEXTUAL WORKSPACE         │ REGION 4  │
│  ┌─────────────────────────────────────────────┐   │NOTIF BAR  │
│  │ [Sub-tab 1] [Sub-tab 2] [Sub-tab 3] ...     │   │           │
│  ├─────────────────────────────────────────────┤   │ ┌───────┐ │
│  │ [Generate▼] [Export] [🔄] [Search] [Date]   │   │ │Alert 1│ │
│  ├─────────────────────────────────────────────┤   │ └───────┘ │
│  │                                             │   │ ┌───────┐ │
│  │           DATA TABLE (scrollable)           │   │ │Alert 2│ │
│  │                                             │   │ └───────┘ │
│  ├─────────────────────────────────────────────┤   │    ...    │
│  │ [Rows: 50▼] Page 1 of 8 (400 items) [< >]   │   │[Prev|Next]│
│  └─────────────────────────────────────────────┘   └───────────┘
└─────────────────────────────────────────────────────────────────┘


### Region Implementation Files

| Region | Component | File |
|--------|-----------|------|
| 1 | Top Navigation | `components/top_navigation.py` |
| 2 | Performance Header | `components/performance_header.py` |
| 3 | Contextual Workspace | `components/contextual_workspace.py` |
| 4 | Notification Sidebar | `components/notification_sidebar.py` |

### Layout Container (app.py)


def index() -> rx.Component:
    return rx.el.div(
        top_navigation(),           # Region 1 - sticky top
        performance_header(),       # Region 2 - sticky below nav
        rx.el.div(
            contextual_workspace(), # Region 3 - flex-1
            notification_sidebar(), # Region 4 - fixed width
            class_name="flex flex-1 overflow-hidden",
        ),
        class_name="flex flex-col h-screen w-screen overflow-hidden",
    )


---

## Current Limitations / TODOs

### Incomplete Features

1. **No Real Database**: All data is in-memory mock data. Integration with real trading APIs needed.

2. **Limited Module Implementation**: Only these modules have full subtab content:
   - ✅ PnL (4 views: Change, Full, Summary, Currency)
   - ⚠️ Others use generic mock table

3. **No WebSocket Updates**: Notifications are simulated. Real-time data feed not implemented.

4. **Missing Features**:
   - Export functionality (PDF/CSV) is placeholder
   - Auto-refresh toggle doesn't actually refresh
   - Date filter UI exists but doesn't filter data

5. **Mobile Responsiveness**: Mobile menu exists but layout not optimized for small screens.

### Known Issues

1. **Table Performance**: 400+ row tables may lag. Consider virtualization.

2. **State Persistence**: Navigation state resets on page refresh. No localStorage.

3. **yfinance Rate Limits**: Finance service may hit API limits with frequent refreshes.

### Priority TODOs for Next Agent


[ ] Implement WebSocket for real-time notification updates
[ ] Add proper data filtering by date in contextual_workspace
[ ] Implement CSV/PDF export functionality
[ ] Add remaining 48 module subtab views (currently placeholder)
[ ] Add table row selection with multi-select for bulk actions
[ ] Implement proper error handling for API calls
[ ] Add loading skeletons for better UX


---

## Reflex-Specific Reminders

1. **All UI is Python**: Never write JSX, HTML, or JavaScript directly.

2. **rx.el.* vs rx.***: Use `rx.el.*` (HTML elements) for most components. Use `rx.*` only for special components like `rx.icon`, `rx.recharts.*`.

3. **Event Handlers**: Must be decorated with `@rx.event`. Background tasks use `@rx.event(background=True)`.

4. **Computed Vars**: Use `@rx.var` for derived state. Use `cache=True` for expensive computations.

5. **Cross-State Access**: Always use `await self.get_state(OtherState)` in async methods.

6. **Styling**: Use Tailwind classes via `class_name`. Never use inline `style={}` except for dynamic values.


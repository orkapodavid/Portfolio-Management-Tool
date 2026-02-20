# AGENTS.md — Reflex UI Starter

## Project Overview

This is a Reflex UI starter template with a **dual-package architecture** that separates business logic from UI concerns:

- **`core_pkg/`** — Pure Python business logic (services, models, repositories). Zero Reflex imports.
- **`starter_app/`** — Reflex UI layer (states, components, pages, routing).

### Features

- 4-region layout (nav, header, workspace, notifications)
- 2 demo modules: **Dashboard** (Overview, Analytics) and **Market Data** (FX Data, Reference Data)
- Notification sidebar with filtering, infinite scroll, and jump-to-row navigation
- AG Grid integration with cell flash, compact mode, Excel export, and layout persistence
- Live ticking FX data via background tasks

---

## Quick Start

```bash
cd reflex-ui-starter
uv sync
uv run reflex init    # first time only
uv run reflex run
```

Open `http://localhost:3000` — redirects to `/dashboard/overview`.

### Running Tests

```bash
# Core package tests (no Reflex dependency)
uv run pytest core_pkg/tests_core/ -v
```

---

## Architecture

### Dual-Package Separation

```
┌──────────────────────────────────────────────────────────────┐
│                      starter_app/                            │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │   pages/    │  │ components/ │  │      states/         │ │
│  │  (routing)  │→ │  (UI render)│← │ (Reflex state mgmt)  │ │
│  └─────────────┘  └─────────────┘  └──────────┬───────────┘ │
│                                                │             │
│  ┌─────────────────────────────────────────────┤             │
│  │        starter_app/services/                │             │
│  │  Thin re-exports + UI constants             │             │
│  └─────────────────────────────────────────────┤             │
└────────────────────────────────────────────────┼─────────────┘
                                                 │ imports
┌────────────────────────────────────────────────┼─────────────┐
│                    core_pkg/core/              │             │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┴───────────┐ │
│  │ models/  │  │ repositories/│  │      services/         │ │
│  │ (domain) │← │  (data DAL)  │← │  (business logic)     │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
│                                                              │
│  ⚠️  NO Reflex imports. NO starter_app imports.              │
└──────────────────────────────────────────────────────────────┘
```

### Import Hierarchy

```
core_pkg.core.services → starter_app.services → starter_app.states → starter_app.components
```

**Rules:**
- `core_pkg/` must **never** import from `reflex` or `starter_app`
- `starter_app/states/` calls core services for data; manages Reflex-specific state (loading, error, search)
- `starter_app/components/` reads state vars and renders UI; never calls services directly
- `starter_app/services/` is a thin re-export layer; may also contain UI-specific constants

### Where Does Logic Belong?

| Logic Type | Package | Example |
|-----------|---------|---------|
| Data generation / mock data | `core_pkg/core/services/` | `FxService.generate_tick()` |
| CRUD operations | `core_pkg/core/services/` | `UserService.get_users()` |
| Business calculations | `core_pkg/core/services/` | `AnalyticsService.get_summary_stats()` |
| Reflex state vars (loading, error) | `starter_app/states/` | `FxDataMixin.is_loading_fx` |
| Background tasks / streaming | `starter_app/states/` | `FxDataMixin.fx_tick_loop()` |
| UI rendering | `starter_app/components/` | `fx_data_ag_grid()` |
| Routing / page composition | `starter_app/pages/` | `fx_data_page()` |
| UI constants (icons, colors) | `starter_app/services/` | `NotificationIcon`, `NotificationColor` |
| Grid IDs, route mappings | `starter_app/` | `ag_grid_constants.py` |

---

## 4-Region Layout

| Region | Component | File |
|--------|-----------|------|
| 1. Top Nav | Module tabs, bell, user | `components/shared/top_navigation.py` |
| 2. App Header | KPI strip, top movers | `components/shared/app_header.py` |
| 3. Workspace | Subtab bar + page content | `components/shared/module_layout.py` |
| 4. Notifications | Alert cards, filters | `components/shared/notification_sidebar.py` |

---

## State Management

| State Class | Purpose | File |
|-------------|---------|------|
| `UIState` | Navigation, sidebar toggle, module config | `states/ui/ui_state.py` |
| `AppHeaderState` | KPI data, top movers | `states/ui/app_header_state.py` |
| `DashboardState` | Composes `OverviewMixin` + `AnalyticsMixin` | `states/dashboard/dashboard_state.py` |
| `MarketDataState` | Composes `FxDataMixin` + `ReferenceDataMixin` | `states/market_data/market_data_state.py` |
| `NotificationSidebarState` | Notifications, CRUD, jump-to-row | `states/notifications/notification_sidebar_state.py` |

### Mixin Pattern

Each module composes its state from focused mixins:

```python
# states/market_data/market_data_state.py
class MarketDataState(FxDataMixin, ReferenceDataMixin, rx.State):
    """Composed state for the Market Data module."""

    @rx.event
    async def load_market_data_module_data(self):
        if self.active_market_data_subtab == "FX Data":
            yield type(self).load_fx_data          # ← mixin dispatch pattern
        elif self.active_market_data_subtab == "Reference Data":
            yield type(self).load_reference_data
```

Mixins handle:
- Loading data from core services
- Managing loading/error/search state
- Background tasks (e.g., FX streaming)

### Route `on_load` Pattern

Routes in `starter_app.py` use `on_load` to set the active module/subtab and trigger data loading:

```python
app.add_page(
    analytics_page,
    route="/dashboard/analytics",
    on_load=[
        UIState.set_active_module("Dashboard"),
        DashboardState.set_dashboard_subtab("Analytics"),
        DashboardState.load_dashboard_module_data,      # dispatches to mixin
    ],
    title="Dashboard — Analytics",
)
```

**Key:** The composed state's `load_*_module_data` handler uses `yield type(self).mixin_method` to dispatch to the correct mixin's event handler. Never call mixin handlers via `self.method()` or `ClassName.method` — use `type(self).method`.

---

## Core Services Inventory

| Service | File | Key Methods |
|---------|------|-------------|
| `UserService` | `core/services/user_service.py` | `get_users()`, `get_by_id()`, `get_active_count()` |
| `AnalyticsService` | `core/services/analytics_service.py` | `get_market_data()`, `get_summary_stats()`, `get_column_defs()` |
| `ConfigService` | `core/services/config_service.py` | `get_config()`, `update_config()`, `reset_to_defaults()` |
| `NotificationConfigService` | `core/services/notification_service.py` | `get_preferences()`, `update_preference()`, `get_enabled_channels()` |
| `FxService` | `core/services/fx_service.py` | `get_fx_data()`, `generate_tick()` |
| `ReferenceDataService` | `core/services/reference_data_service.py` | `get_reference_data()` |

---

## AG Grid Configuration

Shared AG Grid components live in `components/shared/ag_grid_config/`:

| File | Purpose |
|------|---------|
| `grid_factory.py` | `create_standard_grid()` — unified grid constructor |
| `toolbar.py` | `grid_toolbar()` — search, export, save/restore, compact toggle |
| `constants.py` | Grid sizing constants (row height, header height) |
| `export_helpers.py` | Excel export JavaScript generation |
| `styles.py` | Cell style functions (change colors, currency formatting) |

Grid IDs and route mappings are in `starter_app/ag_grid_constants.py`.

---

## Notification Jump-to-Row Architecture

The notification sidebar supports clicking a notification to navigate to a specific row in an AG Grid. This works for both same-page and cross-page scenarios.

**How it works:**

1. `navigate_to_item(notif_id)` — checks if the target grid is on the current page
2. **Same page:** Executes JS to find the row via AG Grid API, scroll to it, flash, and apply a persistent highlight
3. **Cross page:** Stores the target in `sessionStorage`, triggers `rx.redirect()`, and the grid's `on_grid_ready` calls `execute_pending_highlight()` to pick it up

**JS helpers** in `notification_sidebar_state.py` (module-level functions, not inline):

| Helper | Purpose |
|--------|---------|
| `_js_clear_highlight()` | Clears existing row highlights |
| `_js_get_grid_api(grid_id)` | AG Grid API lookup via React Fiber traversal |
| `_js_find_and_highlight_row(row_id, key)` | Find row + scroll + flash + persistent highlight |
| `_build_jump_js(grid_id, row_id, key)` | Composes above for `jump_to_row` |
| `_build_navigate_js(grid_id, row_id, key, route)` | Composes above for `navigate_to_item` |

---

## Routing

Routes in `starter_app.py` (the entry point). Each route has:
- Page component function
- `on_load` handlers to set UIState module/subtab and trigger data loading
- Default route (`/`) redirects to `/dashboard/overview`

---

## Styling

- **Tailwind CSS v3** via `rx.plugins.TailwindV3Plugin()`
- Design tokens in `constants.py`
- Inter font via Google Fonts CDN
- All styling via `class_name=` attribute

---

## Adding a New Module

1. Create core service in `core_pkg/core/services/my_service.py`
2. Export it in `core_pkg/core/services/__init__.py`
3. Create a re-export in `starter_app/services/<module>/__init__.py`
4. Create a state mixin in `starter_app/states/<module>/mixins/my_mixin.py`
5. Compose the mixin into the module's state class
6. Create pages in `starter_app/pages/<module>/`
7. Update `UIState.MODULE_SUBTABS` and `MODULE_ICONS` in `states/ui/ui_state.py`
8. Add nav button in `components/shared/top_navigation.py`
9. Add routes in `starter_app.py` with `on_load` handlers
10. Register grid ID in `ag_grid_constants.py` (if using AG Grid)

---

## Key Reflex Rules

1. **NEVER** use Python `if/else` in component render — use `rx.cond()`
2. **NEVER** use Python `for` loops for state data — use `rx.foreach()`
3. State vars MUST be JSON-serializable (no custom classes, no datetime)
4. Use `TypedDict` for structured data in lists
5. Use `@rx.var` for computed properties, `@rx.event` for handlers
6. All pages must use `module_layout()` wrapper
7. Background tasks use `@rx.event(background=True)` with `async with self`
8. Event chaining from mixins: use `yield type(self).handler_name` (not `self.handler()` or `ClassName.handler`)

---

## Directory Structure

```
reflex-ui-starter/
├── starter_app/                    # UI Layer (Reflex)
│   ├── starter_app.py              # Entry point + routes
│   ├── constants.py                # Design tokens
│   ├── ag_grid_constants.py        # Grid IDs, route mappings
│   ├── components/
│   │   ├── shared/                 # 4-region layout + AG Grid config
│   │   │   ├── ag_grid_config/     # Grid factory, toolbar, styles
│   │   │   ├── module_layout.py    # Workspace wrapper
│   │   │   ├── top_navigation.py   # Nav bar
│   │   │   ├── app_header.py       # KPI header strip
│   │   │   └── notification_sidebar.py
│   │   ├── dashboard/              # Dashboard-specific components
│   │   └── market_data/            # Market data grid components
│   ├── pages/
│   │   ├── dashboard/              # Overview, Analytics pages
│   │   └── market_data/            # FX Data, Reference Data pages
│   ├── states/
│   │   ├── ui/                     # UIState, AppHeaderState
│   │   ├── dashboard/              # DashboardState + mixins
│   │   ├── market_data/            # MarketDataState + mixins
│   │   └── notifications/          # NotificationSidebarState
│   └── services/                   # Thin re-exports + UI constants
│       ├── dashboard/              # Re-exports UserService, AnalyticsService
│       ├── market_data/            # Re-exports FxService, ReferenceDataService
│       └── notifications/          # NotificationType, NotificationIcon, NotificationColor
│
├── core_pkg/                       # Business Logic (no Reflex)
│   ├── core/
│   │   ├── models/                 # Domain models
│   │   ├── services/               # All business services
│   │   └── repositories/           # Data access layer
│   ├── tests_core/                 # Core package tests (40 tests)
│   └── pyproject.toml              # Package config
│
├── rxconfig.py                     # Reflex configuration
├── pyproject.toml                  # Project dependencies
└── AGENTS.md                       # This file
```

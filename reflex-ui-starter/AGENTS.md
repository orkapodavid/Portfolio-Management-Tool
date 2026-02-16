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
| 2. Perf Header | KPI strip, top movers | `components/shared/performance_header.py` |
| 3. Workspace | Subtab bar + page content | `components/shared/module_layout.py` |
| 4. Notifications | Alert cards, filters | `components/shared/notification_sidebar.py` |

---

## State Management

| State Class | Purpose | File |
|-------------|---------|------|
| `UIState` | Navigation, sidebar toggle | `states/ui/ui_state.py` |
| `AppHeaderState` | Top nav state | `states/ui/app_header_state.py` |
| `PerformanceHeaderState` | KPI data, movers | `states/ui/performance_header_state.py` |
| `DashboardState` | Composes `OverviewMixin` + `AnalyticsMixin` | `states/dashboard/dashboard_state.py` |
| `MarketDataState` | Composes `FxDataMixin` + `ReferenceDataMixin` | `states/market_data/market_data_state.py` |
| `NotificationSidebarState` | Notifications, CRUD, jump-to-row | `states/notifications/notification_sidebar_state.py` |

### Mixin Pattern

Each module composes its state from focused mixins:

```python
# states/market_data/market_data_state.py
class MarketDataState(FxDataMixin, ReferenceDataMixin, rx.State):
    """Composed state for the Market Data module."""
    ...
```

Mixins handle:
- Loading data from core services
- Managing loading/error/search state
- Background tasks (e.g., FX streaming)

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

## Routing

Routes in `starter_app.py`. Each route has:
- Page component function
- `on_load` handlers to set UIState module/subtab
- Default route (`/`) redirects to `/dashboard/overview`

---

## Styling

- **Tailwind CSS v3** via `rx.plugins.TailwindV3Plugin()`
- Design tokens in `constants.py`
- Inter font via Google Fonts CDN
- All styling via `class_name=` attribute

---

## Key Reflex Rules

1. **NEVER** use Python `if/else` in component render — use `rx.cond()`
2. **NEVER** use Python `for` loops for state data — use `rx.foreach()`
3. State vars MUST be JSON-serializable (no custom classes, no datetime)
4. Use `TypedDict` for structured data in lists
5. Use `@rx.var` for computed properties, `@rx.event` for handlers
6. All pages must use `module_layout()` wrapper
7. Background tasks use `@rx.event(background=True)` with `async with self`
8. Event chaining from mixins: use `type(self).handler_name` (not `ClassName.handler`)

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
│   │   │   ├── performance_header.py
│   │   │   └── notification_sidebar.py
│   │   ├── dashboard/              # Dashboard-specific components
│   │   └── market_data/            # Market data grid components
│   ├── pages/
│   │   ├── dashboard/              # Overview, Analytics pages
│   │   └── market_data/            # FX Data, Reference Data pages
│   ├── states/
│   │   ├── ui/                     # UIState, PerformanceHeaderState
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
│   ├── tests_core/                 # Core package tests
│   └── pyproject.toml              # Package config
│
├── rxconfig.py                     # Reflex configuration
├── pyproject.toml                  # Project dependencies
└── AGENTS.md                       # This file
```

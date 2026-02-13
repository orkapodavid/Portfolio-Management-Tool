# AGENTS.md — Reflex UI Starter

## Project Overview

This is a Reflex UI starter template. It provides:
- 4-region layout (nav, header, workspace, notifications)
- 2 demo modules: Dashboard (Overview, Analytics) and Settings (General, Notifications)
- Notification sidebar with filtering and infinite scroll
- AG Grid integration example
- Core business logic package (`core_pkg/`)

## Architecture

### 4-Region Layout

| Region | Component | File |
|--------|-----------|------|
| 1. Top Nav | Module tabs, bell, user | `components/shared/top_navigation.py` |
| 2. Perf Header | KPI strip, top movers | `components/shared/performance_header.py` |
| 3. Workspace | Subtab bar + page content | `components/shared/module_layout.py` |
| 4. Notifications | Alert cards, filters | `components/shared/notification_sidebar.py` |

### State Management

| State Class | Purpose | File |
|-------------|---------|------|
| `UIState` | Navigation, sidebar | `states/ui/ui_state.py` |
| `PerformanceHeaderState` | KPI data, movers | `states/ui/performance_header_state.py` |
| `NotificationSidebarState` | Notifications, CRUD | `states/notifications/notification_sidebar_state.py` |
| `AnalyticsState` | AG Grid demo data | `pages/dashboard/analytics_page.py` |

### Routing Pattern

Routes are defined in `app.py`. Each route has:
- Page component function
- `on_load` handlers to set UIState module/subtab
- Default route (`/`) redirects to `/dashboard/overview`

### Styling

- **Tailwind CSS v3** via `rx.plugins.TailwindV3Plugin()`
- Design tokens in `constants.py`
- Inter font via Google Fonts CDN
- All styling via `class_name=` attribute

## Key Reflex Rules

1. **NEVER** use Python `if/else` in component render — use `rx.cond()`
2. **NEVER** use Python `for` loops for state data — use `rx.foreach()`
3. State vars MUST be JSON-serializable (no custom classes, no datetime)
4. Use `TypedDict` for structured data in lists
5. Use `@rx.var` for computed properties, `@rx.event` for handlers
6. All pages must use `module_layout()` wrapper

## Directory Structure

```
starter_app/
├── app.py                 # Entry point + routes
├── constants.py           # Design tokens
├── components/shared/     # All 4 layout regions
├── pages/                 # Module pages
│   ├── dashboard/         # Overview, Analytics
│   └── settings/          # General, Notifications
├── states/                # Reflex state classes
│   ├── ui/                # UIState, PerformanceHeaderState
│   └── notifications/     # NotificationSidebarState
└── services/              # App-layer services
    └── notifications/     # Notification enums

core_pkg/core/             # Business logic (no Reflex imports)
├── models/                # Domain models
├── services/              # Business services
└── repositories/          # Data access
```

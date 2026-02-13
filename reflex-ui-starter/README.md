# Reflex UI Starter

A fresh Reflex UI starter template with tabbed navigation, notification sidebar, performance header, and AG Grid integration.

## Quick Start

```bash
cd reflex-ui-starter
uv sync
uv run reflex init
uv run reflex run
```

Open `http://localhost:3000` — redirects to `/dashboard/overview`.

## Features

- **Dark Top Navigation** — Module tabs with icons, notification bell, mobile menu
- **Performance Header** — KPI cards with sparklines, portfolio summary, top movers
- **Notification Sidebar** — Alert cards with filtering, infinite scroll, mark read, dismiss, simulate
- **Subtab Navigation** — Per-module subtabs with URL routing
- **AG Grid Integration** — Demo market data grid on Analytics page
- **Responsive** — Mobile hamburger menu, collapsible sidebar

## Project Structure

```
reflex-ui-starter/
├── starter_app/           # Reflex UI app
│   ├── app.py             # Routes: Dashboard (Overview, Analytics), Settings (General, Notifications)
│   ├── constants.py       # Design tokens (colors, heights, fonts)
│   ├── components/shared/ # Layout, nav, sidebar, header
│   ├── pages/             # Dashboard + Settings pages
│   ├── states/            # UIState, NotificationSidebarState, PerformanceHeaderState
│   └── services/          # Notification constants
├── core_pkg/              # Business logic (models, services, repositories)
├── reflex_ag_grid/        # AG Grid component (workspace member)
├── docs/                  # Architecture guide + setup docs
├── .agents/               # Agent skills, rules, workflows
├── rxconfig.py            # Reflex config (Tailwind v3, Inter font)
└── pyproject.toml         # Dependencies + uv workspace
```

## Adding a New Module

1. Add pages in `starter_app/pages/your_module/`
2. Update `UIState.MODULE_SUBTABS` and `MODULE_ICONS` in `states/ui/ui_state.py`
3. Add nav button in `components/shared/top_navigation.py`
4. Add routes in `app.py`

## Docs

- [Development Setup](docs/setups/development-setup.md)
- [Architecture Guide](docs/style_guides/reflex-architecture-guide.md)

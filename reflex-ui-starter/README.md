# Reflex UI Starter

A Reflex UI starter template with tabbed navigation, notification sidebar, KPI header, and AG Grid integration.

## Quick Start

```bash
cd reflex-ui-starter
uv sync
uv run reflex init
uv run reflex run
```

Open `http://localhost:3000` — redirects to `/dashboard/overview`.

### Running Tests

```bash
# Core business logic tests (no Reflex dependency)
uv run pytest core_pkg/tests_core/ -v
```

## Features

- **Dark Top Navigation** — Module tabs with icons, notification bell, mobile menu
- **KPI Header** — KPI cards with sparklines, portfolio summary, top movers
- **Notification Sidebar** — Alert cards with filtering, infinite scroll, jump-to-row navigation
- **Subtab Navigation** — Per-module subtabs with URL routing
- **AG Grid Integration** — Market data, FX data, and reference data grids
- **Live FX Streaming** — Ticking FX price data via background tasks
- **Responsive** — Mobile hamburger menu, collapsible sidebar

## Project Structure

```
reflex-ui-starter/
├── starter_app/           # Reflex UI app
│   ├── starter_app.py     # Entry point + routes
│   ├── constants.py       # Design tokens (colors, heights, fonts)
│   ├── ag_grid_constants.py  # Grid IDs, route mappings
│   ├── components/shared/ # Layout, nav, sidebar, header, AG Grid config
│   ├── pages/             # Dashboard + Market Data pages
│   ├── states/            # UIState, AppHeaderState, module states + mixins
│   └── services/          # Re-exports + notification constants
├── core_pkg/              # Business logic (models, services, repositories)
├── docs/                  # Architecture guide + setup docs
├── .agents/               # Agent skills, rules, workflows
├── rxconfig.py            # Reflex config (Tailwind v3, Inter font)
└── pyproject.toml         # Dependencies + uv workspace
```

## Adding a New Module

1. Create core service in `core_pkg/core/services/my_service.py`
2. Export in `core_pkg/core/services/__init__.py`
3. Re-export in `starter_app/services/<module>/__init__.py`
4. Create state mixin in `starter_app/states/<module>/mixins/`
5. Compose mixin into module state class
6. Add pages in `starter_app/pages/<module>/`
7. Update `UIState.MODULE_SUBTABS` and `MODULE_ICONS` in `states/ui/ui_state.py`
8. Add nav button in `components/shared/top_navigation.py`
9. Add routes in `starter_app.py` with `on_load` handlers

## Docs

- [Development Setup](docs/setups/development-setup.md)
- [Architecture Guide](docs/style_guides/reflex-architecture-guide.md)
- [AGENTS.md](AGENTS.md) — Full architecture and agent instructions

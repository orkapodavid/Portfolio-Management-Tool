# Development Setup

## Prerequisites

- Python 3.13 (recommended) or 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ (for Reflex frontend)

## Quick Start

```bash
cd reflex-ui-starter

# Install dependencies
uv sync

# Initialize Reflex
uv run reflex init

# Run the app
uv run reflex run
```

Open `http://localhost:3000` in your browser.

## Running Tests

```bash
# Core business logic tests (no Reflex dependency)
uv run pytest core_pkg/tests_core/ -v
```

## Environment Variables

Copy `.env.example` to `.env` and adjust:

| Variable | Default | Description |
|----------|---------|-------------|
| `REFLEX_FRONTEND_PORT` | 3000 | Frontend port |
| `REFLEX_BACKEND_PORT` | 8000 | Backend port |
| `API_URL` | `http://localhost:8000` | API URL for websockets |
| `REFLEX_STATE_MANAGER_MODE` | `memory` | State manager (`memory` or `redis`) |

## Project Structure

```
reflex-ui-starter/
├── starter_app/           # Reflex UI application
│   ├── starter_app.py     # Entry point + routes
│   ├── constants.py       # Design tokens
│   ├── ag_grid_constants.py  # Grid IDs, route mappings
│   ├── components/        # Reusable UI components
│   │   └── shared/        # Layout, nav, sidebar, header, AG Grid config
│   ├── pages/             # Page components
│   │   ├── dashboard/     # Dashboard module pages
│   │   └── market_data/   # Market Data module pages
│   ├── states/            # Reflex state classes
│   │   ├── ui/            # UIState, AppHeaderState
│   │   ├── dashboard/     # DashboardState + mixins
│   │   ├── market_data/   # MarketDataState + mixins
│   │   └── notifications/ # NotificationSidebarState
│   └── services/          # Re-exports + app-layer constants
├── core_pkg/              # Business logic package
│   ├── core/              # Models, services, repos
│   └── tests_core/        # Unit tests (40 tests)
├── docs/                  # Documentation
├── .agents/               # Agent skills and rules
├── rxconfig.py            # Reflex config
└── pyproject.toml         # Project dependencies
```

## Adding a New Module

1. Create core service in `core_pkg/core/services/my_service.py`
2. Export in `core_pkg/core/services/__init__.py`
3. Re-export in `starter_app/services/<module>/__init__.py`
4. Create state mixin in `starter_app/states/<module>/mixins/`
5. Compose mixin into module state class
6. Add pages in `starter_app/pages/<module>/`
7. Update `UIState.MODULE_SUBTABS` and `MODULE_ICONS`
8. Add nav entry in `top_navigation.py`
9. Add routes in `starter_app.py` with `on_load` handlers

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
│   ├── app.py             # Routes and app config
│   ├── constants.py       # Design tokens
│   ├── components/        # Reusable UI components
│   │   └── shared/        # Layout, nav, sidebar, header
│   ├── pages/             # Page components
│   │   ├── dashboard/     # Dashboard module pages
│   │   └── settings/      # Settings module pages
│   ├── states/            # Reflex state classes
│   │   ├── ui/            # UI state (nav, sidebar)
│   │   └── notifications/ # Notification state
│   └── services/          # App-layer services
├── core_pkg/              # Business logic package
│   └── core/              # Models, services, repos
├── reflex_ag_grid/        # AG Grid component
├── docs/                  # Documentation
├── .agents/               # Agent skills and rules
├── rxconfig.py            # Reflex config
└── pyproject.toml         # Project dependencies
```

## Adding a New Module

1. Create page files in `starter_app/pages/your_module/`
2. Add module to `UIState.MODULE_SUBTABS` and `UIState.MODULE_ICONS`
3. Add nav entry in `top_navigation.py`
4. Add routes in `app.py`

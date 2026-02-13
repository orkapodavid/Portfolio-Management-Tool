# Project Rules

## Code Style
- Use Python type hints everywhere
- Use `TypedDict` for structured state data
- Docstrings on all public functions and classes
- Constants in `constants.py`, not hardcoded

## Architecture
- UI code in `starter_app/` — no direct DB or API calls
- Business logic in `core_pkg/core/` — no Reflex imports
- Services bridge UI and core: `starter_app/services/`
- States in `starter_app/states/` — one dir per domain

## Reflex Patterns
- All pages wrapped in `module_layout()`
- Use `@rx.event` for event handlers
- Use `@rx.var` for computed state
- Tailwind v3 via `class_name=` strings only
- No inline `style=` dicts unless absolutely necessary

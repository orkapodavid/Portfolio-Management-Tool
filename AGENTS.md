# Agents Guide

This repository is designed to be friendly to AI agents.

## Project Overview
Portfolio Management Tool built with **Reflex** (Python web framework) for managing financial positions, compliance, risk, and operations.

## Project Structure
```
[root]
├── app/                      # Reflex application
│   ├── pages/[module]/       # Entry points
│   ├── states/[module]/      # State management
│   ├── services/[module]/    # Business logic wrappers
│   └── components/[module]/  # UI components
├── pmt_core_pkg/pmt_core/    # Shared business logic (installed as pmt_core)
│   ├── models/[module]/      # TypedDicts, enums, data structures
│   ├── services/[module]/    # Core business logic
│   └── repositories/[module]/# Data access layer
├── tests/                    # Application-level tests
├── docs/                     # Design documents
└── .agents/                  # Agent skills and resources
```

**Modules**: `positions`, `pnl`, `risk`, `compliance`, `market_data`, `notifications`, etc.

## Development
```bash
uv run reflex run              # Run app (http://localhost:3001/pmt/)
uv sync --group dev && uv run pytest  # Run tests
uv pip install -e ./pmt_core_pkg      # Install pmt_core editable
```

## Database
MS SQL Server (external) via `DATABASE_URL` environment variable.

## Key Navigation
Top Nav: Positions | Compliance | PnL | Risk | Portfolio Tools | Market Data | Instrument | Events | Operations | Orders

Global: Header Dashboard (metrics) + Notifications Sidebar (alerts)

---

## State Architecture Best Practices

**Reference**: `.agents/skills/reflex-dev/references/reflex-state-structure.mdc`

### Core Principles
1. **Flat State Structure**: States inherit from `rx.State` directly, avoid deep hierarchies
2. **Separation of Concerns**: One state per feature, use `get_state()` for cross-state access
3. **Service Layer**: States delegate to services → Pattern: State → Service → Database/API

### State Pattern
```python
class PnLState(rx.State):
    data: list[dict] = []
    is_loading: bool = False
    
    async def on_load(self):
        self.is_loading = True
        try:
            self.data = await PnLService().get_pnl_data()
        finally:
            self.is_loading = False
```

### Common Pitfalls

| ❌ Don't | ✅ Do |
|----------|-------|
| Create mega-states (1000+ lines) | Break into focused substates (~200-400 lines) |
| Mix UI logic with business logic | Delegate to service classes |
| Load all data on startup | Use `on_load()` for lazy loading |
| Deep inheritance hierarchies | Flat structure + `get_state()` |
| Tailwind sizes (`"lg"`, `"md"`) for Radix props | Numeric strings `'1'`-`'9'` for size props |
| Raw string literals (`"category": "Alerts"`) | StrEnums + TypedDicts for type safety |

### Type Safety
Define constants with `StrEnum` and `TypedDict` for:
- **Autocomplete** in IDE
- **Refactoring safety** (rename propagates)
- **Runtime validation**

Examples: `app/ag_grid_constants.py`, `app/services/notifications/notification_constants.py`

### Error Handling
Use custom exceptions from `app/exceptions.py`: `PMTError`, `DatabaseConnectionError`, `DataExtractionError`, `ServiceUnavailableError`

---

## Current Blockers

| Resource | Blocks |
|----------|--------|
| PyQt Source (`source/`) | Service adapters, ReportClass |
| Database Access | Database connectivity |
| Config Files (`resources/config/`) | Config migration |
| Bloomberg Terminal | EMSX integration |

See `docs/milestone-1-pre-integration-checklist.md` for details.

---

## References
- `pmt_core_pkg/README.md` - Shared package docs
- `docs/style_guides/reflex-architecture-guide.md` - Architecture patterns
- `app/states/pnl/pnl_state.py` - Exemplar implementation
- `app/states/types.py` - Shared TypedDicts

---

## Superpowers System

<EXTREMELY_IMPORTANT>
You have superpowers. To load your skills, run at start of any task:
node .agents/skills/superpowers/bootstrap.js

Follow the instructions it returns.
</EXTREMELY_IMPORTANT>

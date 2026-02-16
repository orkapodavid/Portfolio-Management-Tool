# Agents Guide

This repository is designed to be friendly to AI agents.

## Project Overview
Portfolio Management Tool built with **Reflex** (Python web framework) for managing financial positions, compliance, risk, and operations.

> **CRITICAL**: This is a **Reflex** application. The UI is written entirely in Python but compiles to React/Next.js. DO NOT write raw HTML, JavaScript, or React components. All UI must use `rx.*` components.

---

## ⚠️ Architecture: Dual-Package Separation

> **THE GOLDEN RULE**: Business / backend logic lives in **`pmt_core_pkg/pmt_core/`**. UI / UX logic lives in **`app/`**. Never mix them.

```
┌───────────────────────────────────────────────────────────────┐
│                          app/                                 │
│  ┌────────────┐  ┌─────────────┐  ┌────────────────────────┐ │
│  │   pages/   │  │ components/ │  │       states/          │ │
│  │ (routing)  │→ │ (UI render) │← │ (Reflex state mgmt)    │ │
│  └────────────┘  └─────────────┘  └──────────┬─────────────┘ │
│                                               │               │
│  ┌────────────────────────────────────────────┤               │
│  │            app/services/                   │               │
│  │  Thin adapters — call pmt_core services    │               │
│  │  May add UI-specific constants, caching    │               │
│  └────────────────────────────────────────────┤               │
└───────────────────────────────────────────────┼───────────────┘
                                                │ imports
┌───────────────────────────────────────────────┼───────────────┐
│                pmt_core_pkg/pmt_core/         │               │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┴─────────────┐ │
│  │ models/  │  │repositories/ │  │       services/          │ │
│  │ (domain) │← │  (data DAL)  │← │  (business logic)       │ │
│  └──────────┘  └──────────────┘  └──────────────────────────┘ │
│                                                               │
│  ⚠️  NO Reflex imports. NO app/ imports.                      │
└───────────────────────────────────────────────────────────────┘
```

### Import Hierarchy (one-way)

```
pmt_core.services → app.services → app.states → app.components
```

- `pmt_core_pkg/` must **NEVER** import from `reflex` or `app/`
- `app/states/` calls core services for data; manages Reflex-specific state (loading, error, search)
- `app/components/` reads state vars and renders UI; never calls services directly
- `app/services/` is a thin adapter layer; may add caching, error wrapping, or UI-specific constants

### Where Does Logic Belong?

| Logic Type | Package | Example |
|-----------|---------|--------|
| Data models, TypedDicts, Enums | `pmt_core/models/` | `PositionRecord`, `InstrumentType` |
| Data access (DB, API, files) | `pmt_core/repositories/` | `PositionsRepository.fetch()` |
| Business rules, calculations | `pmt_core/services/` | `PricingService.calculate_pnl()` |
| Logging utilities | `pmt_core/utilities/` | `get_logger()` |
| Reflex state vars (loading, error) | `app/states/` | `PnLState.is_loading` |
| Background tasks / streaming | `app/states/` | `MarketDataState.auto_refresh()` |
| UI rendering | `app/components/` | `positions_grid()` |
| Routing / page composition | `app/pages/` | `pnl_page()` |
| Grid IDs, notification icons | `app/` | `ag_grid_constants.py` |
| Service adapters (thin wrappers) | `app/services/` | `app.services.pnl` wraps `pmt_core.services.pnl` |

---

## Project Structure
```
[root]
├── app/                      # UI / UX Layer (Reflex)
│   ├── pages/[module]/       # Route entry points
│   ├── states/[module]/      # Reflex state management
│   ├── services/[module]/    # Thin adapters wrapping pmt_core services
│   ├── components/[module]/  # UI components
│   ├── ag_grid_constants.py  # Grid IDs, route mappings
│   └── exceptions.py        # App-level custom exceptions
├── pmt_core_pkg/pmt_core/    # Business / Backend Logic (NO Reflex)
│   ├── models/[module]/      # TypedDicts, enums, data structures
│   ├── services/[module]/    # Core business logic & calculations
│   ├── repositories/[module]/# Data access layer (DB, API, files)
│   └── utilities/            # Logging, helpers
├── tests/                    # Application-level tests
├── docs/                     # Design documents
└── .agents/                  # Agent skills and resources
```

**Modules**: `positions`, `pnl`, `risk`, `compliance`, `market_data`, `notifications`, `instruments`, `events`, `operations`, `emsx`, `portfolio_tools`, `reconciliation`, etc.

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

## UI Architecture: 4-Region Layout

```
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
│  │           DATA TABLE (scrollable)           │   │ ┌───────┐ │
│  ├─────────────────────────────────────────────┤   │ │Alert 2│ │
│  │ [Rows: 50▼] Page 1 of 8 (400 items) [< >]   │   │ └───────┘ │
│  └─────────────────────────────────────────────┘   └───────────┘
└─────────────────────────────────────────────────────────────────┘
```

| Region | Component | File |
|--------|-----------|------|
| 1 | Top Navigation | `components/top_navigation.py` |
| 2 | Performance Header | `components/performance_header.py` |
| 3 | Contextual Workspace | `components/contextual_workspace.py` |
| 4 | Notification Sidebar | `components/notification_sidebar.py` |

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

## Reflex UI Patterns

### Conditional Rendering (`rx.cond`)

**NEVER use Python if/else in component functions**. Always use `rx.cond`:

```python
# ✅ CORRECT
rx.cond(
    State.is_positive,
    rx.el.span("Positive", class_name="text-green-500"),
    rx.el.span("Negative", class_name="text-red-500"),
)

# ❌ WRONG - Never use Python if/else
if state.is_positive:  # BREAKS COMPILATION
    return rx.el.span("Positive")
```

### List Iteration (`rx.foreach`)

**NEVER use Python for loops or list comprehensions**:

```python
# ✅ CORRECT
rx.foreach(State.items, render_item)

# ❌ WRONG
[render_item(item) for item in State.items]  # BREAKS
```

### Multi-Condition Rendering (`rx.match`)

```python
rx.match(
    notification["type"],
    ("alert", rx.el.div(class_name="bg-amber-100")),
    ("warning", rx.el.div(class_name="bg-yellow-100")),
    ("info", rx.el.div(class_name="bg-blue-100")),
    rx.el.div(class_name="bg-gray-100"),  # default
)
```

### Reflex-Specific Reminders

1. **All UI is Python**: Never write JSX, HTML, or JavaScript directly.
2. **`rx.el.*` vs `rx.*`**: Use `rx.el.*` (HTML elements) for most components. Use `rx.*` only for special components like `rx.icon`, `rx.recharts.*`.
3. **Event Handlers**: Must be decorated with `@rx.event`. Background tasks use `@rx.event(background=True)`.
4. **Computed Vars**: Use `@rx.var` for derived state. Use `cache=True` for expensive computations.
5. **Cross-State Access**: Always use `await self.get_state(OtherState)` in async methods.
6. **Styling**: Use Tailwind classes via `class_name`. Never use inline `style={}` except for dynamic values.

---

## Critical Troubleshooting

### PyO3 / Tokio Panic with Background Tasks

**Issue**: Using a `while True` loop inside a `@rx.event(background=True)` handler can cause the application to crash with a `tokio-runtime-worker` panic:
`"Cannot drop pointer into Python heap without the thread being attached to the Python interpreter"`

**Solution**: Use the **Recursive Event Pattern** instead of an infinite loop.

**❌ BAD (Unsafe):**
```python
@rx.event(background=True)
async def start_auto_refresh(self):
    while True:  # <--- CAUSES PANIC
        async with self:
            if not self.active: break
            self.refresh_data()
        await asyncio.sleep(2)
```

**✅ GOOD (Safe):**
```python
@rx.event(background=True)
async def run_refresh_step(self):
    async with self:
        if not self.active: return
        self.refresh_data()
    
    await asyncio.sleep(2)
    return type(self).run_refresh_step  # Recursively schedule next step
```

---

## Current Blockers

| Resource | Blocks |
|----------|--------|
| PyQt Source (`source/`) | Service adapters, ReportClass |
| Database Access | Database connectivity |
| Config Files (`resources/config/`) | Config migration |
| Bloomberg Terminal | EMSX integration |

See `docs/todos/milestone-1-pre-integration-checklist.md` for details.

---

## References
- `docs/index.md` - **Documentation index** (start here)
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


# Agents Guide

This repository is designed to be friendly to AI agents.

## Project Overview
This is a Portfolio Management Tool built with **Reflex** (Python web framework). It features a dashboard for managing financial positions, compliance, risk, and operations.

## Project Structure
- `app/`: Source code for the Reflex application.
- `pmt_core_pkg/`: Shared business logic package (installed as `pmt_core`).
- `tests/`: Application-level tests.
- `docs/`: Specific requirements and design documents.
- `pyproject.toml`: Dependency management using `uv`.
- `rxconfig.py`: Reflex configuration.
- `.agents/`: Contains skills and other agent-specific resources.
 
 ## Page/Tab Folder Architecture
 
 To ensure scalability and maintainability, **all Python scripts must be layered by folder based on the pages/tab implementation.** taking inspiration from `docs/style_guides/reflex-module-layout-tabs-prompt.md`.
 
 ### Rule
 Every functional layer (`pages`, `states`, `services`, `components`) in `app/` and equivalent layers in `pmt_core/` (`models`, `services`, `repositories`) must be organized into **module-specific subdirectories**.
 
 ### Structure Pattern
 
 ```
 [root]
 ├── app/
 │   ├── pages/[module]/         # Entry points for the module
 │   ├── states/[module]/        # State management for the module
 │   ├── services/[module]/      # Business logic wrappers / API calls
 │   └── components/[module]/    # Module-specific UI components
 └── pmt_core_pkg/
    └── pmt_core/
        ├── models/[module]/        # Domain models for the module
        ├── services/[module]/      # Core business logic
        └── repositories/[module]/  # Data access layer
 ```
 
 **Modules** correspond to the main tabs in the application (e.g., `positions`, `pnl`, `risk`, `compliance`, `market_data`).
 
 ### Example: Compliance Module
 - `app/pages/compliance/`
 - `app/states/compliance/`
 - `app/services/compliance/`
 - `pmt_core_pkg/pmt_core/models/compliance/`
 - `pmt_core_pkg/pmt_core/services/compliance/`
 - `pmt_core_pkg/pmt_core/repositories/compliance/`

## Development
- **Package Manager**: `uv`
- **Run Command**: `uv run reflex run`
- **Frontend**: http://localhost:3001/pmt/
- **Backend**: http://0.0.0.0:8001

## pmt_core Package

The `pmt_core` package contains shared business logic that can be used by both the Reflex web app and future PyQt integration.

### Installation
```powershell
# Install pmt_core in editable mode
uv pip install -e ./pmt_core_pkg
```

### Package Structure
```
pmt_core_pkg/
└── pmt_core/
    ├── models/       # TypedDicts, enums, data structures
    ├── services/     # Business logic
    ├── repositories/ # Data access
    ├── resources/    # Configuration templates
    └── utilities/    # Logging, config helpers
    └── tests_core/   # Package-level tests
```

### Usage
```python
from pmt_core import (
    PositionRecord, PnLRecord, MarketDataRecord,
    InstrumentType, DashboardSection, OrderStatus
)

# Use types for type hints
def process_position(pos: PositionRecord) -> None:
    if pos["sec_type"] == InstrumentType.STOCK:
        pass
```

## Testing

### Run All Tests
```powershell
# Install test dependencies
uv sync --group dev

# Run all tests
uv run pytest
```

### Test Structure
```
tests/
├── conftest.py          # Shared fixtures
└── services/            # Service tests

pmt_core_pkg/tests_core/
├── conftest.py          # pmt_core fixtures
├── test_models.py       # Type and enum tests
└── test_init.py         # Package init tests
```

## Database

This application uses **MS SQL Server** hosted externally (not SQLite or any local database).

- **Connection**: Configured via `DATABASE_URL` environment variable
- **Driver**: ODBC Driver 17 for SQL Server
- **Backup**: Managed externally by database administrators
- **Migrations**: Run via `reflex db migrate` (connects to remote MS SQL)

Example connection string format:
```
mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

## Current Blockers

The following external resources are **not yet available** and block certain integration tasks:

| Resource | Status | Blocks |
|----------|--------|--------|
| PyQt Source Code (`source/`) | Unavailable | Service adapters, ReportClass integration |
| Database Access (MS SQL Server) | Unavailable (hosted externally) | Database connectivity |
| Configuration Files (`resources/config/`) | Unavailable | Config migration |
| Bloomberg Terminal | Unavailable | EMSX integration |

See `docs/milestone-1-pre-integration-checklist.md` for full details.

## Key Features & Navigation
The application uses a **Top Navigation Bar** with icons to switch between views:
- **Positions**: View holdings (Stocks, Warrants, Bonds). Includes "Generate Positions" button.
- **Compliance**: Restricted lists and undertakings.
- **PnL**: Profit and Loss analysis.
- **Risk**: Delta change and risk measures.
- **Portfolio Tools**: Pay-To-Hold and settlement views.
- **Market Data**, **Instrument**, **Events**, **Operations**, **Orders**: Additional functional modules.

**Global Elements**:
- **Header Dashboard**: Key metrics summary at the top.
- **Notifications Sidebar**: Real-time alerts on the right.

## Verification
1. Run the app: `uv run reflex run`.
2. Browse to `http://localhost:3001/pmt/`.
3. Verify that the Dashboard and Top Navigation load.
4. Click through the icons to ensure data tables render.
5. Check the Notifications Sidebar for alerts.

---

## Reflex State Architecture Best Practices

**Reference**: `.agents/skills/reflex-dev/references/reflex-state-structure.mdc`

This project follows Reflex best practices for state management to ensure scalability, maintainability, and performance.

### Core Principles

1. **Flat State Structure**
   - Keep most substates directly inheriting from `rx.State`
   - Avoid deep inheritance hierarchies
   - Each state should be independent and focused

2. **Separation of Concerns**
   - One state class per major feature or page
   - Each state handles only its own data and logic
   - Use `get_state()` to access other states when needed

3. **Service Layer Integration**
   - States should NOT contain business logic
   - States delegate to service classes for data operations
   - Pattern: State → Service → Database/API

### State Organization Pattern

```python
# ✅ GOOD: Focused, independent states
class PnLState(rx.State):
    """Handles only P&L data."""
    pnl_data: list[dict] = []
    is_loading: bool = False
    
    async def load_data(self):
        service = PnLService()
        self.pnl_data = await service.get_pnl_data()

class PositionsState(rx.State):
    """Handles only positions data."""
    positions: list[dict] = []
    
    async def load_data(self):
        service = PositionService()
        self.positions = await service.get_positions()
```

```python
# ❌ BAD: Single mega-state with everything
class DashboardState(rx.State):
    """Handles EVERYTHING - anti-pattern!"""
    pnl_data: list[dict] = []
    positions: list[dict] = []
    risk_data: list[dict] = []
    compliance_data: list[dict] = []
    # ... thousands of lines
```

### Performance Optimization

**State Loading Behavior**:
- When an event handler is called, Reflex loads:
  1. The substate containing the event handler
  2. All parent states (if inheriting)
  3. All child substates of the parent

**Optimization Rules**:
1. **Use `on_load()`**: Load data only when view is accessed
2. **Flat Structure**: Avoid inheritance; use `get_state()` instead
3. **Computed Vars**: Place in leaf states, use `cache=True`
4. **Separate Views**: Different features = different state classes

### Accessing Other States

```python
class GreeterState(rx.State):
    message: str = ""
    
    async def greet(self, name: str):
        # Access another state's data
        settings = await self.get_state(SettingsState)
        self.message = f"{settings.salutation}, {name}!"
```

### Project Structure Example

```
app/states/
├── dashboard/
│   ├── types.py              # Shared TypedDict definitions
│   ├── pnl_state.py          # P&L data and operations
│   ├── positions_state.py    # Position data
│   ├── risk_state.py         # Risk metrics
│   └── compliance_state.py   # Compliance data
├── portfolio/
│   ├── portfolio_state.py
│   ├── watchlist_state.py
│   └── goals_state.py
└── user/
    ├── profile_state.py
    └── settings_state.py
```

###  Service Layer Pattern

Every state should use services for data access:

```python
import reflex as rx
from app.services import PnLService

class PnLState(rx.State):
    data: list[dict] = []
    is_loading: bool = False
    
    async def on_load(self):
        """Load data when view first accessed."""
        await self.load_data()
    
    async def load_data(self):
        """Service integration pattern."""
        self.is_loading = True
        try:
            service = PnLService()
            self.data = await service.get_pnl_data()
        except Exception as e:
            logging.exception(f"Error loading: {e}")
        finally:
            self.is_loading = False
```

### Common Pitfalls to Avoid

❌ **Don't**: Create mega-states with thousands of lines  
✅ **Do**: Break into focused substates (~200-400 lines each)

❌ **Don't**: Mix UI logic with business logic in states  
✅ **Do**: Delegate business logic to service classes

❌ **Don't**: Load all data on app startup  
✅ **Do**: Use `on_load()` to load data when needed

❌ **Don't**: Create deep inheritance hierarchies  
✅ **Do**: Keep flat structure, use `get_state()` for cross-state access

❌ **Don't**: Use Tailwind-style sizes (`"lg"`, `"md"`, `"sm"`) for Radix component props like `rx.heading(size=...)`  
✅ **Do**: Use numeric string values `'1'` through `'9'` for Radix component size props (e.g., `rx.heading("Title", size="5")`)

### Error Handling

Use the custom exception hierarchy defined in `app/exceptions.py`:

```python
from app.exceptions import (
    PMTError,
    DatabaseConnectionError,
    DataExtractionError,
    ServiceUnavailableError,
)

try:
    data = await service.fetch_data()
except DatabaseConnectionError as e:
    logger.error(f"Database error: {e}")
except PMTError as e:
    logger.error(f"Application error: {e}")
```

### References

- **pmt_core Package**: `pmt_core/README.md` - Shared package documentation
- **Milestone 1 Checklist**: `docs/milestone-1-pre-integration-checklist.md` - Pre-integration tasks
- **Reflex Architecture Guide**: `docs/style_guides/reflex-architecture-guide.md` - Comprehensive patterns for layout, state, services, components, and styling
- **Style Migration Prompts**: `docs/style_guides/reflex-style-migration-prompts.md` - Prompt templates for applying architecture patterns
- **Reflex State Structure Guide**: `.agents/skills/reflex-dev/references/reflex-state-structure.mdc`
- **Example Implementation**: `app/states/pnl/pnl_state.py` (exemplar with mixins)
- **Type Definitions**: `app/states/types.py`, `pmt_core/pmt_core/models/types.py`
- **Custom Exceptions**: `app/exceptions.py`


## Superpowers System

<EXTREMELY_IMPORTANT>
You have superpowers. Superpowers teach you new skills and capabilities.

To load your skills, you must run the bootstrap script at the start of any task:
node .agents/skills/superpowers/bootstrap.js

Follow the instructions it returns.
</EXTREMELY_IMPORTANT>

# Portfolio Management Tool

A professional portfolio management web dashboard built with Reflex.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### System Dependencies

Some Python packages require system-level libraries.

**Linux (Ubuntu/Debian/Pop!_OS):**
```bash
sudo apt-get update
sudo apt-get install -y unixodbc
```

**Windows:**
- Usually pre-installed.
- If connecting to SQL Server, install the [ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).


### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Portfolio-Management-Tool
   ```

2. **Install dependencies (including pmt_core):**
   ```bash
   uv sync
   ```
   > This automatically installs the `pmt_core` shared package in editable mode via uv workspace linking.

3. **Verify installation:**
   ```bash
   python -c "from pmt_core import __version__; print(f'pmt_core version: {__version__}')"
   ```

### Running the App

```bash
uv run reflex run
```

The app will be available at:
- **Frontend:** http://localhost:3001/pmt/
- **Backend:** http://0.0.0.0:8001

---

## Architecture: Dual-Package Separation

This project enforces a strict separation between **business logic** and **UI/UX**:

| Layer | Package | Purpose |
|-------|---------|--------|
| **Business / Backend** | `pmt_core_pkg/pmt_core/` | Models, services, repositories, utilities — **NO Reflex imports** |
| **UI / UX** | `app/` | Reflex pages, states, components — connects to `pmt_core` for business logic |

**Import flow (one-way only):**
```
pmt_core.services → app.services → app.states → app.components
```

- `pmt_core_pkg/` must **never** import from `reflex` or `app/`
- `app/services/` are thin adapters that call `pmt_core` services
- `app/states/` manages Reflex-specific state (loading, errors, search) and delegates data operations to services
- `app/components/` renders UI from state vars — never calls services directly

For detailed architecture guidance, see [AGENTS.md](AGENTS.md).

---

## Project Structure

```
Portfolio-Management-Tool/
├── app/                        # UI / UX Layer (Reflex)
│   ├── components/             # UI components
│   │   ├── shared/             # Shared layout (module_layout.py, etc.)
│   │   └── [module]/           # Module-specific components (e.g., positions/, pnl/)
│   ├── pages/                  # Route pages
│   │   └── [module]/           # Module entry pages
│   ├── services/               # Thin adapters wrapping pmt_core services
│   │   └── [module]/           # e.g., services/positions/, services/compliance/
│   ├── states/                 # Reflex state classes (UI state management)
│   │   └── [module]/           # e.g., states/risk/, states/portfolio/
│   ├── utils/                  # Utilities
│   └── exceptions.py           # Custom exceptions
├── pmt_core_pkg/               # Business / Backend Logic (NO Reflex)
│   └── pmt_core/
│       ├── models/             # TypedDicts, enums, data structures
│       │   └── [module]/       # Module-specific models
│       ├── services/           # Core business logic & calculations
│       │   └── [module]/       # e.g., services/pricing/, services/reports/
│       ├── repositories/       # Data access layer (DB, API, files)
│       │   └── [module]/       # Module-specific repositories
│       └── utilities/          # Logging, helpers
├── tests/                      # Application tests
├── docs/                       # Documentation
└── pyproject.toml              # Project configuration
```

---

## Using `pmt_core` in the Reflex App

The `pmt_core` package provides shared type definitions and utilities that can be imported into the Reflex application.

### Importing Types

```python
# In app/states/ or app/services/
from pmt_core import (
    # TypedDicts for type hints
    PositionRecord,
    PnLRecord,
    MarketDataRecord,
    OrderRecord,
    ComplianceRecord,
    RiskRecord,
)

# Use in function signatures
def process_positions(positions: list[PositionRecord]) -> None:
    for pos in positions:
        print(f"Ticker: {pos['ticker']}, Type: {pos['sec_type']}")
```

### Importing Enums

```python
from pmt_core import (
    InstrumentType,
    DashboardSection,
    OrderStatus,
    ComplianceType,
)

# Use for validation and comparisons
if position["sec_type"] == InstrumentType.STOCK:
    # Handle stock position
    pass

if order["status"] == OrderStatus.FILLED:
    # Process filled order
    pass
```

### Additional Enums

```python
from pmt_core.models.enums import (
    OrderSide,        # buy, sell, short, cover
    MarketStatus,     # open, closed, pre_market, after_hours, halted
    Currency,         # USD, HKD, JPY, CNY, EUR, etc.
    ReconciliationStatus,  # matched, unmatched, partial, pending, failed
)
```

### Using Logging Utilities

```python
from pmt_core.utilities import get_logger, setup_logging

# Get a module-specific logger
logger = get_logger("my_service")
logger.info("Service initialized")

# Or use app-level logging
from app.utils import logger
logger.info("Processing request")
```

### Complete Example: Service with pmt_core Types

```python
# app/services/example_service.py
from pmt_core import PositionRecord, InstrumentType
from pmt_core.utilities import get_logger

logger = get_logger("example_service")

class ExampleService:
    async def get_stock_positions(self) -> list[PositionRecord]:
        """Fetch only stock positions."""
        logger.info("Fetching stock positions")
        
        # Your data fetching logic here
        all_positions: list[PositionRecord] = await self._fetch_positions()
        
        # Filter using enum
        return [
            pos for pos in all_positions 
            if pos["sec_type"] == InstrumentType.STOCK
        ]
    
    async def _fetch_positions(self) -> list[PositionRecord]:
        # Placeholder - implement actual data fetching
        return []
```

---

## Development

### Install Dev Dependencies

```bash
uv sync --group dev
```

### Running Tests

```bash
# Run all tests (single command)
uv run pytest -v

# Run only app tests
uv run pytest tests/ -v

# Run only pmt_core tests
uv run pytest
```

### Project Commands Summary

| Command | Description |
|---------|-------------|
| `uv sync` | Install all dependencies (including pmt_core) |
| `uv sync --group dev` | Install dev dependencies (pytest, etc.) |
| `uv run reflex run` | Start the Reflex application |
| `uv run pytest -v` | Run all tests |

---

## Tech Stack

- **Framework**: [Reflex](https://reflex.dev) (Python → React/Next.js)
- **Styling**: TailwindCSS v3
- **Icons**: Lucide Icons via `rx.icon()`
- **Charts**: Recharts via `rx.recharts`
- **Data**: yfinance for market data

---

## Key Routes

| Route | Description |
|-------|-------------|
| `/pmt/` | Main dashboard with 4-region layout |
| `/pmt/pnl` | P&L Change, Summary, Currency, Full views |
| `/pmt/positions` | Position data, Stock/Warrant/Bond positions |
| `/pmt/market-data` | Market data, FX, Historical, Trading Calendar |
| `/pmt/risk` | Delta Change, Risk Measures, Risk Inputs, Pricers |
| `/pmt/recon` | PPS, Settlement, Failed Trades, PnL Recon |
| `/pmt/compliance` | Restricted List, Undertakings, Beneficial Ownership |
| `/pmt/portfolio-tools` | Pay-To-Hold, Stock Borrow, Resets, Installments |
| `/pmt/instruments` | Ticker Data, Stock Screener, Special Terms |
| `/pmt/events` | Event Calendar, Event Stream, Reverse Inquiry |
| `/pmt/operations` | Daily Procedure Check, Operation Process |
| `/pmt/orders` | EMSX Order, EMSX Route |

---

## Troubleshooting

**Port already in use**:
```bash
uv run reflex run --frontend-port 3001 --backend-port 8001
```

**Frontend not building**:
```bash
rm -rf .web
uv run reflex run
```

**Pydantic V1 compatibility (Python 3.14+)**:
```bash
# Recreate virtual environment with Python 3.13
uv venv --python 3.13 .venv
uv sync
```

---

## Documentation

- **[docs/index.md](docs/index.md)** - **Documentation index** (start here)
- **[AGENTS.md](AGENTS.md)** - Guide for AI agents working with this codebase
- **[pmt_core_pkg/README.md](pmt_core_pkg/README.md)** - Detailed pmt_core package documentation
- **[docs/todos/milestone-1-pre-integration-checklist.md](docs/todos/milestone-1-pre-integration-checklist.md)** - Integration preparation checklist

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key variables:
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- Database credentials (when available)

### Redis on Windows (Memurai/Garnet)

If you set up **Memurai** (see [docs/setups/memurai.md](docs/setups/memurai.md)) or **Garnet** (see [docs/setups/garnet.md](docs/setups/garnet.md)), you must configure the following in your `.env` file:

```bash
# Redis Configuration (Garnet/Memurai)
REFLEX_REDIS_URL=redis://localhost:6379

# State Manager
REFLEX_STATE_MANAGER_MODE=redis
```

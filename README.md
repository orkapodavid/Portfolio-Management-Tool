# Portfolio Management Tool

A professional portfolio management web dashboard built with Reflex.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

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

## Project Structure

```
Portfolio-Management-Tool/
├── app/                        # Reflex web application
│   ├── components/             # UI components
│   │   ├── shared/             # Shared layout like module_layout.py
│   │   └── [module]/           # Module-specific components (e.g., positions/, pnl/)
│   ├── pages/                  # Route pages
│   │   └── [module]/           # Module entry pages
│   ├── services/               # Service layer (grouped by module)
│   │   └── [module]/           # e.g., services/positions/, services/compliance/
│   ├── states/                 # Reflex state classes (grouped by module)
│   │   └── [module]/           # e.g., states/risk/, states/portfolio/
│   ├── utils/                  # Utilities
│   └── exceptions.py           # Custom exceptions
├── pmt_core_pkg/               # Shared business logic package
│   └── pmt_core/
│       ├── models/             # Data models
│       │   └── [module]/       # Module-specific models (proposed)
│       ├── services/           # Business logic
│       │   └── [module]/       # e.g., services/pricing/, services/reports/
│       ├── repositories/       # Data access
│       │   └── [module]/       # Module-specific repositories
│       └── utilities/          # Helpers
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

## Documentation

- **[AGENTS.md](AGENTS.md)** - Guide for AI agents working with this codebase
- **[pmt_core_pkg/README.md](pmt_core_pkg/README.md)** - Detailed pmt_core package documentation
- **[docs/milestone-1-pre-integration-checklist.md](docs/milestone-1-pre-integration-checklist.md)** - Integration as

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

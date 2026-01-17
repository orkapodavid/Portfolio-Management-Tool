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
├── app/                    # Reflex web application
│   ├── components/         # Reusable UI components
│   ├── pages/              # Route pages
│   ├── services/           # Service layer (data access)
│   ├── states/             # Reflex state classes
│   ├── utils/              # Utilities (logging, etc.)
│   └── exceptions.py       # Custom exceptions (re-exports from pmt_core)
├── pmt_core_pkg/           # Shared business logic package
│   └── pmt_core/
│       ├── models/         # TypedDicts and Enums
│       ├── services/       # Business logic (PricingService, ReportService)
│       ├── repositories/   # Data access (pending)
│       ├── utilities/      # Logging helpers
│       └── exceptions.py   # Shared exception hierarchy
├── tests/                  # Application tests
├── docs/                   # Documentation
└── pyproject.toml          # Project configuration
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
uv run pytest pmt_core/tests_core/ -v
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
- **[pmt_core/README.md](pmt_core/README.md)** - Detailed pmt_core package documentation
- **[docs/milestone-1-pre-integration-checklist.md](docs/milestone-1-pre-integration-checklist.md)** - Integration status

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key variables:
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- Database credentials (when available)

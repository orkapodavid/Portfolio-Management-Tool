# pmt_core

Shared business logic for Portfolio Management Tool.

## Overview

`pmt_core` is a standalone Python package containing shared business logic, data models, and utilities used by both:
- The **Reflex web application** (`app/`)
- Future integration with **PyQt desktop application** (`source/`)

This package enables code reuse and maintains consistency between the two UIs.

## Installation

### Development (Editable Install)

```bash
# From repository root
pip install -e ./pmt_core

# Or with uv
uv pip install -e ./pmt_core
```

### Verify Installation

```python
from pmt_core import __version__
print(f"pmt_core version: {__version__}")
```

## Package Structure

```
pmt_core/
├── models/          # Enums, dataclasses, TypedDicts
│   ├── types.py     # Data structure definitions
│   └── enums.py     # Enumeration types
├── services/        # Business logic (pricing, reporting, EMSX)
├── repositories/    # Database/file access wrappers
├── resources/       # Packaged configs/templates
└── utilities/       # Config/logging helpers (UI-free)
```

## Usage

### Type Definitions

```python
from pmt_core.models import PositionRecord, InstrumentType

# Use types for type hints
def process_position(position: PositionRecord) -> None:
    if position["sec_type"] == InstrumentType.STOCK:
        # Handle stock position
        pass
```

### Enums

```python
from pmt_core.models import DashboardSection, OrderStatus

current_section = DashboardSection.POSITIONS
order_status = OrderStatus.WORKING
```

## Current Status

**Version:** 0.1.0 (Scaffold)

This package is currently a scaffold with:
- ✅ Preliminary type definitions based on documentation
- ✅ Placeholder enums for common values
- ⏳ Services pending PyQt source code integration
- ⏳ Repositories pending database access

## Dependencies

- `pandas` - Data manipulation
- `pyodbc` - Database connectivity
- `python-dotenv` - Environment configuration

## Related Documentation

- [Milestone 1 Checklist](../docs/milestone-1-pre-integration-checklist.md)
- [PMT Architecture](../docs/pmt.md)
- [Main AGENTS.md](../AGENTS.md)

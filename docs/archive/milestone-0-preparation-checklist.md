> [!NOTE]
> **Status: ✅ Archived** — 2026-02-19
> Superseded by Milestone 1 and subsequent work. Infrastructure items completed or tracked in `service_layer_migration_2.md`.

# Milestone 0: Infrastructure Preparation (No Source Code Required)

**Description:** Preparation tasks that can be completed before obtaining the PyQt source code. These establish the foundation for rapid integration once the source becomes available.

**Status:** Not Started  
**Created:** 2026-01-14

---

## Overview

This checklist covers all preparatory work that does NOT require the PyQt `source/` directory. Completing these tasks will minimize integration time once the source code is obtained.

---

## 1. Database Infrastructure

### 1.1 Database Connection Setup
- [ ] Verify ODBC Driver 17 for SQL Server is installed
- [ ] Obtain database credentials (server, database name, username, password)
- [ ] Create `.env` file from template with actual credentials
- [ ] Test raw database connection using pyodbc directly

### 1.2 DatabaseService Implementation
- [ ] Implement `app/services/shared/database_service.py`:
  - [ ] `connect()` - Establish connection with retry logic
  - [ ] `disconnect()` - Clean connection closure
  - [ ] `execute_query(sql, params)` - Parameterized query execution
  - [ ] `execute_query_df(sql, params)` - Return pandas DataFrame
  - [ ] `test_connection()` - Health check method
- [ ] Add connection pooling (consider `pyodbc` pooling or custom pool)
- [ ] Implement context manager for automatic connection handling
- [ ] Add query timeout configuration

### 1.3 Database Schema Discovery
- [ ] Query `INFORMATION_SCHEMA.TABLES` to list available tables
- [ ] Document discovered table names
- [ ] Query `INFORMATION_SCHEMA.COLUMNS` for key tables
- [ ] Create preliminary data dictionary

**Verification:**
```python
from app.services.shared.database_service import DatabaseService
db = DatabaseService()
assert db.test_connection() == True
tables = db.execute_query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
print(f"Found {len(tables)} tables")
```

---

## 2. Environment Configuration

### 2.1 Environment Variables
- [ ] Create `.env.example` template:
  ```env
  # Database Configuration
  DB_SERVER=your_server
  DB_DATABASE=your_database
  DB_USERNAME=your_username
  DB_PASSWORD=your_password
  DB_DRIVER=ODBC Driver 17 for SQL Server
  
  # Optional: Bloomberg Configuration
  BBG_HOST=localhost
  BBG_PORT=8194
  
  # Logging
  LOG_LEVEL=INFO
  LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
  ```
- [ ] Update `.gitignore` to exclude `.env`
- [ ] Create `app/config.py` for centralized config loading
- [ ] Document all environment variables in README or separate doc

### 2.2 Configuration Loader
- [ ] Create `app/utils/config_loader.py`:
  - [ ] Load from `.env` using `python-dotenv`
  - [ ] Provide typed access to config values
  - [ ] Support default values
  - [ ] Validate required variables on startup

---

## 3. Shared Package Scaffold (`pmt_core/`)

### 3.1 Package Structure
- [ ] Create directory structure:
  ```
  pmt_core/
  ├── pyproject.toml
  └── pmt_core/
      ├── __init__.py
      ├── models/
      │   └── __init__.py
      ├── services/
      │   └── __init__.py
      ├── repositories/
      │   └── __init__.py
      ├── resources/
      │   └── __init__.py
      └── utilities/
          └── __init__.py
  ```

### 3.2 Package Configuration
- [ ] Create `pmt_core/pyproject.toml`:
  ```toml
  [project]
  name = "pmt-core"
  version = "0.1.0"
  description = "Shared business logic for Portfolio Management Tool"
  requires-python = ">=3.11"
  dependencies = [
      "pandas",
      "pyodbc",
      "python-dotenv",
  ]
  
  [build-system]
  requires = ["setuptools>=61.0"]
  build-backend = "setuptools.build_meta"
  ```
- [ ] Add to main `pyproject.toml` dependencies:
  ```toml
  dependencies = [
      ...
      "pmt-core @ file:./pmt_core",
  ]
  ```
- [ ] Test editable install: `pip install -e ./pmt_core`
- [ ] Verify import: `from pmt_core import __version__`

---

## 4. Type Definitions (Based on Documentation)

### 4.1 Core TypedDicts
Based on `pmt.md` documentation, create preliminary type definitions in `app/states/types.py` or `pmt_core/models/types.py`:

- [ ] **PositionRecord** - Fields from position_full report
  ```python
  class PositionRecord(TypedDict):
      id: int
      position_date: str
      underlying: str
      ticker: str
      instrument_type: str  # Stock, Warrant, Bond
      quantity: float
      market_value: float
      currency: str
      # ... extend based on actual schema
  ```

- [ ] **PnLRecord** - Fields from pnl_tab reports
  ```python
  class PnLRecord(TypedDict):
      id: int
      trade_date: str
      underlying: str
      ticker: str
      pnl_ytd: float
      pnl_1d: float
      pnl_1w: float
      pnl_1m: float
      # ... extend based on actual schema
  ```

- [ ] **MarketDataRecord** - Real-time market data fields
- [ ] **OrderRecord** - EMSX order fields
- [ ] **ComplianceRecord** - Restricted list, undertaking fields
- [ ] **RiskRecord** - Delta, Greeks, risk measure fields

### 4.2 Enum Definitions
- [ ] Create placeholder enums based on documentation:
  ```python
  class InstrumentType(str, Enum):
      STOCK = "stock"
      WARRANT = "warrant"
      BOND = "bond"
      CONVERTIBLE = "convertible"
  
  class DashboardSection(str, Enum):
      POSITIONS = "positions"
      PNL = "pnl"
      COMPLIANCE = "compliance"
      TRADING = "trading"
      MARKET_DATA = "market_data"
      RISK = "risk"
      OPERATIONS = "operations"
      EVENTS = "events"
  ```

---

## 5. Service Layer Preparation

### 5.1 Adapter Interface Definition
- [ ] Create `app/adapters/__init__.py`
- [ ] Define base adapter protocol:
  ```python
  from typing import Protocol
  
  class DataAdapter(Protocol):
      async def fetch_data(self, **params) -> list[dict]:
          """Fetch data from source."""
          ...
      
      async def refresh_data(self) -> None:
          """Trigger data refresh."""
          ...
  ```

### 5.2 Service Factory Pattern
- [ ] Create `app/services/service_factory.py`:
  - [ ] Factory to instantiate services with proper dependencies
  - [ ] Support mock vs real implementation switching
  - [ ] Dependency injection for DatabaseService

### 5.3 Async Wrapper Utilities
- [ ] Create `app/utils/async_helpers.py`:
  ```python
  import asyncio
  from typing import Callable, TypeVar
  
  T = TypeVar('T')
  
  async def run_sync(func: Callable[..., T], *args, **kwargs) -> T:
      """Run synchronous function in thread pool."""
      return await asyncio.to_thread(func, *args, **kwargs)
  ```

---

## 6. Testing Infrastructure

### 6.1 Test Configuration
- [ ] Create `pytest.ini` or `pyproject.toml` pytest section:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests", "pmt_core/tests"]
  python_files = ["test_*.py"]
  python_functions = ["test_*"]
  asyncio_mode = "auto"
  ```
- [ ] Install test dependencies: `pytest`, `pytest-asyncio`, `pytest-mock`

### 6.2 Test Directory Structure
- [ ] Create test directories:
  ```
  tests/
  ├── __init__.py
  ├── conftest.py           # Shared fixtures
  ├── test_database.py      # Database connection tests
  ├── test_config.py        # Config loading tests
  └── services/
      ├── __init__.py
      └── test_services.py  # Service mock tests
  
  pmt_core/tests/
  ├── __init__.py
  ├── conftest.py
  └── test_utilities.py
  ```

### 6.3 Test Fixtures
- [ ] Create `tests/conftest.py`:
  ```python
  import pytest
  from unittest.mock import MagicMock
  
  @pytest.fixture
  def mock_db_connection():
      """Mock database connection for testing."""
      conn = MagicMock()
      conn.cursor.return_value.fetchall.return_value = []
      return conn
  
  @pytest.fixture
  def sample_position_data():
      """Sample position records for testing."""
      return [
          {"id": 1, "ticker": "AAPL", "quantity": 100},
          {"id": 2, "ticker": "MSFT", "quantity": 200},
      ]
  ```

### 6.4 Database Integration Tests (Skippable)
- [ ] Create `tests/test_database_integration.py`:
  ```python
  import pytest
  from app.services.shared.database_service import DatabaseService
  
  @pytest.mark.skipif(
      not os.getenv("DB_SERVER"),
      reason="Database credentials not configured"
  )
  class TestDatabaseIntegration:
      def test_connection(self):
          db = DatabaseService()
          assert db.test_connection()
  ```

---

## 7. Logging Setup

### 7.1 Logger Configuration
- [ ] Create `app/utils/logging_config.py`:
  ```python
  import logging
  import os
  
  def setup_logging():
      level = os.getenv("LOG_LEVEL", "INFO")
      format_str = os.getenv(
          "LOG_FORMAT",
          "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      )
      logging.basicConfig(level=level, format=format_str)
      
      # Silence noisy loggers
      logging.getLogger("httpx").setLevel(logging.WARNING)
      logging.getLogger("httpcore").setLevel(logging.WARNING)
  ```
- [ ] Call `setup_logging()` in app initialization

### 7.2 Custom Exceptions
- [ ] Create `app/exceptions.py`:
  ```python
  class PMTError(Exception):
      """Base exception for Portfolio Management Tool."""
      pass
  
  class DatabaseConnectionError(PMTError):
      """Failed to connect to database."""
      pass
  
  class ConfigurationError(PMTError):
      """Invalid or missing configuration."""
      pass
  
  class DataExtractionError(PMTError):
      """Failed to extract data from source."""
      pass
  
  class ServiceUnavailableError(PMTError):
      """Required service is not available."""
      pass
  ```

---

## 8. Documentation

### 8.1 Update Existing Docs
- [ ] Update `AGENTS.md`:
  - [ ] Add database setup instructions
  - [ ] Add testing commands
  - [ ] Document environment variables
- [ ] Update `README.md`:
  - [ ] Add prerequisites section
  - [ ] Add setup instructions
  - [ ] Add development workflow

### 8.2 Create Integration Guide
- [ ] Create `docs/integration-guide.md`:
  - [ ] Step-by-step integration process
  - [ ] Service migration order
  - [ ] Testing strategy
  - [ ] Rollback procedures

---

## 9. CI/CD Preparation (Optional)

### 9.1 GitHub Actions Workflow
- [ ] Create `.github/workflows/test.yml`:
  ```yaml
  name: Tests
  on: [push, pull_request]
  jobs:
    test:
      runs-on: windows-latest
      steps:
        - uses: actions/checkout@v4
        - uses: astral-sh/setup-uv@v4
        - run: uv sync
        - run: uv run pytest tests/ -v --ignore=tests/test_database_integration.py
  ```

### 9.2 Pre-commit Hooks
- [ ] Create `.pre-commit-config.yaml` for code quality checks

---

## 10. Verify Reflex App Stability

### 10.1 Current App Health Check
- [ ] Run `uv run reflex run` and verify startup
- [ ] Navigate through all dashboard sections
- [ ] Confirm mock data displays correctly
- [ ] Check browser console for JavaScript errors
- [ ] Verify no Python exceptions in terminal

### 10.2 State Management Audit
- [ ] Review each state class for `on_load` implementation
- [ ] Verify service injection patterns
- [ ] Check for potential race conditions in async handlers
- [ ] Document any existing issues to fix

---

## Completion Checklist

Before marking this milestone complete, verify:

- [ ] Database connection works: `db.test_connection() == True`
- [ ] `pmt_core` package installs: `pip install -e ./pmt_core`
- [ ] Environment config loads: `from app.config import settings`
- [ ] Tests pass: `uv run pytest tests/ -v`
- [ ] Reflex app starts: `uv run reflex run`
- [ ] All type definitions documented
- [ ] Logging configured and working
- [ ] Documentation updated

---

## What This Enables

Once complete, when PyQt source code is obtained:

1. **Immediate model migration** - Copy enums/types directly
2. **Quick service integration** - Adapter interfaces ready
3. **Database queries work** - Connection already tested
4. **Testing ready** - Fixtures and structure in place
5. **Minimal friction** - All infrastructure prepared

---

## Notes

- Focus on database connectivity first - it's the most critical dependency
- Type definitions can be refined once actual data structures are seen
- Keep mock implementations working throughout preparation
- Document any assumptions made about data structures

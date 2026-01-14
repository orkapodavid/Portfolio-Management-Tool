# Milestone 1: Pre-Integration Preparation

**Description:** Prepare the codebase infrastructure and resolve dependencies before integrating the PyQt business logic into the Reflex web application via the `pmt_core` shared package.

**Status:** Not Started  
**Created:** 2026-01-14

---

## Overview

This milestone establishes the foundation for system integration. Tasks are categorized by availability of external dependencies.

---

## Blocked Dependencies

The following resources are **NOT currently available** and block certain tasks:

| Resource | Status | Blocks |
|----------|--------|--------|
| PyQt Source Code (`source/`) | **Unavailable** | Sections 5, 6, 7 |
| Database Access (MS SQL Server) | **Unavailable** | Section 3 |
| Configuration Files (`resources/config/`) | **Unavailable** | Section 4 |
| Bloomberg Terminal | **Unavailable** | EMSX integration |

---

## Pre-Integration Checklist

### 1. External Resources Acquisition (BLOCKED)

- [ ] **1.1** Obtain the PyQt application source code (`source/` directory)
- [ ] **1.2** Obtain the configuration files (`resources/config/` directory)
- [ ] **1.3** Obtain MS SQL Server database credentials
- [ ] **1.4** Verify ODBC Driver 17 for SQL Server is installed
- [ ] **1.5** Verify source directory structure matches `pmt.md` documentation
- [ ] **1.6** Document any differences between expected and actual structure

**Status:** BLOCKED - Waiting on external access  
**Action Required:** Contact repository owner / IT for access

---

### 2. Shared Package Structure (`pmt_core/`) - CAN PROCEED

- [ ] **2.1** Create `pmt_core/` directory at repository root
- [ ] **2.2** Create `pmt_core/pyproject.toml` for standalone installation:
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
- [ ] **2.3** Create package subdirectories:
  ```
  pmt_core/
  ├── pyproject.toml
  └── pmt_core/
      ├── __init__.py
      ├── models/          # Enums, dataclasses, TypedDicts
      │   └── __init__.py
      ├── services/        # Business logic (pricing, reporting, EMSX)
      │   └── __init__.py
      ├── repositories/    # Database/file access wrappers
      │   └── __init__.py
      ├── resources/       # Packaged configs/templates (placeholder)
      │   └── __init__.py
      └── utilities/       # Config/logging helpers (UI-free)
          └── __init__.py
  ```
- [ ] **2.4** Configure editable installation: `pip install -e ./pmt_core`
- [ ] **2.5** Add `pmt_core` dependency to main `pyproject.toml`
- [ ] **2.6** Verify package imports work in Reflex app

**Status:** CAN PROCEED  
**Verification:** `pip install -e ./pmt_core && python -c "from pmt_core import __version__"`

---

### 3. Database Connectivity (BLOCKED)

- [ ] **3.1** Verify MS SQL Server access credentials
- [ ] **3.2** Create `.env.example` template with required variables:
  ```
  DB_SERVER=
  DB_DATABASE=
  DB_USERNAME=
  DB_PASSWORD=
  DB_DRIVER=ODBC Driver 17 for SQL Server
  ```
- [ ] **3.3** Implement `DatabaseService.connect()` method in `app/services/shared/database_service.py`
- [ ] **3.4** Implement `DatabaseService.execute_query()` with parameterized queries
- [ ] **3.5** Add connection pooling configuration
- [ ] **3.6** Test database connection with simple SELECT query
- [ ] **3.7** Document required database tables (cross-reference with `pmt.md`)

**Status:** BLOCKED - No database access  
**Dependency:** MS SQL Server credentials

---

### 4. Configuration Migration (BLOCKED)

- [ ] **4.1** Analyze `resources/config/env.ini` structure
- [ ] **4.2** Map `.ini` configuration to environment variables or YAML
- [ ] **4.3** Create `pmt_core/utilities/config_loader.py` using `importlib.resources`
- [ ] **4.4** Migrate report configurations:
  - [ ] `position_tab/*.report.ini`
  - [ ] `pnl_tab/*.report.ini`
  - [ ] `compliance_tab/*.report.ini`
  - [ ] `trading_tab/*.report.ini`
  - [ ] `market_data_tab/*.report.ini`
  - [ ] `risk_tab/*.report.ini` (if exists)
- [ ] **4.5** Create config validation utilities
- [ ] **4.6** Test config loading from packaged resources

**Status:** BLOCKED - No configuration files  
**Dependency:** `resources/config/` directory

---

### 5. Model & Type Definitions (PARTIALLY BLOCKED)

#### Can Do Now (based on documentation):
- [ ] **5.1** Create preliminary TypedDict definitions based on `pmt.md`:
  - [ ] `PositionRecord` (basic fields from documentation)
  - [ ] `PnLRecord` (basic fields from documentation)
  - [ ] `MarketDataRecord`
  - [ ] `OrderRecord`
  - [ ] `ComplianceRecord`
  - [ ] `RiskRecord`
- [ ] **5.2** Create placeholder enums based on documentation:
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
      # ...
  ```
- [ ] **5.3** Align with existing `app/states/types.py` definitions

#### Blocked (requires source code):
- [ ] **5.4** Extract exact enums from `source/models/enum_*.py`
- [ ] **5.5** Validate TypedDict fields against actual data structures
- [ ] **5.6** Create Pydantic models for API validation

**Status:** PARTIALLY BLOCKED  
**Can proceed with:** Preliminary types based on `pmt.md` documentation

---

### 6. Service Layer Adapters (BLOCKED)

- [ ] **6.1** Create adapter pattern for each service domain:

  | Reflex Service | PyQt Source | Adapter Location |
  |----------------|-------------|------------------|
  | `PnLService` | `source/reports/pnl_tab/` | `app/adapters/pnl_adapter.py` |
  | `PositionService` | `source/reports/position_tab/` | `app/adapters/position_adapter.py` |
  | `RiskService` | `source/reports/analytics_tab/` | `app/adapters/risk_adapter.py` |
  | `ComplianceService` | `source/reports/compliance_tab/` | `app/adapters/compliance_adapter.py` |
  | `EMSXService` | `source/reports/trading_tab/` | `app/adapters/emsx_adapter.py` |
  | `MarketDataService` | `source/reports/market_data_tab/` | `app/adapters/market_data_adapter.py` |

- [ ] **6.2** Define adapter interface contracts (ABC or Protocol)
- [ ] **6.3** Create mock adapter implementations for testing
- [ ] **6.4** Document `asyncio.to_thread` usage for blocking calls

**Status:** BLOCKED - No source code  
**Dependency:** PyQt `source/` directory

---

### 7. ReportClass Integration Pattern (BLOCKED)

- [ ] **7.1** Analyze `source/models/class_mapping.py` for ReportType mappings
- [ ] **7.2** Document `ReportClass` interface methods:
  - `extract_report_data()` - Data fetch
  - `merge_report_data()` - Join operations
  - `process_report_data()` - Side effects
- [ ] **7.3** Create wrapper for calling `extract_report_data()` from async context
- [ ] **7.4** Map `[Query]` section SQL to parameterized queries
- [ ] **7.5** Document merge dependencies between report types

**Status:** BLOCKED - No source code  
**Dependency:** PyQt `source/` directory

---

### 8. Testing Infrastructure - CAN PROCEED

- [ ] **8.1** Set up pytest configuration:
  ```toml
  # Add to pyproject.toml
  [tool.pytest.ini_options]
  testpaths = ["tests", "pmt_core/tests"]
  python_files = ["test_*.py"]
  asyncio_mode = "auto"
  ```
- [ ] **8.2** Create test directory structure:
  ```
  tests/
  ├── __init__.py
  ├── conftest.py           # Shared fixtures
  └── services/
      └── __init__.py
  
  pmt_core/tests/
  ├── __init__.py
  └── conftest.py
  ```
- [ ] **8.3** Create mock fixtures in `tests/conftest.py`:
  ```python
  @pytest.fixture
  def mock_db_connection():
      """Mock database connection for testing."""
      ...
  
  @pytest.fixture
  def sample_position_data():
      """Sample position records for testing."""
      ...
  ```
- [ ] **8.4** Add placeholder unit tests for future components
- [ ] **8.5** Install test dependencies: `pytest`, `pytest-asyncio`, `pytest-mock`

**Status:** CAN PROCEED  
**Verification:** `uv run pytest tests/ -v`

---

### 9. Logging & Error Handling - CAN PROCEED

- [ ] **9.1** Create `app/exceptions.py`:
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
- [ ] **9.2** Create `app/utils/logging_config.py`:
  ```python
  import logging
  import os
  
  def setup_logging():
      level = os.getenv("LOG_LEVEL", "INFO")
      logging.basicConfig(
          level=level,
          format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      )
  ```
- [ ] **9.3** Configure generic logger for `pmt_core` (`logging.getLogger("pmt_core")`)
- [ ] **9.4** Add structured logging format compatible with both UIs

**Status:** CAN PROCEED

---

### 10. Documentation Updates - CAN PROCEED

- [ ] **10.1** Update `AGENTS.md` with:
  - [ ] Current blockers and dependencies
  - [ ] Available preparation tasks
  - [ ] Testing commands
- [ ] **10.2** Create `pmt_core/README.md` with:
  - Package overview
  - Installation instructions
  - Placeholder usage examples
- [ ] **10.3** Document service migration roadmap (high-level)
- [ ] **10.4** Add inline TODO comments referencing this checklist

**Status:** CAN PROCEED

---

### 11. Reflex App Stability Verification - CAN PROCEED

- [ ] **11.1** Run `uv run reflex run` and verify startup
- [ ] **11.2** Navigate through all dashboard sections
- [ ] **11.3** Confirm mock data displays correctly
- [ ] **11.4** Check browser console for JavaScript errors
- [ ] **11.5** Verify no Python exceptions in terminal
- [ ] **11.6** Review each state class for `on_load` implementation
- [ ] **11.7** Document any existing issues to fix

**Status:** CAN PROCEED  
**Verification:** Manual testing of all views

---

## Summary: What Can Be Done Now

| Section | Status | Action |
|---------|--------|--------|
| 1. External Resources | BLOCKED | Wait for access |
| 2. pmt_core Structure | **CAN PROCEED** | Create scaffold |
| 3. Database Connectivity | BLOCKED | Wait for credentials |
| 4. Configuration Migration | BLOCKED | Wait for config files |
| 5. Type Definitions | **PARTIAL** | Create preliminary types |
| 6. Service Adapters | BLOCKED | Wait for source code |
| 7. ReportClass Integration | BLOCKED | Wait for source code |
| 8. Testing Infrastructure | **CAN PROCEED** | Set up pytest |
| 9. Logging & Errors | **CAN PROCEED** | Create utilities |
| 10. Documentation | **CAN PROCEED** | Update docs |
| 11. App Verification | **CAN PROCEED** | Test current app |

---

## Immediate Action Items

Tasks that can start immediately without any blocked dependencies:

1. **Create `pmt_core/` package scaffold** (Section 2)
2. **Set up pytest configuration** (Section 8)
3. **Create custom exceptions** (Section 9.1)
4. **Create logging configuration** (Section 9.2)
5. **Create preliminary TypedDicts** (Section 5.1-5.3)
6. **Verify Reflex app stability** (Section 11)
7. **Update documentation** (Section 10)

---

## Success Criteria (With Current Constraints)

Before proceeding to integration phase, verify:

1. [ ] `pmt_core` package scaffold created and installs: `pip install -e ./pmt_core`
2. [ ] pytest configuration works: `uv run pytest tests/ -v`
3. [ ] Custom exceptions defined in `app/exceptions.py`
4. [ ] Logging configuration created
5. [ ] Preliminary TypedDicts documented
6. [ ] Reflex app starts without errors: `uv run reflex run`
7. [ ] All blocked dependencies documented and tracked

---

## Next Steps After Dependencies Are Resolved

When external resources become available:

| When Available | Then Complete |
|----------------|---------------|
| PyQt Source Code | Sections 5.4-5.6, 6, 7 |
| Database Access | Section 3 |
| Config Files | Section 4 |
| All Resources | Full integration testing |

---

## Notes

- Focus on scaffold and infrastructure that doesn't require external dependencies
- Keep mock implementations working throughout preparation
- Document all assumptions made about data structures
- Track dependency resolution separately

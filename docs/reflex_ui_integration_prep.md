# Reflex UI Integration Preparation Guide

This guide provides step-by-step prompts for preparing the Reflex web application to integrate with the PMT (Portfolio Management Tool) PyQt application's business logic. These steps can be executed **independently** without requiring deep knowledge of the PyQt codebase.

## Prerequisites

Before starting, ensure:
- You have access to this Reflex app repository
- You understand this repo will eventually be copied into the PMT PyQt repository as a subfolder
- The PMT PyQt repo contains business logic in `source/` and configs in `resources/` that will be shared via a `pmt_core` package

---

## Phase 1: Understanding the Current Reflex App Structure

### Prompt 1 – Audit the Existing Reflex Application

```text
I need to understand the current Reflex application structure before integrating it with external business logic.

1) **Goal**
Map out the existing Reflex app architecture, identify where business logic currently lives, and understand the current data flow.

2) **Actions**
- Examine the project structure:
  - `app/` directory: main application entry point and routing
  - `app/components/`: reusable UI components (identify which ones fetch or display data)
  - `app/pages/`: page-level views (portfolio, goals, research, reports, etc.)
  - `app/states/`: state management modules (identify which states manage financial data)
  - `app/services/`: existing services (e.g., `finance_service.py`)
- For each state file in `app/states/`, document:
  - What data it manages (e.g., portfolio holdings, stock prices, goals)
  - Where it currently fetches data from (hardcoded, external APIs, services)
  - What external dependencies it uses (yfinance, PyGithub, etc.)
- For each service in `app/services/`, document:
  - What business logic it encapsulates
  - What external APIs or libraries it depends on

3) **Output**
Provide a structured summary:
- Directory tree showing key files
- List of states with their responsibilities and current data sources
- List of services with their current implementations
- Identification of "integration points" where PMT business logic will eventually replace current implementations
```

---

### Prompt 2 – Identify Data Models and DTOs

```text
Before integrating with external business logic, I need to understand what data structures the Reflex UI currently expects.

1) **Goal**
Document all data models, types, and structures currently used by the Reflex UI components and states.

2) **Actions**
- Search through `app/states/` for any dataclasses, Pydantic models, or TypedDicts
- Examine `app/components/` to identify what data shapes components expect (e.g., table columns, chart data formats)
- Document the structure of data passed between:
  - Services → States
  - States → Components/Pages
- Look for any type hints or explicit data contracts

3) **Output**
Create a data model inventory:
- List all defined models/types with their fields
- Document implicit data structures (dictionaries with known keys)
- Identify any data transformation logic between layers
- Note which models are tied to external APIs (yfinance, etc.) vs internal business logic
```

---

## Phase 2: Preparing for `pmt_core` Integration

### Prompt 3 – Design the Adapter Layer Structure

```text
The Reflex app will eventually call into a shared `pmt_core` package for business logic. I need to design an adapter layer to bridge between `pmt_core` DTOs and Reflex UI data structures.

1) **Goal**
Create a clean adapter architecture that isolates the Reflex app from direct knowledge of PMT internals while enabling easy integration.

2) **Context**
- The `pmt_core` package will provide services like:
  - `pmt_core.services.reporting` (portfolio reports, positions, P&L)
  - `pmt_core.services.pricing` (instrument pricing)
  - `pmt_core.models` (enums, configuration models)
- The `pmt_core` package uses `.ini` configuration files
- All `pmt_core` services are synchronous Python functions
- Reflex states are async and need to call sync `pmt_core` services via `asyncio.to_thread`

3) **Actions**
- Propose an `app/adapters/` directory structure with modules like:
  - `pmt_adapter.py` (base adapter interface)
  - `portfolio_adapter.py` (adapts PMT portfolio/positions data to Reflex format)
  - `pricing_adapter.py` (adapts PMT pricing data)
  - `reporting_adapter.py` (adapts PMT reports)
- For each adapter, design:
  - Input: `pmt_core` DTO types (describe expected structure based on finance domain)
  - Output: Reflex-friendly dictionaries or dataclasses
  - Error handling strategy (what happens if `pmt_core` is unavailable?)
  - Caching strategy (if needed for performance)

4) **Output**
Provide:
- Proposed adapter directory structure
- Skeleton code for 2-3 key adapters with docstrings
- Interface contracts (type hints) showing how states will call adapters
- Notes on how to handle the sync→async boundary using `asyncio.to_thread`
```

---

### Prompt 4 – Create Mock `pmt_core` Interfaces for Development

```text
While the real `pmt_core` package is being built, I need mock interfaces so I can develop and test the Reflex UI independently.

1) **Goal**
Create a mock `pmt_core` package within the Reflex repo that mimics the expected API of the real `pmt_core`, allowing parallel development.

2) **Actions**
- Create a `app/mocks/pmt_core/` directory structure:
  ```
  app/mocks/pmt_core/
  ├── __init__.py
  ├── services/
  │   ├── __init__.py
  │   ├── reporting.py      # Mock reporting functions
  │   ├── pricing.py        # Mock pricing functions
  │   └── rules.py          # Mock rules/alerts
  ├── models/
  │   ├── __init__.py
  │   └── enums.py          # Mock enums (ReportType, etc.)
  └── utilities/
      ├── __init__.py
      └── config.py         # Mock config loading
  ```
- For each mock service module, implement:
  - Function signatures matching expected `pmt_core` API
  - Return realistic sample data (portfolios, positions, prices)
  - Add delays (`time.sleep`) to simulate real data fetching
  - Document the expected real signature in docstrings

3) **Output**
- Full mock package structure
- Implementation of at least 3 mock service functions:
  - `reporting.get_portfolio_positions(date: str) -> PositionsData`
  - `pricing.get_current_prices(tickers: List[str]) -> PriceData`
  - `reporting.get_pnl_summary(start_date: str, end_date: str) -> PnLData`
- Instructions for how to switch from mock to real `pmt_core` later (via environment variable or config flag)
```

---

### Prompt 5 – Update States to Use Adapters (Mock Mode)

```text
Now that I have adapters and mocks, I need to refactor existing Reflex states to use the adapter layer instead of direct API calls.

1) **Goal**
Refactor at least one state (e.g., `portfolio_state.py`) to use the mock `pmt_core` via adapters, establishing the integration pattern.

2) **Actions**
- Choose one state file (e.g., `app/states/portfolio/portfolio_state.py`)
- Identify where it currently fetches data (e.g., `yfinance` calls in event handlers)
- Replace direct data fetching with:
  ```python
  from app.adapters.portfolio_adapter import PortfolioAdapter
  from app.mocks.pmt_core.services import reporting
  
  async def load_portfolio_data(self):
      # Call mock pmt_core via adapter
      raw_data = await asyncio.to_thread(reporting.get_portfolio_positions, "2024-01-01")
      adapted_data = PortfolioAdapter.adapt_positions(raw_data)
      self.portfolio_data = adapted_data
  ```
- Add error handling and loading states
- Ensure UI components still work with adapted data

3) **Constraints**
- Do NOT remove existing code yet; keep it commented as reference
- Ensure the refactored state works with existing UI components
- Use `asyncio.to_thread` for all mock service calls (they're sync functions)

4) **Output**
- Refactored state file with adapter integration
- Before/after comparison showing the changes
- Notes on any data structure mismatches discovered
- Test plan for validating the refactored state works
```

---

## Phase 3: Configuration and Environment Setup

### Prompt 6 – Add Configuration for `pmt_core` Integration

```text
The Reflex app needs configuration to manage the integration with `pmt_core`, including toggling between mock and real implementations.

1) **Goal**
Add configuration management that supports development (mock mode) and production (real `pmt_core`) scenarios.

2) **Actions**
- Create or update `app/constants.py` or a new `app/config.py` with:
  ```python
  import os
  from enum import Enum
  
  class IntegrationMode(Enum):
      MOCK = "mock"          # Use mock pmt_core
      REAL = "real"          # Use real pmt_core package
      STANDALONE = "standalone"  # Use only yfinance/direct APIs (current mode)
  
  PMT_INTEGRATION_MODE = os.getenv("PMT_INTEGRATION_MODE", "mock")
  PMT_CORE_PATH = os.getenv("PMT_CORE_PATH", None)  # Path to real pmt_core when available
  ```
- Update adapter modules to check `PMT_INTEGRATION_MODE` and import accordingly:
  ```python
  if PMT_INTEGRATION_MODE == "mock":
      from app.mocks.pmt_core.services import reporting
  elif PMT_INTEGRATION_MODE == "real":
      from pmt_core.services import reporting
  else:
      # Use existing standalone implementation
  ```
- Document how to set environment variables for different modes

3) **Output**
- Configuration module with integration mode support
- Updated adapters with conditional imports
- README section explaining:
  - How to run in mock mode (default for development)
  - How to run in standalone mode (current behavior)
  - How to run in real mode (once `pmt_core` is available)
```

---

### Prompt 7 – Prepare Dependency Management for Integration

```text
The Reflex app will eventually depend on the real `pmt_core` package. I need to prepare the dependency configuration.

1) **Goal**
Update `requirements.txt` and `pyproject.toml` (if exists) to support optional `pmt_core` dependency.

2) **Actions**
- Add commented-out entry to `requirements.txt`:
  ```
  # PMT Core integration (uncomment when pmt_core is available)
  # -e ../pmt_core  # Editable install from parent directory
  ```
- If using `pyproject.toml`, add optional dependency group:
  ```toml
  [project.optional-dependencies]
  pmt-integration = [
      "pmt_core @ file:///${PMT_CORE_PATH}",
  ]
  ```
- Document the installation process for both scenarios:
  - Development (current): `pip install -r requirements.txt` (works standalone)
  - Integration (future): `pip install -e . && pip install -e ../pmt_core`
- Ensure all mock dependencies are in the main requirements

3) **Output**
- Updated dependency files with integration notes
- Installation instructions for both modes
- List of any dependency conflicts to watch for (e.g., if `pmt_core` needs different pandas version)
```

---

## Phase 4: Testing and Validation

### Prompt 8 – Create Integration Tests with Mocks

```text
Before the real `pmt_core` is available, I need tests that validate the adapter layer and state integration work correctly with mocks.

1) **Goal**
Create a test suite that validates the Reflex app's integration readiness using mock `pmt_core`.

2) **Actions**
- Create `tests/integration/` directory (if not exists)
- Add test files:
  - `test_portfolio_adapter.py`: Test adapter transformations
  - `test_pmt_state_integration.py`: Test state integration with mocks
  - `test_mock_pmt_core.py`: Validate mock APIs match expected signatures
- For each test:
  - Use `pytest` (or existing test framework)
  - Test both success and error scenarios
  - Validate data structure transformations
  - Test async boundary (mock service → `asyncio.to_thread` → state)
- Add fixture for mock `pmt_core` responses

3) **Output**
- Test files with at least 10 test cases covering:
  - Adapter transformations
  - State event handlers calling adapters
  - Error handling when mock returns errors
  - Data type validation
- Instructions for running tests: `pytest tests/integration/`
- Documentation of test coverage and what still needs manual testing
```

---

### Prompt 9 – Create UI Components for PMT-Specific Features

```text
The PMT system has specific features (e.g., compliance alerts, position reconciliation) that may not exist in the current Reflex UI. I need to prepare components for these.

1) **Goal**
Identify and create placeholder UI components for PMT-specific features that will be populated with real data later.

2) **Actions**
Based on the PMT features described in `docs/PMT Architecture Map.md`, create placeholder components for:
- **Compliance Panel**: Display restricted list, undertakings, beneficial ownership alerts
- **Reconciliation Widget**: Show position discrepancies between sources
- **Rules & Alerts Panel**: Display rule-based alerts with severity levels
- **EMSX Order Status**: If trading features are needed (optional)

For each component:
- Create in `app/components/pmt/` directory
- Use mock data for initial rendering
- Design props interface to accept data from adapters
- Include loading/error states
- Style consistently with existing Reflex components

3) **Output**
- 3-4 new component files in `app/components/pmt/`
- Each component should:
  - Accept data via props (typed if possible)
  - Render mock/sample data by default
  - Include docstrings explaining what real data will look like
- Example usage in a test page to validate rendering
```

---

### Prompt 10 – Document the Integration Handoff

```text
Create documentation that explains the current Reflex app state and what's needed to complete the `pmt_core` integration.

1) **Goal**
Produce clear documentation for future developers (or yourself) to complete the integration once `pmt_core` is available.

2) **Actions**
Create a `docs/reflex_integration_status.md` file with sections:

**Section 1: What's Been Done**
- List of refactored states using adapters
- List of created adapters and their purposes
- Mock `pmt_core` package structure and capabilities
- New PMT-specific UI components
- Configuration setup for mode switching

**Section 2: Integration Checklist (To Complete)**
- [ ] Install real `pmt_core` package
- [ ] Update `PMT_INTEGRATION_MODE` to "real"
- [ ] Validate adapter transformations with real data
- [ ] Remove or archive mock `pmt_core` package
- [ ] Update remaining states not yet using adapters
- [ ] Test all UI components with real data
- [ ] Add error handling for `pmt_core` failures
- [ ] Performance testing with real database queries

**Section 3: Known Gaps & Assumptions**
- Document any assumptions made about `pmt_core` API
- List any data structure mismatches anticipated
- Note any PMT features not yet supported in UI

**Section 4: Testing Strategy**
- How to test with mock vs real data
- What manual testing is needed
- What automated tests exist

3) **Output**
- Complete documentation file
- Diagrams (mermaid or text-based) showing:
  - Current data flow: UI → Adapters → Mock
  - Future data flow: UI → Adapters → `pmt_core`
- Contact points or resources for getting help
```

---

## Quick Start Workflow

If you want to execute these prompts efficiently, follow this order:

1. **Week 1 - Understanding**: Run Prompts 1-2 to map current state
2. **Week 2 - Architecture**: Run Prompts 3-4 to design and create mocks
3. **Week 3 - Implementation**: Run Prompts 5-7 to refactor and configure
4. **Week 4 - Validation**: Run Prompts 8-10 to test and document

By the end, your Reflex app will be **integration-ready**: it will work standalone with mocks, have a clear adapter layer, and be prepared to swap in the real `pmt_core` with minimal changes.

---

## Environment Variables Reference

```bash
# Development mode (default)
export PMT_INTEGRATION_MODE=mock

# Standalone mode (current yfinance-based implementation)
export PMT_INTEGRATION_MODE=standalone

# Real integration mode (once pmt_core is available)
export PMT_INTEGRATION_MODE=real
export PMT_CORE_PATH=/path/to/pmt_core
```

---

## Success Criteria

You'll know the Reflex app is ready for integration when:

✅ All states use adapters instead of direct API calls  
✅ Mock `pmt_core` provides realistic test data  
✅ UI components render correctly with adapted data  
✅ Configuration supports easy mode switching  
✅ Integration tests pass with mocks  
✅ Documentation clearly explains next steps  
✅ The app runs without errors in both standalone and mock modes  

Once `pmt_core` is available, integration should be as simple as:
1. Install `pmt_core` package
2. Set `PMT_INTEGRATION_MODE=real`
3. Run integration tests with real data
4. Fix any adapter mismatches discovered

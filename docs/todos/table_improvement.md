# AG Grid Reflex Wrapper Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a generic, reusable AG Grid Enterprise wrapper as a local Reflex package, then migrate existing tables in phases.

**Architecture:** Local package (`reflex_ag_grid/`) with Python Reflex component wrapping AG Grid Enterprise. Uses standard Reflex state management (no dedicated WebSocket). Config-driven column definitions enable easy customization per table.

**Tech Stack:** Reflex Python, AG Grid Enterprise 31.x, React 18, TypeScript/JavaScript

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Licensing | **Enterprise** | Full feature set for context menu, range selection, grouping, Excel export |
| Real-time Updates | **Reflex State** | Simpler architecture, sufficient for current needs |
| Migration | **Phased Rollout** | Start with 1-2 critical tables, validate, then migrate others |
| Package Structure | **Local Package** | Copyable between repos as `reflex_ag_grid/` folder |

---

## Requirements Traceability Matrix

| # | Requirement | AG-Grid Feature | Implementation Approach |
|---|-------------|-----------------|------------------------|
| 1 | Right-click context menu | `getContextMenuItems()` | Enterprise: Built-in customizable menu |
| 2 | Bulk state changes (Range) | `enableRangeSelection` | Enterprise: Range selection + batch updates |
| 3 | Blinking cell changes | `api.flashCells()` | Community: CSS animation on value change |
| 4 | Notification jump & highlight | `ensureNodeVisible()` | Community: Scroll + flash API |
| 5 | Grouping & Summary | `rowGroup` + `aggFunc` | Enterprise: Row grouping with aggregation |
| 6 | Notification publisher | Reflex State | Python: State-based notification list |
| 7 | Data Validation (.ini) | `valueParser` | Python: ConfigParser → JS validators |
| 8 | Copy cell / with header | Clipboard API | Enterprise: Context menu copy actions |
| 9 | Export Excel | `exportDataAsExcel()` | Enterprise: Native Excel export |
| 10 | WebSocket publishing | Reflex WebSocket | Reflex: Native state updates |
| 11 | Different Cell Editors | `cellEditor` mapping | Community: Type-based editor selection |
| 12 | Disable auto-refresh on edit | Edit tracking | JS: Track editing cells, skip updates |
| 13 | Cell-by-cell update | Transaction API | Community: `applyTransaction()` for delta |
| 14 | Update timing | Reflex background | Python: Background task scheduling |
| 15 | Save table format | `localStorage` | Community: Column state persistence |

---

## Project Structure

```
reflex_ag_grid/
├── __init__.py                    # Package exports
├── components/
│   ├── __init__.py
│   ├── ag_grid.py                 # Main Reflex custom component
│   ├── ag_grid_state.py           # Base state mixin class
│   └── notification_panel.py      # Optional notification UI
├── services/
│   ├── __init__.py
│   ├── validation_loader.py       # .ini config parser
│   └── column_config.py           # Column definition helpers
├── static/
│   └── ag_grid_wrapper.js         # React wrapper for AG Grid
├── config/
│   └── validation.example.ini     # Example validation config
└── README.md                      # Usage documentation
```

---

## Phase 1: Core Wrapper Implementation

### Objective
Build the foundational AG Grid wrapper component that can render a basic grid with Enterprise features.

### Checklist

- [x] **1.1** Set up `reflex_ag_grid/` package structure
- [x] **1.2** Create JavaScript React wrapper (`ag_grid_wrapper.js`)
  - [x] AG Grid Enterprise initialization
  - [x] Column definition processing
  - [x] Cell editor mapping by type
  - [x] Context menu with copy/export actions
  - [x] Column state localStorage persistence
  - [x] **Function Registry Pattern** - String keys for formatters/renderers
  - [x] **Event Sanitization** - Safe event data, no circular refs
  - [x] **License Key Injection** - Via prop or window.AG_GRID_LICENSE_KEY
- [x] **1.3** Create Reflex custom component (`ag_grid.py`)
  - [x] `NoSSRComponent` subclass
  - [x] Props: `column_defs`, `row_data`, `theme`, `height`, `width`
  - [x] Events: `on_cell_edit`, `on_selection_change`, `on_grid_ready`
- [x] **1.4** Create base state mixin (`ag_grid_state.py`)
  - [x] `AGGridStateMixin` with common handlers
  - [x] `jump_to_row()`, `export_excel()`, `export_csv()` via `rx.call_script`
- [x] **1.5** Add AG Grid Enterprise dependencies via `lib_dependencies` (Reflex-native, no package.json)
- [x] **1.6** Write serialization unit tests (17 tests, all passing)
- [x] **1.7** Create basic usage example
- [x] **1.8** Create full demo app (`reflex_ag_grid/examples/demo_app/`)
  - [x] `rxconfig.py` for standalone execution
  - [x] Multi-page app showcasing all features:
    - [x] Basic Grid page - simple data display
    - [x] Editable Grid page - cell editing with validation
    - [x] Grouped Grid page - row grouping with aggregation
    - [x] Streaming Data page - mock real-time updates
  - [x] Mock streaming data with toggle (manual refresh mode - rx.background N/A in 0.8.26)
  - [x] Notifications panel (simplified)
  - [x] Export buttons (Excel, CSV)
  - [x] README with run instructions
- [ ] **1.9** Create Playwright E2E tests (`reflex_ag_grid/tests/`)
  - [ ] `tests/setup_browsers.py` - Browser installation check/setup script
  - [ ] `tests/e2e_ag_grid.py` - Main E2E test script using `uv run`
  - [ ] Test cases:
    - [ ] Grid renders with correct row count
    - [ ] Cell editing updates value
    - [ ] Right-click shows context menu
    - [ ] Copy cell to clipboard works
    - [ ] Export triggers file download
    - [ ] Column resize persists after refresh
    - [ ] Notifications display and jump-to-row works
  - [ ] Uses semantic locators (per Playwright skill best practices)
  - [ ] Screenshots on failure for debugging

### Architectural Constraints Applied (Per Senior Review)

1. ✅ **Function Registry Pattern** - Formatters/renderers use string keys mapped to JS functions
2. ✅ **Event Sanitization** - All AG Grid events sanitized before sending to Python
3. ✅ **Pydantic Validation** - Using `ColumnDef` and `ValidationSchema` Pydantic models
4. ✅ **License Key Injection** - Supports `license_key` prop or `window.AG_GRID_LICENSE_KEY`

### Testing Plan - Phase 1

| Test Type | Test Case | Expected Result | Verification Method |
|-----------|-----------|-----------------|---------------------|
| Unit | `ColumnDef.to_ag_grid_def()` | Correct dict output | `pytest reflex_ag_grid/tests/test_models.py -v` |
| Unit | `ValidationSchema.validate_row()` | Valid/invalid detection | `pytest reflex_ag_grid/tests/test_models.py -v` |
| Integration | Demo app starts | No errors on `reflex run` | Manual: `cd reflex_ag_grid/examples/demo_app && reflex run` |
| E2E | Grid renders with data | Rows visible in browser | `uv run reflex_ag_grid/tests/e2e_ag_grid.py` |
| E2E | Cell edit saves value | New value persists | `uv run reflex_ag_grid/tests/e2e_ag_grid.py` |
| E2E | Context menu appears | Menu visible on right-click | `uv run reflex_ag_grid/tests/e2e_ag_grid.py` |
| E2E | Export downloads file | .xlsx/.csv file created | `uv run reflex_ag_grid/tests/e2e_ag_grid.py` |

**Verification Commands:**
```bash
# 1. Setup Playwright browsers (one-time)
uv run reflex_ag_grid/tests/setup_browsers.py

# 2. Run Python unit tests
pytest reflex_ag_grid/tests/test_models.py -v

# 3. Start demo app (in separate terminal)
cd reflex_ag_grid/examples/demo_app
reflex run

# 4. Run E2E tests (requires demo app running)
uv run reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000

# 5. Manual verification
# Navigate to http://localhost:3000, test each page
```

---

## Phase 2: Validation & Cell Editing

### Objective
Add validation configuration loading and type-based cell editing with validation feedback.

### Checklist

- [ ] **2.1** Create validation loader (`validation_loader.py`)
  - [ ] Parse `.ini` config file
  - [ ] `FieldValidation` dataclass
  - [ ] Type, min, max, pattern, enum support
- [ ] **2.2** Integrate validation into JS wrapper
  - [ ] `valueParser` with validation rules
  - [ ] Visual feedback for invalid cells (red border)
  - [ ] Reject invalid values, keep old value
- [ ] **2.3** Cell editor configuration
  - [ ] Map types to AG Grid editors (text, number, select, checkbox, date)
  - [ ] `enumValues` → dropdown options
  - [ ] Number precision and range
- [ ] **2.4** Edit event handling
  - [ ] `on_cell_edit` fires with rowId, field, oldValue, newValue
  - [ ] Python handler receives edit data
- [ ] **2.5** Create example validation config
- [ ] **2.6** Write validation loader unit tests
- [ ] **2.7** Document validation config format

### Testing Plan - Phase 2

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Unit | Load valid .ini config | FieldValidation objects created |
| Unit | Load invalid .ini | Graceful error handling |
| Unit | Validate int in range | Returns (True, None) |
| Unit | Validate int out of range | Returns (False, error_msg) |
| Unit | Validate enum value | Accepts valid, rejects invalid |
| Integration | Edit numeric cell | Number editor appears |
| Integration | Edit enum cell | Dropdown with options |
| E2E | Enter invalid value | Cell shows error, reverts |
| E2E | Enter valid value | Cell updates, event fires |

**Verification Commands:**
```bash
# Run validation tests
pytest tests/unit/reflex_ag_grid/test_validation_loader.py -v

# Manual test: Edit cells with different types
```

---

## Phase 3: Advanced Features

### Objective
Implement grouping, aggregation, notifications, and export functionality.

### Checklist

- [ ] **3.1** Row grouping support
  - [ ] `rowGroup: true` in column def
  - [ ] Group expansion/collapse
  - [ ] `aggFunc` for summary values (sum, avg, count, min, max)
- [ ] **3.2** Range selection and bulk updates
  - [ ] `enableRangeSelection: true`
  - [ ] Bulk state change handler
  - [ ] Flash affected cells
- [ ] **3.3** Cell flashing on value change
  - [ ] CSS animation class
  - [ ] `api.flashCells()` integration
- [ ] **3.4** Notification panel component
  - [ ] `notification_panel.py` UI component
  - [ ] Click notification → jump to row
  - [ ] Notification types: info, warning, error, success
- [ ] **3.5** Export functionality
  - [ ] Excel export via `exportDataAsExcel()`
  - [ ] CSV export via `exportDataAsCsv()`
  - [ ] Toolbar buttons for export
- [ ] **3.6** Jump to row functionality
  - [ ] `ensureNodeVisible()` + flash
  - [ ] Triggered from notifications or external
- [ ] **3.7** Write integration tests
- [ ] **3.8** Update documentation

### Testing Plan - Phase 3

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Integration | Group by column | Rows grouped with headers |
| Integration | Collapse group | Child rows hidden |
| Integration | Aggregation sum | Group shows sum of values |
| E2E | Select range | Multiple cells highlighted |
| E2E | Export to Excel | .xlsx file downloads |
| E2E | Export to CSV | .csv file downloads |
| E2E | Notification click | Grid scrolls to row, flashes |
| E2E | Cell value change | Cell flashes briefly |

**Verification Commands:**
```bash
# Run all tests
pytest tests/ -v

# Manual tests:
# 1. Group by a column, verify aggregation
# 2. Click export buttons, verify downloads
# 3. Add notification, click to jump
```

---

## Phase 4: Pilot Migration - Holdings Table

### Objective
Migrate `holdings_table.py` as the first real table to validate the wrapper.

### Checklist

- [ ] **4.1** Analyze current `holdings_table.py`
  - [ ] Document current columns and data types
  - [ ] Document current styling/behavior
- [ ] **4.2** Create column definition config
  - [ ] Define columns: symbol, shares, price, value, gain_loss, change
  - [ ] Set types, formatters, styles
- [ ] **4.3** Create `holdings_ag_grid.py` using wrapper
  - [ ] Use `AGGrid` component with config
  - [ ] Wire up to `PortfolioState`
- [ ] **4.4** Add validation config for holdings
  - [ ] Price validation (min 0)
  - [ ] Shares validation (min 1)
- [ ] **4.5** Style matching
  - [ ] Match or improve current visual design
  - [ ] Dark/light theme support
- [ ] **4.6** Side-by-side comparison
  - [ ] Create toggle between old/new table
  - [ ] Verify feature parity
- [ ] **4.7** Remove old implementation (after validation)
- [ ] **4.8** Document migration learnings

### Testing Plan - Phase 4

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Visual | Compare old vs new | Visually equivalent or better |
| Functional | View holdings | All data displays correctly |
| Functional | Sort by column | Sorting works |
| Functional | Filter by column | Filtering works |
| E2E | Edit share count | Value updates, state syncs |
| E2E | Right-click copy | Cell value copied |
| Performance | Load 100 holdings | Renders in <1s |

**Verification Commands:**
```bash
# Run app
reflex run

# Navigate to portfolio page
# Compare old table vs new AG Grid table
# Test all interactive features
```

---

## Phase 5: Batch Migration

### Objective
Migrate remaining tables systematically using patterns from Phase 4.

### Migration Order (by complexity)

| Priority | Component | File | Complexity |
|----------|-----------|------|------------|
| 1 | Risk Views | `risk/risk_views.py` (5 tables) | Medium |
| 2 | Positions | `positions/positions_views.py` (5 tables) | Medium |
| 3 | PnL Views | `pnl/pnl_views.py` (4 tables) | Medium |
| 4 | Reconciliation | `reconciliation/reconciliation_views.py` (5 tables) | Medium |
| 5 | Portfolio Tools | `portfolio_tools/portfolio_tools_views.py` (9 tables) | High |
| 6 | Market Data | `market_data/market_data_views.py` (5 tables) | Medium |
| 7 | Instruments | `instruments/instrument_views.py` (5 tables) | Medium |
| 8 | Events | `events/events_views.py` (3 tables) | Low |
| 9 | Operations | `operations/operations_views.py` (2 tables) | Low |
| 10 | EMSX | `emsx/emsx_views.py` (2 tables) | Low |
| 11 | Compliance | `compliance/` (2 tables) | Low |
| 12 | Others | Remaining tables | Low |

### Checklist per Component

For each component migration:
- [ ] Create column config for all tables
- [ ] Create validation config if needed
- [ ] Create new AG Grid-based component
- [ ] Test feature parity
- [ ] Remove old implementation
- [ ] Update imports

### Testing Plan - Phase 5

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Regression | All pages load | No errors |
| Regression | All tables render | Data displays |
| Regression | All interactions work | Sorting, filtering, editing |
| Performance | Full app benchmark | No performance regression |

**Verification Commands:**
```bash
# Run full test suite
pytest tests/ -v

# Smoke test all pages
# Manual navigation through app
```

---

## Phase 6: Documentation & Polish

### Objective
Finalize documentation, create migration guide, ensure package is ready for reuse.

### Checklist

- [ ] **6.1** Complete `reflex_ag_grid/README.md`
  - [ ] Installation instructions
  - [ ] Quick start guide
  - [ ] API reference
  - [ ] Configuration examples
- [ ] **6.2** Create migration guide
  - [ ] Step-by-step migration from `rx.el.table`
  - [ ] Common patterns and solutions
  - [ ] Troubleshooting guide
- [ ] **6.3** Add inline code documentation
  - [ ] Docstrings for all public functions
  - [ ] Type hints throughout
- [ ] **6.4** Create example gallery
  - [ ] Basic grid
  - [ ] Grouped grid
  - [ ] Editable grid with validation
  - [ ] Full-featured trading grid
- [ ] **6.5** Performance optimization review
  - [ ] Review large table performance
  - [ ] Document best practices
- [ ] **6.6** Final cleanup
  - [ ] Remove deprecated code
  - [ ] Consistent code style
  - [ ] Update all imports

### Testing Plan - Phase 6

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Documentation | Follow README quickstart | Grid works as documented |
| Documentation | All examples run | No errors |
| Code Quality | Linting passes | No lint errors |
| Code Quality | Type checking | No type errors |

**Verification Commands:**
```bash
# Lint check
ruff check reflex_ag_grid/

# Type check
mypy reflex_ag_grid/

# Build docs (if applicable)
# Run all examples
```

---

## Appendix A: Original Requirements Analysis

### Status
**Current Stage**: Implementation Planning Complete

### Objective
Build a generic AG Grid wrapper to satisfy all 15 requirements from original analysis.

### Requirements Analysis Matrix

| # | Requirement | Ag-Grid Community (FOSS) | Ag-Grid Enterprise (Paid) | Custom `rx.table` / `rx.data_editor` | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Right click context menu | **No** (Standard browser menu) | **Yes** (Customizable) | **Possible** | Can be built with `rx.context_menu` wrapping the table. |
| 2 | State changes on multiple (Range) | **No** | **Yes** (Range Selection) | **Hard** | `rx.data_editor` might support some, but custom `rx.table` requires complex JS logic for drag-select. |
| 3 | Blinking cell changes | **Yes** (`enableCellChangeFlash`) | **Yes** | **Medium** | Doable with CSS transitions and state updates. |
| 4 | Notification jump & highlight | **Yes** (API `ensureIndexVisible`) | **Yes** | **Medium** | Requires calculating pagination/scroll position manually. |
| 5 | Grouping & Summary | **No** | **Yes** (Row Grouping/Pivot) | **Hard** | Requires backend processing to structure data as tree, handling expansion state manually. |
| 6 | Notification publisher | **N/A** (Backend logic) | **N/A** | **N/A** | Both solutions display data similarly. |
| 7 | Data Validation (.ini) | **Yes** (Value Setters) | **Yes** | **Yes** | Can be handled in Python event handlers. |
| 8 | Copy cell / Copy with header | **Yes** (Basic OS copy) | **Yes** (Advanced Clipboard) | **Medium** | Browser native copy works for text; advanced (headers) needs custom JS. |
| 9 | Export Excel | **No** (CSV only) | **Yes** (.xlsx native) | **Medium** | Can implement `pandas.to_excel` on backend + `rx.download`. |
| 10 | WebSocket publishing | **Yes** (Reflex Native) | **Yes** | **Yes** | Core Reflex feature. |
| 11 | Different Cell Editors | **Yes** | **Yes** | **Yes** | `rx.data_editor` has types; Custom table needs dynamic component rendering. |
| 12 | Disable auto-refresh on edit | **Yes** | **Yes** | **Yes** | Manage via State flags. |
| 13 | Cell-by-cell update (Efficiency) | **Yes** (Transaction API) | **Yes** | **Medium** | `rx.table` redraws rows; Ag-Grid handles DOM Diffing very well. |
| 14 | Update timing | **N/A** (Backend logic) | **N/A** | **N/A** | Backend task. |
| 15 | Save table format (Local Storage) | **Yes** (`getColumnState`) | **Yes** | **Hard** | Ag-Grid has built-in state methods. Custom requires manually tracking/saving column widths/order. |

### Selected Option
**Option A: AG Grid Enterprise** - All requirements are out-of-the-box (OOTB), highly performant.

---

## Appendix B: Dependencies

### Python (requirements.txt)
```
reflex>=0.4.0
configparser>=5.0
```

### JavaScript (package.json additions)
```json
{
  "dependencies": {
    "ag-grid-react": "^31.3.0",
    "ag-grid-enterprise": "^31.3.0",
    "ag-grid-community": "^31.3.0"
  }
}
```

---

## Appendix C: Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Core Wrapper | 3-4 days | None |
| Phase 2: Validation & Editing | 2-3 days | Phase 1 |
| Phase 3: Advanced Features | 2-3 days | Phase 2 |
| Phase 4: Pilot Migration | 1-2 days | Phase 3 |
| Phase 5: Batch Migration | 5-7 days | Phase 4 |
| Phase 6: Documentation | 1-2 days | Phase 5 |

**Total Estimate: 14-21 days**

---

## Implementation Checklist Summary

### Phase 1: Core Wrapper
- [ ] 1.1 Package structure setup
- [ ] 1.2 JavaScript React wrapper
- [ ] 1.3 Reflex custom component
- [ ] 1.4 Base state mixin
- [ ] 1.5 Package dependencies
- [ ] 1.6 Unit tests
- [ ] 1.7 Basic example

### Phase 2: Validation & Editing
- [ ] 2.1 Validation loader
- [ ] 2.2 JS validation integration
- [ ] 2.3 Cell editor config
- [ ] 2.4 Edit event handling
- [ ] 2.5 Example config
- [ ] 2.6 Validation tests
- [ ] 2.7 Documentation

### Phase 3: Advanced Features
- [ ] 3.1 Row grouping
- [ ] 3.2 Range selection
- [ ] 3.3 Cell flashing
- [ ] 3.4 Notification panel
- [ ] 3.5 Export functionality
- [ ] 3.6 Jump to row
- [ ] 3.7 Integration tests
- [ ] 3.8 Documentation

### Phase 4: Pilot Migration
- [ ] 4.1 Analyze holdings_table
- [ ] 4.2 Column config
- [ ] 4.3 New AG Grid component
- [ ] 4.4 Validation config
- [ ] 4.5 Style matching
- [ ] 4.6 Side-by-side comparison
- [ ] 4.7 Remove old implementation
- [ ] 4.8 Document learnings

### Phase 5: Batch Migration
- [ ] 5.1 Risk Views (5 tables)
- [ ] 5.2 Positions (5 tables)
- [ ] 5.3 PnL Views (4 tables)
- [ ] 5.4 Reconciliation (5 tables)
- [ ] 5.5 Portfolio Tools (9 tables)
- [ ] 5.6 Market Data (5 tables)
- [ ] 5.7 Instruments (5 tables)
- [ ] 5.8 Events (3 tables)
- [ ] 5.9 Operations (2 tables)
- [ ] 5.10 EMSX (2 tables)
- [ ] 5.11 Compliance (2 tables)
- [ ] 5.12 Remaining tables

### Phase 6: Documentation
- [ ] 6.1 README.md
- [ ] 6.2 Migration guide
- [ ] 6.3 Code documentation
- [ ] 6.4 Example gallery
- [ ] 6.5 Performance review
- [ ] 6.6 Final cleanup
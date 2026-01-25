# AG Grid Reflex Wrapper Implementation Plan

> **For AI Assistants:** Follow Phase checklists task-by-task. Read "Lessons Learned" section before making AG Grid changes.

**Goal:** Build a generic, reusable AG Grid Enterprise wrapper as a local Reflex package, then migrate existing tables in phases.

**Architecture:** Local package (`reflex_ag_grid/`) with Python Reflex component wrapping AG Grid Enterprise. Uses standard Reflex state management (no dedicated WebSocket). Config-driven column definitions enable easy customization per table.

**Tech Stack:** Reflex Python, AG Grid Enterprise 32.3.0, React 18, TypeScript/JavaScript

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Licensing | **Enterprise** | Full feature set for context menu, range selection, grouping, Excel export |
| Real-time Updates | **Reflex State** | Simpler architecture, sufficient for current needs |
| Migration | **Phased Rollout** | Start with 1-2 critical tables, validate, then migrate others |
| Package Structure | **Local Package** | Copyable between repos as `reflex_ag_grid/` folder |

---

## ⚠️ Lessons Learned (AG Grid 32.x Migration)

> **CRITICAL:** Read this section before making changes to the AG Grid wrapper.

### 1. ResizeObserver Error (AG Grid 32.1.0)

**Problem:** AG Grid 32.1.0 crashes with `TypeError: parameter 1 is not of type 'Element'` during React hydration.

**Root Cause:** AG Grid's `ResizeObserverService` tries to observe DOM elements before they exist.

**Solution:** Upgrade to **AG Grid 32.2.0+** which fixes the hydration timing issue.

### 2. Do NOT Use Custom JS Wrapper with NoSSRComponent

**Problem:** Using `rx.NoSSRComponent` with a custom `library` path (e.g., `/assets/ag_grid_wrapper.js`) causes Reflex to generate duplicate identifier errors.

**What Happens:**
```javascript
// Reflex generates BOTH of these with same name:
import SafeAgGridReact from "/assets/ag_grid_wrapper.js";      // Static import
const SafeAgGridReact = ClientSide(() => import(...));         // Dynamic import
// → "Identifier 'SafeAgGridReact' has already been declared"
```

**Solution:** Use `rx.Component` (not `NoSSRComponent`) with standard npm library:
```python
class AgGrid(rx.Component):
    library: str = "ag-grid-react@32.3.0"  # Standard npm package
    tag: str = "AgGridReact"
```

### 3. Theme Prop API Change (AG Grid 32.x)

**Problem:** AG Grid 32.x changed the `theme` prop API. Passing `theme="quartz"` crashes with `TypeError: newGridTheme?.startUse is not a function`.

**Solution:** Remove `theme` from props, use CSS class instead:
```python
# In create() method:
theme_name = props.pop("theme", "quartz")  # Remove from props!
props["class_name"] = rx.match(
    theme_name,
    ("quartz", rx.color_mode_cond("ag-theme-quartz", "ag-theme-quartz-dark")),
    ...
)
```

### 4. Always Clean Build After Version Changes

**Command:** Always delete `.web` folder when changing AG Grid versions:
```bash
Remove-Item -Recurse -Force .web; reflex run
```

### 5. Deprecation Warnings (AG Grid 32.2+)

The following props are deprecated but still work:
- `suppressRowClickSelection` → use `rowSelection.enableClickSelection`
- `groupSelectsChildren` → use `rowSelection.groupSelects = "descendants"`
- `rowSelection="multiple"` → use object-based config

These are cosmetic warnings, not breaking changes.

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
│   ├── ag_grid.py                 # Main Reflex custom component (rx.Component)
│   ├── ag_grid_state.py           # Base state mixin class
│   └── notification_panel.py      # Optional notification UI
├── services/
│   ├── __init__.py
│   ├── validation_loader.py       # .ini config parser
│   └── column_config.py           # Column definition helpers
├── config/
│   └── validation.example.ini     # Example validation config
├── examples/
│   └── demo_app/                  # Standalone demo application
└── README.md                      # Usage documentation
```

> **Note:** Static JS wrapper removed - using standard `ag-grid-react` npm package via `lib_dependencies`.

---

## Phase 1: Core Wrapper Implementation

### Objective
Build the foundational AG Grid wrapper component that can render a basic grid with Enterprise features.

### Checklist

- [x] **1.1** Set up `reflex_ag_grid/` package structure
- [x] **1.2** ~~Create JavaScript React wrapper (`ag_grid_wrapper.js`)~~ (REMOVED - using npm imports)
  - [x] AG Grid Enterprise initialization
  - [x] Column definition processing
  - [x] Cell editor mapping by type
  - [x] Context menu with copy/export actions
  - [x] Column state localStorage persistence
  - [x] **Function Registry Pattern** - String keys for formatters/renderers
  - [x] **Event Sanitization** - Safe event data, no circular refs
  - [x] **License Key Injection** - Via prop or window.AG_GRID_LICENSE_KEY
- [x] **1.3** Create Reflex custom component (`ag_grid.py`)
  - [x] `rx.Component` subclass (AG Grid 32.3.0 fixed hydration issue)
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
- [x] **1.9** Create Playwright E2E tests (`reflex_ag_grid/tests/`) ✅
  - [x] `tests/setup_browsers.py` - Browser installation check/setup script
  - [x] `tests/e2e_ag_grid.py` - Main E2E test script using `uv run`
  - [x] Test cases (6/6 passed):
    - [x] Grid renders with correct row count (8 rows)
    - [x] Grid has expected columns
    - [x] Row selection works
    - [x] Theme is applied
    - [x] Right-click shows context menu
    - [x] No fatal console errors
  - [x] Screenshots on failure for debugging
- [x] **1.10** Demo App - Requirements Coverage (all 15 requirements) ✅
  > Ensure `demo_app` demonstrates every requirement from the Traceability Matrix
  
  | Req# | Requirement | Demo Page | Status |
  |------|-------------|-----------|--------|
  | 1 | Right-click context menu | Basic Grid | ✅ Done |
  | 2 | Bulk range selection | Range Selection page | ✅ Done |
  | 3 | Blinking cell changes | Streaming Data | ✅ Done (enableCellChangeFlash) |
  | 4 | Notification jump & highlight | Notifications panel | ✅ Done (ensureNodeVisible) |
  | 5 | Grouping & Summary | Grouped Grid | ✅ Done |
  | 6 | Notification publisher | Notifications panel | ✅ Done |
  | 7 | Data Validation | Editable Grid | ✅ Done (error feedback) |
  | 8 | Copy cell / with header | Basic Grid context menu | ✅ Done |
  | 9 | Export Excel | Export buttons | ✅ Done |
  | 10 | WebSocket publishing | Streaming Data | ✅ Done |
  | 11 | Different Cell Editors | Editable Grid | ✅ Done (select, checkbox) |
  | 12 | Disable auto-refresh on edit | Editable Grid | ✅ Done (pause toggle) |
  | 13 | Cell-by-cell update | Streaming Data | ✅ Done |
  | 14 | Update timing | Streaming Data | ✅ Done (toggle) |
  | 15 | Save table format | Column State page | ✅ Done (localStorage) |
  
  **Tasks: (10/10 complete)**
  - [x] 1.10.1 Add `enableCellChangeFlash` prop for cell flash (Req 3)
  - [x] 1.10.2 Add `ensureNodeVisible()` jump-to-row in Notifications (Req 4)
  - [x] 1.10.3 Add validation error feedback in Editable Grid (Req 7)
  - [x] 1.10.4 Add Range Selection demo page (Req 2)
  - [x] 1.10.5 Add different cell editors (select, checkbox) (Req 11)
  - [x] 1.10.6 Add "pause updates while editing" toggle (Req 12)
  - [x] 1.10.7 Streaming Data page with manual/auto updates (Req 13)
  - [x] 1.10.8 Add Column State persistence demo (Req 15)
  - [x] 1.10.9 Update E2E tests (9/9 passed)
  - [x] 1.10.10 Update demo README with all features
- [ ] **1.11** Standalone Package Setup (uv workspace member)
  > Make `reflex_ag_grid/` a standalone package importable by `app/components/shared` and other packages
  
  **Why:** Currently `reflex_ag_grid` requires sys.path hacks. As a proper uv workspace member, it can be:
  - Imported cleanly: `from reflex_ag_grid import ag_grid, ColumnDef`
  - Published to PyPI if needed
  - Reused across multiple projects
  
  **Tasks:**
  - [x] 1.11.1 Create `reflex_ag_grid/pyproject.toml` with package metadata
    ```toml
    [project]
    name = "reflex-ag-grid"
    version = "0.1.0"
    dependencies = ["reflex>=0.8.26", "pydantic>=2.0"]
    
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    ```
  - [x] 1.11.2 Add to root workspace in main `pyproject.toml`
    ```toml
    [tool.uv.sources]
    reflex-ag-grid = { workspace = true }
    
    [tool.uv.workspace]
    members = ["reflex_ag_grid"]
    ```
  - [x] 1.11.3 Remove sys.path hacks from `demo_app/ag_grid_demo.py`
  - [x] 1.11.4 Run `uv sync` to install as editable workspace member
  - [x] 1.11.5 Verify import works: `from reflex_ag_grid import ag_grid`
  - [N/A] 1.11.6 Update `app/components/shared` to use the package (not currently using it)
  - [x] 1.11.7 Update demo_app to use package import
  - [x] 1.11.8 Run E2E tests to verify no regressions (12/12 passed ✅)
- [ ] **1.12** Global Search / Quick Filter Component
  > Add a `quick_filter_text` prop to the AG Grid component for reactive text filtering
  
  **Why:** Users need a quick way to filter grid data across all columns. Using a reactive prop:
  - Follows Reflex patterns (state-driven)
  - Gives users full control over the input component (styling, debouncing, placement)
  - Integrates with AG Grid's built-in `quickFilterText` option
  
  **Tasks:**
  - [x] 1.12.1 Add `quick_filter_text: rx.Var[str]` prop to `ag_grid.py` component
  - [x] 1.12.2 Add demo page `/search` to demo app showing the feature
  - [x] 1.12.3 Add E2E test for search functionality
  - [x] 1.12.4 Update README with usage examples
  
  **Usage Example:**
  ```python
  class State(rx.State):
      search_text: str = ""

  def search_grid():
      return rx.vstack(
          rx.input(
              placeholder="Search all columns...",
              value=State.search_text,
              on_change=State.set_search_text,
          ),
          ag_grid(
              id="my_grid",
              row_data=State.data,
              column_defs=columns,
              quick_filter_text=State.search_text,  # Reactive filter
          ),
      )
  ```

### Architectural Constraints Applied (Per Senior Review)

1. ✅ **Function Registry Pattern** - Formatters/renderers use string keys mapped to JS functions
2. ✅ **Event Sanitization** - All AG Grid events sanitized before sending to Python
3. ✅ **Pydantic Validation** - Using `ColumnDef` and `ValidationSchema` Pydantic models
4. ✅ **License Key Injection** - Supports `license_key` prop or `window.AG_GRID_LICENSE_KEY`

### Testing Plan - Phase 1

| Test Type | Test Case | Expected Result | Verification Method |
|-----------|-----------|-----------------|---------------------|
| Unit | `ColumnDef.to_ag_grid_def()` | Correct dict output | `pytest reflex_ag_grid/tests/test_serialization.py -v` |
| Unit | `ValidationSchema.validate_row()` | Valid/invalid detection | `pytest reflex_ag_grid/tests/test_serialization.py -v` |
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

> **Note:** Cell editors (2.3) and edit events (2.4) were implemented in Phase 1. Remaining work is validation system.

### Checklist

- [x] **2.1** Create validation loader (`validation_loader.py`) ✅
  - [x] Parse `.ini` or Python config file (`models/validation.py`)
  - [x] `FieldValidation` Pydantic model
  - [x] Type, min, max, pattern, enum support
- [x] **2.2** Integrate validation into JS wrapper ✅
  - [x] Added `validation_schema` prop to `ag_grid.py`
  - [x] `to_js_config()` generates JS-compatible validation rules
  - [x] Visual feedback via ColumnDef `cellClassRules`
- [x] **2.3** Cell editor configuration ✅ (Done in Phase 1)
  - [x] Map types to AG Grid editors (text, number, select, checkbox, date)
  - [x] `enumValues` → dropdown options
  - [x] `AGEditors` constants in `ag_grid.py`
- [x] **2.4** Edit event handling ✅ (Done in Phase 1)
  - [x] `on_cell_value_changed` with row_index, field, new_value
  - [x] `on_cell_editing_started/stopped` events
  - [x] Python handler receives edit data
- [x] **2.5** Create example validation config ✅
  - [x] Added `EDITABLE_VALIDATION` schema to demo app
  - [x] Demonstrates price, qty, change, symbol, sector validation
- [x] **2.6** Write validation loader unit tests ✅ (20 tests passing)
  - [x] Test `FieldValidation` model
  - [x] Test `ValidationSchema.validate_row()` method
  - [x] Test `to_js_config()` output
- [x] **2.7** Document validation config format ✅
  - [x] Updated README with validation section
  - [x] Includes usage examples and type table
- [x] **2.8** E2E tests for validation ✅
  - [x] Navigate to `/validation` page
  - [x] Test validation rules table visible
  - [x] Test code example visible
  - [x] Test cell editing with valid value
  - [/] Test sector dropdown (minor: dropdown locator issue)

### Testing Plan - Phase 2

**Unit Tests (20 tests in `test_validation.py`):**
| Test Case | Status |
|-----------|--------|
| Validate required empty | ✅ |
| Validate required None | ✅ |
| Validate optional empty | ✅ |
| Validate number in range | ✅ |
| Validate number below min | ✅ |
| Validate number above max | ✅ |
| Validate integer from string | ✅ |
| Validate integer invalid string | ✅ |
| Validate pattern match | ✅ |
| Validate pattern no match | ✅ |
| Validate enum valid | ✅ |
| Validate enum invalid | ✅ |
| Validate string min length | ✅ |
| Validate string max length | ✅ |
| FieldValidation.to_js_validation() | ✅ |
| ValidationSchema.get_field() found | ✅ |
| ValidationSchema.get_field() not found | ✅ |
| ValidationSchema.validate_row() all valid | ✅ |
| ValidationSchema.validate_row() with errors | ✅ |
| ValidationSchema.to_js_config() | ✅ |

**E2E Tests (task 2.8 - TODO):**
| Test Case | Expected Result |
|-----------|-----------------|
| Edit price with valid value (100) | Cell updates, no error |
| Edit price with invalid value (-10) | Error shown, value rejected |
| Edit sector dropdown | Opens with valid options |
| Clear required symbol field | Error shown |

**Verification Commands:**
```bash
# Run validation unit tests (20 tests)
pytest reflex_ag_grid/tests/test_validation.py -v

# Run E2E tests (includes editable page)
uv run python reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000
```

---

## Phase 3: Advanced Features

### Objective
Implement grouping, aggregation, notifications, and export functionality.

> **Note:** Most Phase 3 features were implemented in Phase 1. Remaining work is notification panel refinement.

### Checklist

- [x] **3.1** Row grouping support ✅ (Done in Phase 1 - Grouped Grid page)
  - [x] `rowGroup: true` in column def
  - [x] Group expansion/collapse
  - [x] `aggFunc` for summary values (sum, avg, count, min, max)
- [x] **3.2** Range selection and bulk updates ✅ (Done in Phase 1 - Range Selection page)
  - [x] `enableRangeSelection: true`
  - [x] Range selection demo
- [x] **3.3** Cell flashing on value change ✅ (Done in Phase 1 - Streaming page)
  - [x] `enableCellChangeFlash` prop
  - [x] `api.flashCells()` integration
- [x] **3.4** Notification panel component ✅
  - [x] `notification_panel.py` reusable component
  - [x] Click notification → jump to row (uses refs-based AG Grid API access)
  - [x] Notification types: info, warning, error, success
  - [x] `flash_on_jump` parameter for configurable highlight
  - [x] `route` parameter for cross-page navigation before jumping
  - [x] `jump_to_row()` standalone helper function exported
- [x] **3.5** Export functionality ✅ (Done in Phase 1)
  - [x] Excel export via `exportDataAsExcel()`
  - [x] CSV export via `exportDataAsCsv()`
  - [x] Export buttons in demo app
- [x] **3.6** Jump to row functionality ✅ (Uses refs API: `refs['ref_{grid_id}'].current.api`)
  - [x] `ensureNodeVisible()` + `flashCells()`
  - [x] Triggered from notifications
  - [x] Works on streaming page with correct ref name
- [x] **3.7** Write integration tests ✅
  - [x] Grouped grid tests (3 E2E tests)
  - [x] Streaming page tests (2 E2E tests)
- [x] **3.8** Update documentation ✅
  - [x] Added notification panel section to README

### Future Enhancement: Cross-Page Navigation with Highlighting ✅

> [!NOTE]
> This enhancement allows notifications to navigate to a different page/table and then highlight a specific row or cell.

**Implemented Features:**
- [x] **3.9** Enhanced cross-page navigation ✅
  - [x] `pending_highlight` state for storing target row
  - [x] `navigate_and_highlight(route, grid_id, row_id)` method
  - [x] `execute_pending_highlight(grid_id)` called on grid ready
  - [x] Jump Demo page at `/jump-demo` with navigation buttons
  - [x] Supports multiple grids via grid_id

**Example API:**
```python
# Notification with cross-page navigation
notification = {
    "message": "Price alert for AAPL",
    "row_id": "row_3",
    "level": "warning",
    "route": "/portfolio-tools",           # Navigate to this page first
    "grid_id": "holdings_grid",      # Target specific grid
    "highlight_field": "price",      # Highlight specific cell
    "highlight_style": "flash",      # flash | border | bg-color
}

# Or programmatic jump
def jump_to_cell(grid_id: str, row_id: str, field: str = None) -> rx.EventSpec:
    """Jump to a specific cell in a grid, optionally on another page."""
    pass
```

**Implementation Notes:**
1. Store target row/cell in URL or session state before navigation
2. On grid ready, check for pending highlight and execute
3. Support multiple highlight styles via CSS classes
4. Add E2E tests for cross-page navigation flow

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

## Phase 4: Documentation & Polish ✅ (In Progress)

### Objective
Finalize documentation, create migration guide, ensure package is ready for reuse.

### Checklist

- [x] **4.1** Split demo app into modular files ✅
  - [x] Create `demo_app/pages/` directory
  - [x] Extract each page to separate file:
    - [x] `pages/index.py` - Basic Grid
    - [x] `pages/editable.py` - Editable Grid
    - [x] `pages/validation.py` - Validation Demo
    - [x] `pages/grouped.py` - Grouped Grid
    - [x] `pages/streaming.py` - Streaming Data
    - [x] `pages/range.py` - Range Selection
    - [x] `pages/column_state.py` - Column State
    - [x] `pages/search.py` - Global Search
    - [x] `pages/jump_demo.py` - Cross-Page Jump Demo
  - [x] Create `components/` directory for shared components:
    - [x] `components/nav_bar.py` - Navigation bar
    - [x] `components/notification_panel.py` - Notification panel
    - [x] `components/status_badge.py` - Status badge
  - [x] Create `state.py` for DemoState class
  - [x] Create `columns.py` for column definitions
  - [x] Add inline documentation to all files
  - [x] Update main app to import from modules
  - [x] E2E tests pass: 21/21 ✅

- [x] **4.2** Create 15 aligned demo pages (one per requirement) ✅
  - [x] Reorganize demo pages to match requirements 1:1
  - [x] All 15 pages created with `req##_` naming convention:

    | Req # | Requirement | Demo Page | Route | Status |
    |-------|-------------|-----------|-------|--------|
    | 1 | Context Menu | `req01_context_menu.py` | `/01-context-menu` | ✅ Done |
    | 2 | Range Selection | `req02_range_selection.py` | `/02-range-selection` | ✅ Done |
    | 3 | Cell Flash | `req03_cell_flash.py` | `/03-cell-flash` | ✅ Done |
    | 4 | Jump & Highlight | `req04_jump_highlight.py` | `/04-jump-highlight` | ✅ Done |
    | 5 | Grouping & Summary | `req05_grouping.py` | `/05-grouping` | ✅ Done |
    | 6 | Notifications | `req06_notifications.py` | `/06-notifications` | ✅ Done |
    | 7 | Validation | `req07_validation.py` | `/07-validation` | ✅ Done |
    | 8 | Clipboard | `req08_clipboard.py` | `/08-clipboard` | ✅ Done |
    | 9 | Excel Export | `req09_excel_export.py` | `/09-excel-export` | ✅ Done |
    | 10 | WebSocket | `req10_websocket.py` | `/10-websocket` | ✅ Done |
    | 11 | Cell Editors | `req11_cell_editors.py` | `/11-cell-editors` | ✅ Done |
    | 12 | Edit Pause | `req12_edit_pause.py` | `/12-edit-pause` | ✅ Done |
    | 13 | Transaction API | `req13_transaction_api.py` | `/13-transaction-api` | ✅ Done |
    | 14 | Background Tasks | `req14_background_tasks.py` | `/14-background-tasks` | ✅ Done |
    | 15 | Column State | `req15_column_state.py` | `/15-column-state` | ✅ Done |

  - [x] Pages renamed to `req##_` naming convention (all created fresh)
  - [x] Old pages removed (index.py, streaming.py, search.py, etc.)
  - [x] Navigation and routes updated

  **Remaining Enhancements:**
  - [x] `req08_clipboard.py` - Enable copying from a single cell (not just range selection) ✅

- [x] **4.3** Create documentation aligned with demo pages ✅
  - [x] Create `reflex_ag_grid/docs/` directory
  - [x] Create doc page for each requirement (linking to demo):

    | Doc File | Links To Demo | Requirement | Status |
    |----------|---------------|-------------|--------|
    | `01_context_menu.md` | `/01-context-menu` | Right-click context menu | ✅ |
    | `02_range_selection.md` | `/02-range-selection` | Bulk state changes | ✅ |
    | `03_cell_flash.md` | `/03-cell-flash` | Blinking cell changes | ✅ |
    | `04_jump_highlight.md` | `/04-jump-highlight` | Notification jump & highlight | ✅ |
    | `05_grouping.md` | `/05-grouping` | Grouping & Summary | ✅ |
    | `06_notifications.md` | `/06-notifications` | Notification publisher | ✅ |
    | `07_validation.md` | `/07-validation` | Data Validation | ✅ |
    | `08_clipboard.md` | `/08-clipboard` | Copy cell / with header | ✅ |
    | `09_excel_export.md` | `/09-excel-export` | Export Excel | ✅ |
    | `10_websocket.md` | `/10-websocket` | WebSocket publishing | ✅ |
    | `11_cell_editors.md` | `/11-cell-editors` | Different Cell Editors | ✅ |
    | `12_edit_pause.md` | `/12-edit-pause` | Disable auto-refresh on edit | ✅ |
    | `13_transaction_api.md` | `/13-transaction-api` | Cell-by-cell update | ✅ |
    | `14_background_tasks.md` | `/14-background-tasks` | Update timing | ✅ |
    | `15_column_state.md` | `/15-column-state` | Save table format | ✅ |

  - [x] Each doc includes:
    - [x] Requirement description
    - [x] AG Grid feature used  
    - [x] Link to live demo page
    - [x] Code example
    - [x] How to implement in your app

- [x] **4.4** Complete `reflex_ag_grid/README.md` ✅
  - [x] Installation instructions
  - [x] Quick start guide
  - [x] API reference (column definitions, value formatters, events)
  - [x] Configuration examples
  - [x] Links to detailed docs

- [x] **4.5** Create migration guide ✅
  - [x] Step-by-step migration from `rx.el.table`
  - [x] Common patterns and solutions
  - [x] Troubleshooting guide

- [x] **4.6** Add inline code documentation ✅
  - [x] Docstrings for all public functions
  - [x] Type hints throughout

- [x] **4.7** Create example gallery ✅
  - [x] Example Gallery page created (`/`) with ALL 15 demo pages
  - [x] Basic categories and advanced features covered
  - [x] Visual index for all requirements

- [x] **4.8** Performance optimization review ✅
  - [x] Review large table performance
  - [x] Document best practices (`docs/performance.md`)

- [x] **4.9** Final cleanup ✅
  - [x] Remove deprecated code
  - [x] Consistent code style
  - [x] Update all imports

- [x] **4.10** Move notification_panel out of main package ✅
  > Keep `reflex_ag_grid` focused purely on AG Grid. notification_panel is a demo component.
  
  - [x] Remove from `reflex_ag_grid/components/`:
    - [x] Remove `notification_panel.py`
    - [x] Remove notification-related code from `ag_grid_state.py`:
      - `add_notification()`
      - `clear_notification()`
      - `clear_all_notifications()`
      - `notifications` state variable
  - [x] Move to `reflex_ag_grid/examples/demo_app/ag_grid_demo/components/`:
    - [x] `notification_panel.py` already exists in demo components
    - [x] Notification state kept in demo app's `DemoState`
  - [x] Update imports:
    - [x] Removed from `reflex_ag_grid/__init__.py` exports
    - [x] Demo app uses local component
  - [x] Update documentation:
    - [x] Updated `06_notifications.md` to show demo-only pattern
    - [x] Updated README to note notification_panel is demo-only

- [x] **4.11** Refactor AG Grid components for LLM-friendly maintenance ✅
  > Use `.agents/skills/superpowers` principles. Keep code precise, modular, and easy to maintain or improve for LLM coders.
  
  - [x] Review `reflex_ag_grid/components/ag_grid.py`:
    - [x] Extracted `_get_theme_class_name()` helper function
    - [x] Added module docstring with usage example
    - [x] Improved all class/function docstrings with examples
    - [x] Grouped props with clear section headers
    - [x] Extracted `_CELL_EVENT_EXCLUDE_KEYS` and `_ROW_EVENT_EXCLUDE_KEYS` constants
  - [x] Review `reflex_ag_grid/components/ag_grid_state.py`:
    - [x] Methods already well-structured
    - [x] Added examples to all public method docstrings
    - [x] Improved section organization with headers
  - [x] General improvements:
    - [x] All functions do ONE thing
    - [x] Nesting depth ≤3 levels
    - [x] Descriptive variable names
    - [x] Consistent code style

### Testing Plan - Phase 4

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

## Phase 5: Pilot Migration - Market Data Table ✅

### Objective
Migrate `market_data_table.py` as the first real table to validate the wrapper.

### Checklist

- [x] **5.1** Analyze current `market_data_table.py`
  - [x] Document current columns and data types (11 columns in MarketDataItem)
  - [x] Document current styling/behavior (header_cell, text_cell helpers)
- [x] **5.2** Create column definition config
  - [x] Define columns: ticker, listed_shares, last_volume, last_price, vwap_price, bid, ask, chg_1d_pct, implied_vol_pct, market_status, created_by
  - [x] Set types, filters
- [x] **5.3** Create `market_data_ag_grid.py` using wrapper
  - [x] Use `ag_grid()` component with column defs
  - [x] Wire up to `MarketDataState.filtered_market_data`
  - [x] Add quick_filter_text integration with existing search
- [x] **5.4** Validation (deferred - see 5.9)
  - [x] Grid renders correctly with all 11 columns
  - [x] Sorting works (click headers)
  - [x] Filtering available (column filters)
- [x] **5.5** Style matching
  - [x] Quartz theme applied
  - [x] Dark/light theme support via `rx.color_mode_cond`
  - [ ] Custom cell renderers (deferred - see 5.9)
- [x] **5.6** Update all usages
  - [x] `market_data_page.py` - updated to use `market_data_ag_grid`
  - [x] `contextual_workspace.py` - updated import and usage
- [x] **5.7** Remove old implementation
  - [x] Deleted `market_data_table.py`
  - [x] Removed exports from `__init__.py`
  - [x] Removed exports from `market_data_views.py`
- [x] **5.8** Document migration learnings (see Lessons Learned below)

### ⚠️ Lessons Learned - Phase 5 (AG Grid React Cell Renderers)

> [!CAUTION]
> **AG-Grid React Cell Renderer Limitation**
> 
> Custom `cell_renderer` functions that return `document.createElement` DOM elements crash with:
> `Error: Objects are not valid as a React child (found: [object HTMLSpanElement])`
> 
> HTML string returns (template literals) are escaped and displayed as text.

**Failed Approaches:**
1. ❌ Returning HTML strings: `return \`<span style='color: blue'>${val}</span>\``
   - AG-Grid escapes the HTML and displays it as text
2. ❌ Returning DOM elements: `return document.createElement('span')`
   - React throws "Objects are not valid as a React child"

**Deferred to Phase 5.9:** Investigate proper React-based cell renderers.

### Testing Plan - Phase 5

| Test Type | Test Case | Expected Result | Status |
|-----------|-----------|-----------------|--------|
| Visual | Grid renders with all columns | ✅ 11 columns visible | Passed |
| Functional | Sort by column | ✅ Sorting works | Passed |
| Functional | Filter by column | ✅ Column filters available | Passed |
| Functional | Quick filter search | ✅ Filters across all columns | Passed |
| Theme | Dark/light mode | ✅ Theme switches correctly | Passed |

---

## Phase 5.9: React Cell Renderer Support (NEW)

### Objective
Investigate and implement proper React-based cell renderers for AG-Grid to support custom styling (colored text, badges, etc.).

### Background
During Phase 5 migration, we discovered that AG-Grid React doesn't support:
1. JavaScript functions returning DOM elements (crashes React)
2. HTML string returns (escaped as text)

This new requirement will investigate the proper approach for custom cell renderers in AG-Grid React.

### Checklist

- [ ] **5.9.1** Research AG-Grid React cell renderer patterns
  - [ ] Review AG-Grid docs for React component cell renderers
  - [ ] Check if `cellStyle` function can handle conditional styling
  - [ ] Investigate `cellClass` for CSS-based styling
- [ ] **5.9.2** Update `reflex_ag_grid/components/ag_grid.py` wrapper
  - [ ] Add support for React component cell renderers
  - [ ] Add `cell_style` prop for function-based styling
  - [ ] Add `cell_class` prop for CSS class-based styling
  - [ ] Document the approach in `reflex_ag_grid/README.md`
- [ ] **5.9.3** Create demo page for cell renderers
  - [ ] Add `/16-cell-renderers` page to demo app
  - [ ] Show colored text examples
  - [ ] Show badge/pill styling examples
  - [ ] Show conditional formatting examples
- [ ] **5.9.4** Apply to Market Data table
  - [ ] Update `market_data_ag_grid.py` with proper cell styling:
    - [ ] Ticker column - blue link style
    - [ ] 1D Change % - green/red based on value
    - [ ] Market Status - badge styling
- [ ] **5.9.5** Documentation
  - [ ] Create `docs/16_cell_renderers.md`
  - [ ] Update migration guide with cell renderer patterns

### Implementation Options to Investigate

1. **`cellStyle` function** - Returns inline styles based on value
   ```javascript
   cellStyle: params => ({ color: params.value >= 0 ? 'green' : 'red' })
   ```

2. **`cellClass` function** - Returns CSS class names
   ```javascript
   cellClass: params => params.value >= 0 ? 'positive-cell' : 'negative-cell'
   ```

3. **`cellClassRules`** - Object mapping classes to conditions
   ```javascript
   cellClassRules: {
     'positive-cell': params => params.value >= 0,
     'negative-cell': params => params.value < 0,
   }
   ```

4. **React Component Renderer** - Custom React component (requires investigation)

### Testing Plan - Phase 5.9

| Test Type | Test Case | Expected Result |
|-----------|-----------|-----------------|
| Visual | Ticker column blue | Text displays in blue color |
| Visual | 1D Change % colored | Green for positive, red for negative |
| Visual | Market Status badge | Rounded pill with background color |
| Integration | Theme switching | Styles work in both light/dark modes |

---

## Phase 6: Batch Migration

### Objective
Migrate remaining tables systematically using patterns from Phase 5.

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

### Testing Plan - Phase 6

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

## Appendix A: Original Requirements Analysis

### Status
**Current Stage**: Phase 1 Complete ✅ (AG Grid 32.3.0)

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

### Python (via pyproject.toml)
```toml
[project]
dependencies = [
    "reflex>=0.8.26",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "playwright>=1.57.0",
    "pytest>=8.0",
]
```

### JavaScript (via lib_dependencies - no package.json needed)
```python
# In ag_grid.py
library: str = "ag-grid-react@32.3.0"
lib_dependencies: list[str] = [
    "ag-grid-community@32.3.0",
    "ag-grid-enterprise@32.3.0",
]
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

### Phase 1: Core Wrapper ✅ (12/12 Complete)
- [x] 1.1 Package structure setup
- [x] 1.2 ~~JS wrapper~~ (using npm imports)
- [x] 1.3 Reflex custom component
- [x] 1.4 Base state mixin
- [x] 1.5 Package dependencies (AG Grid 32.3.0)
- [x] 1.6 Unit tests (17 serialization tests)
- [x] 1.7 Basic example
- [x] 1.8 Demo app (7 pages)
- [x] 1.9 E2E tests (12/12 passed)
- [x] 1.10 Demo requirements coverage ✅ (15/15 reqs)
- [x] 1.11 Standalone package setup ✅
- [x] 1.12 Global search / Quick filter ✅

### Phase 2: Validation & Editing ✅ (7/7 Complete)
- [x] 2.1 Validation loader ✅
- [x] 2.2 JS validation integration ✅
- [x] 2.3 Cell editor config ✅
- [x] 2.4 Edit event handling ✅
- [x] 2.5 Example config ✅
- [x] 2.6 Validation tests (20 passing) ✅
- [x] 2.7 Documentation ✅

### Phase 3: Advanced Features ✅ (8/8 Complete)
- [x] 3.1 Row grouping ✅
- [x] 3.2 Range selection ✅
- [x] 3.3 Cell flashing ✅
- [x] 3.4 Notification panel (reusable) ✅
- [x] 3.5 Export functionality ✅
- [x] 3.6 Jump to row ✅
- [x] 3.7 Integration tests ✅
- [x] 3.8 Documentation ✅

### Phase 4: Pilot Migration (Market Data Table)
- [ ] 4.1 Analyze market_data_table
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
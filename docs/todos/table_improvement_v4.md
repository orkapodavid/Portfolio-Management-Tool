# AG Grid Reflex Wrapper - Phase 4 Implementation Plan

> **For AI Assistants:** Follow task checklists in order. Test demo pages in browser after changes. Use `uv run reflex run` from `reflex_ag_grid/examples/demo_app`.

**Goal:** Fix overlay props and implement additional improvements to the AG Grid wrapper.

**Tech Stack:** Reflex Python, AG Grid Enterprise 35.0.1, React 18

---

## Implementation Status

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | Overlay Props | ✅ Complete | Fixed `loading`, `overlay_loading_template`, `overlay_no_rows_template` |

---

## Requirement 1: Fix Overlay Props

**Problem:** Overlays don't work on `/20-overlays` demo page.

**Root Cause:** The `ag_grid.py` component does NOT define the following props:
- `loading: bool` - Shows/hides loading overlay
- `overlay_loading_template: str` - Custom loading message HTML
- `overlay_no_rows_template: str` - Custom no-rows message HTML

The demo page passes these props but they are silently ignored.

### AG Grid v35 Overlay API

| Prop | Type | Description |
|------|------|-------------|
| `loading` | `boolean` | When `true`, shows loading overlay |
| `overlayLoadingTemplate` | `string` | HTML template for loading overlay |
| `overlayNoRowsTemplate` | `string` | HTML template for no-rows overlay |

### Files to Modify

#### [MODIFY] [ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/reflex_ag_grid/components/ag_grid.py)

Add new props after the "Suppress Events" section (~line 510):

```python
# -------------------------------------------------------------------------
# Overlays
# -------------------------------------------------------------------------
loading: rx.Var[bool] = False
overlay_loading_template: rx.Var[str] | None = None
overlay_no_rows_template: rx.Var[str] | None = None
suppress_no_rows_overlay: rx.Var[bool] = False
```

**No changes needed in `create()` method** - these props are passed through normally.

### Verification Plan

#### Automated Verification (Browser Subagent)

1. Navigate to `http://localhost:3000/20-overlays`
2. Click "Load Data" button
3. Verify loading overlay with "Loading data..." text appears during 2-second delay
4. Verify 3 rows appear after loading
5. Click "Clear" button
6. Verify no-rows overlay with custom message appears

#### Manual Verification

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
# Open http://localhost:3000/20-overlays
```

Expected behavior:
- Initial state: "No Rows To Show" overlay visible
- Load Data clicked: "Loading data..." overlay visible for 2s
- Data loaded: 3 rows displayed, no overlay
- Clear clicked: Custom "No rows to display..." message

---

## Summary

| Phase | Description | Status |
|-------|-------------|--------|
| 4.1 | Overlay Props | ✅ Complete |
| 4.2 | Tree Data Props | ✅ Complete |
| 4.3 | Status Bar Props | ✅ Complete |

---

## Requirement 2: Tree Data Props Fix

**Problem:** Tree data on `/17-tree-data` rendered as flat list instead of hierarchy.

**Root Cause:** The `tree_data` and `get_data_path` props were not recognized, causing Reflex to serialize them into `css:{}` instead of top-level props.

### Solution
1. Props were already defined in `ag_grid.py`:
```python
tree_data: rx.Var[bool] = rx.Var.create(False)
get_data_path: rx.Var | None = None
```

2. **Critical Step:** Must reinstall package in demo_app after modifying component attributes:
```bash
cd reflex_ag_grid/examples/demo_app
uv sync --reinstall-package reflex-ag-grid
```

### Key Learning
When modifying `rx.Component` class attributes in an editable package, the consuming project's venv may have a stale version. Always run `uv sync --reinstall-package` after changes.

### Verification
Check props are recognized:
```python
from reflex_ag_grid.components.ag_grid import AgGrid
print('tree_data in props:', 'tree_data' in AgGrid.get_props())  # Should be True
```

---

## Requirement 3: Status Bar Props Fix

**Problem:** Status bar not visible on `/19-status-bar` page.

**Root Cause:** The `status_bar` prop was NOT defined in `ag_grid.py`.

### Solution
Added to `ag_grid.py`:
```python
# Status Bar (Enterprise)
status_bar: rx.Var[dict[str, Any]] | None = None
```

### Built-in Status Panel Components

| Panel | Description |
|-------|-------------|
| `agTotalRowCountComponent` | Total row count |
| `agFilteredRowCountComponent` | Filtered row count |
| `agSelectedRowCountComponent` | Selected row count |
| `agAggregationComponent` | Sum/Avg/Min/Max of selected cells |
| `agTotalAndFilteredRowCountComponent` | Combined total and filtered count |

**Estimated Time:** 1-2 hours

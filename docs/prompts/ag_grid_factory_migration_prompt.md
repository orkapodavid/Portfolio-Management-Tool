# AG Grid Factory Migration Prompt

## Objective
Migrate all remaining AG Grid components to use the `create_standard_grid()` factory from `app/components/shared/ag_grid_config.py`.

---

## Migration Pattern

### Before (Old Pattern)
```python
import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.module.state import SomeState

def my_grid() -> rx.Component:
    return ag_grid(
        id="my_grid",
        row_data=SomeState.data,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
```

### After (New Pattern with Export Button)
```python
import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.module.state import SomeState
from app.components.shared.ag_grid_config import create_standard_grid, export_button

def my_grid() -> rx.Component:
    return rx.vstack(
        # Export toolbar
        rx.hstack(
            export_button(),
            justify="end",
            width="100%",
            padding_bottom="2",
        ),
        # Grid
        create_standard_grid(
            grid_id="my_grid",
            row_data=SomeState.data,
            column_defs=_get_column_defs(),
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
```

---

## Export Button

The `export_button()` helper creates an Excel export button that finds the first AG Grid on the page:

```python
from app.components.shared.ag_grid_config import export_button

# Default size
export_button()

# Adjust button size (Radix size: "1", "2", "3")
export_button(button_size="1")
```

**Filename Pattern**: `<page_name>_YYYYMMDD_HHMM.xlsx` (e.g., `pnl_full_20260203_1050.xlsx`)

### Context Menu Export

To apply timestamped filenames to right-click Export → Excel/CSV:

```python
from app.components.shared.ag_grid_config import (
    get_default_export_params,
    get_default_csv_export_params,
)

create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    default_excel_export_params=get_default_export_params("my_table"),
    default_csv_export_params=get_default_csv_export_params("my_table"),
)
```

### Export Behavior

| Condition | Export Result |
|-----------|---------------|
| **No rows selected** | Exports all rows |
| **Some rows selected** | Exports only selected rows |

This applies to both toolbar button and context menu exports:
- **Excel**: `my_table_20260203_1050.xlsx`
- **CSV**: `my_table_20260203_1050.csv`

---

## Quick Filter

Instant search across all grid columns (AG Grid Community feature):

### 1. Add a State Class for the Grid

```python
class MyGridState(rx.State):
    """State for grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""
```

### 2. Add the Search Input to Toolbar

```python
from app.components.shared.ag_grid_config import quick_filter_input

rx.hstack(
    # Left side: Quick filter
    quick_filter_input(
        search_value=MyGridState.search_text,
        on_change=MyGridState.set_search,
        on_clear=MyGridState.clear_search,
    ),
    # Right side: Export and column buttons
    rx.hstack(
        export_button(page_name="my_table"),
        column_state_buttons(_STORAGE_KEY, show_save=True),
        gap="4",
    ),
    justify="between",
    width="100%",
    padding_bottom="2",
)
```

### 3. Pass Search Text to Grid

```python
create_standard_grid(
    grid_id="my_grid",
    row_data=SomeState.data,
    column_defs=_get_column_defs(),
    quick_filter_text=MyGridState.search_text,  # <-- Add this
)
```

**Behavior**:
- Searches across all visible columns instantly
- Case-insensitive by default
- Splits search by spaces (matches all words)

---

## Grid Toolbar (Recommended)

Use the `grid_toolbar` helper for a complete toolbar with proper button grouping:

```python
from app.components.shared.ag_grid_config import grid_state_script, grid_toolbar

_STORAGE_KEY = "my_grid_state"
_GRID_ID = "my_grid"

rx.vstack(
    # IMPORTANT: Pass grid_id to grid_state_script for SPA navigation support
    rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
    grid_toolbar(
        storage_key=_STORAGE_KEY,
        page_name="my_table",
        search_value=MyState.search_text,
        on_search_change=MyState.set_search,
        on_search_clear=MyState.clear_search,
        grid_id=_GRID_ID,            # Required for Compact toggle
        show_compact_toggle=True,     # Optional: Show Compact mode button
    ),
    create_standard_grid(
        grid_id=_GRID_ID,  # Must match grid_id in grid_toolbar and grid_state_script
        ...
    ),
)
```

**Visual Layout:**
```
[Search: _______________]     [Compact] | [Excel] | [Save Layout] [Restore] [Reset]
                              ↑ violet   ↑ green   ↑ blue        ↑ blue    ↑ red
```

**Color Scheme:**
- **Compact**: Violet (view toggle) → Green when active
- **Excel**: Green (data export)
- **Save/Restore**: Blue (layout actions grouped)
- **Reset**: Red (destructive action)

> [!IMPORTANT]
> When using `show_compact_toggle=True`, you MUST provide `grid_id` and it MUST match the `grid_id` in `create_standard_grid`. Without this, the Compact button won't appear.

---

## Grid State Persistence (Manual)

If you need individual control over buttons, use separate helpers:

```python
from app.components.shared.ag_grid_config import grid_state_script, grid_state_buttons

_STORAGE_KEY = "my_grid_state"
_GRID_ID = "my_grid"

rx.vstack(
    # IMPORTANT: Always pass grid_id as second argument for SPA navigation
    rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
    rx.hstack(
        export_button(page_name="my_table"),
        grid_state_buttons(_STORAGE_KEY),
    ),
    create_standard_grid(
        grid_id=_GRID_ID,
        ...
    ),
)
```

### What Gets Saved

| Category | State Saved |
|----------|-------------|
| **Columns** | Width, order, visibility, pinning |
| **Filters** | All column filter configurations |
| **Sorting** | Sort column and direction |

> [!CAUTION]
> **SPA Navigation Bug Fix**: Always pass `grid_id` to `grid_state_script()`. Without it, tab navigation in single-page apps can cause data corruption as the grid API selector defaults to the first `.ag-root-wrapper` on the page, which may target the wrong grid.

---


## Tier 2 Enhancements

Add these flags based on component category:

### Real-Time Grids (enable cell flash)
- `market_data/*.py`
- `pnl/*.py`
- `risk/*.py`

```python
create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    enable_cell_flash=True,  # Tier 2: Real-time
)
```

### Row Numbers (all grids)
Add automatic row numbering column to all grids:

```python
create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    enable_row_numbers=True,  # Tier 2: Row numbering
)
```

### Multi-Row Selection with Checkboxes
Enable checkbox selection for multiple rows:

```python
create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    enable_multi_select=True,  # Tier 2: Multi-row checkbox selection
)
```

**Note**: This enables AG Grid v35's `multiRow` selection mode with checkboxes. Users can select multiple rows using checkboxes or Ctrl/Cmd+Click. The status bar will show "Selected: X" when rows are selected.

### Compact Mode (Dense Rows)
Enable compact mode to reduce row height and fit more data per screen:

```python
create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    enable_compact_mode=True,  # Tier 2: Dense rows (28px vs default ~42px)
)
```

**Note**: Compact mode sets `row_height=28` and `header_height=32` for a denser display. This is ideal for data-heavy dashboards where screen real estate matters.

### Row Grouping (All Grids - Recommended)
Enable drag-to-group for all analytics grids:

```python
# On grid:
create_standard_grid(
    grid_id="...",
    row_data=...,
    column_defs=...,
    row_group_panel_show="always",  # Show grouping panel at top
    group_default_expanded=-1,       # Expand all groups (-1 = all)
    grand_total_row="bottom",        # Pin totals at bottom (optional)
)

# On columns (add to groupable fields):
ag_grid.column_def(
    field="underlying",
    enable_row_group=True,  # Allow dragging to group panel
)
ag_grid.column_def(
    field="pnl_ytd",
    enable_row_group=True,
    agg_func="sum",  # sum, avg, count, min, max
)
```

**Note**: Row grouping is an Enterprise feature. Use `agg_func="sum"` for amounts, `agg_func="avg"` for percentages/rates.

> [!WARNING]
> **Only use `grand_total_row` when columns have meaningful aggregations.** For grids with rates, ratios, or categorical data (e.g., FX rates, currency grids), omit `grand_total_row` to avoid an empty pinned row at the bottom.

### Categorical Columns (use Set Filter)
For columns with discrete values (status, sector, type, account, currency):

```python
ag_grid.column_def(
    field="status",
    header_name="Status",
    filter="agSetColumnFilter",  # Instead of AGFilters.text
    min_width=100,
)
```

### Column Pinning (Identifier Columns)
Pin key identifier columns to the left so they remain visible while scrolling:

```python
ag_grid.column_def(
    field="ticker",
    header_name="Ticker",
    filter=AGFilters.text,
    min_width=100,
    pinned="left",  # Always visible on left
)
```

**Use for**: `ticker`, `deal_num`, `id`, or other primary identifiers.

### Tooltips (Truncated Text)
Enable tooltips to show full text when cells are truncated:

```python
# Simple tooltip - show same field value
ag_grid.column_def(
    field="company_name",
    header_name="Company Name",
    tooltip_field="company_name",  # Show full text on hover
    min_width=150,
)

# Header tooltip for long column names
ag_grid.column_def(
    field="price_change_pct",
    header_name="Price Change %",
    header_tooltip="Percentage change in price from previous day",
    min_width=120,
)
```

> [!TIP]
> **Enable `tooltip_field` on ALL text columns by default.** This improves UX when columns are narrow.

### Auto-Size Strategy (Column Sizing)
Automatically size columns on grid load:

```python
create_standard_grid(
    grid_id="my_grid",
    row_data=SomeState.data,
    column_defs=_get_column_defs(),
    # Fit all columns to container width
    auto_size_strategy={"type": "fitGridWidth"},
)
```

**Options**:
- `{"type": "fitGridWidth"}` - Fit all columns to container
- `{"type": "fitCellContents"}` - Fit to content (may cause horizontal scroll)

### Lock Column Position (Prevent Moving)
Lock important columns in place to prevent accidental reordering:

```python
ag_grid.column_def(
    field="ticker",
    header_name="Ticker",
    lock_position=True,  # Cannot be moved by drag
    pinned="left",
)
```

---

## Best Practices (v35)

### Performance: Prefer Value Formatters over Cell Renderers

Value Formatters don't create extra DOM, while Cell Renderers do:

```python
# ✅ GOOD - Value Formatter (lightweight, no extra DOM)
ag_grid.column_def(
    field="price",
    value_formatter=rx.Var("(p) => '$' + p.value.toFixed(2)"),
)

# ❌ AVOID - Cell Renderer (creates extra DOM elements)
# Only use when you need interactive elements (buttons, links)
```

### Conditional Cell Styling Pattern

For financial grids with positive/negative values:

```python
_VALUE_STYLE = rx.Var("""(params) => {
    const val = String(params.value || '');
    const isNegative = val.startsWith('-') || val.startsWith('(');
    return {
        color: isNegative ? '#dc2626' : '#059669',
        fontWeight: '700',
        fontFamily: 'monospace'
    };
}""")

ag_grid.column_def(
    field="pnl_ytd",
    header_name="PnL YTD",
    cell_style=_VALUE_STYLE,  # Green for positive, red for negative
)
```

### Row Grouping (Enterprise)

Enable drag-to-group for analytics dashboards:

```python
# On grid:
create_standard_grid(
    ...,
    row_group_panel_show="always",  # Show grouping panel at top
    group_default_expanded=-1,       # Expand all groups (-1 = all)
    grand_total_row="bottom",        # Pin totals at bottom
)

# On columns:
ag_grid.column_def(
    field="underlying",
    enable_row_group=True,  # Allow dragging to group panel
)
ag_grid.column_def(
    field="pnl_ytd",
    enable_row_group=True,
    agg_func="sum",  # Aggregate: sum, avg, count, min, max
)
ag_grid.column_def(
    field="pnl_pct",
    agg_func="avg",  # Use avg for percentages
)
```

### Filter Types by Column Category

| Column Type | Filter | Example |
|-------------|--------|---------|
| Text/ID | `AGFilters.text` | ticker, symbol, name |
| Numeric | `AGFilters.number` | price, qty, amount |
| Date | `AGFilters.date` | trade_date, expiry |
| Categorical | `"agSetColumnFilter"` | status, sector, account |

### v35 Deprecations to Avoid

| ❌ Deprecated | ✅ Use Instead |
|---------------|----------------|
| `checkboxSelection` on column | `enable_multi_select=True` on grid |
| `headerCheckboxSelection` | Handled by wrapper |
| `row_selection="multiple"` | Wrapper auto-transforms to object format |
| `enable_range_selection` | `cell_selection=True` |

---

## Files to Migrate (42 remaining)

### compliance/ (0 remaining - COMPLETED)
- [x] `beneficial_ownership_ag_grid.py` - Migrated with compact toggle
- [x] `monthly_exercise_limit_ag_grid.py` - Migrated with compact toggle
- [x] `restricted_list_ag_grid.py` - Migrated with compact toggle

### emsx/ (0 remaining - COMPLETED)
- [x] `emsa_order_ag_grid.py` - Migrated with compact toggle
- [x] `emsa_route_ag_grid.py` - Migrated with compact toggle

### events/ (0 remaining - COMPLETED)
- [x] `event_calendar_ag_grid.py` - Migrated with compact toggle
- [x] `event_stream_ag_grid.py` - Migrated with compact toggle
- [x] `reverse_inquiry_ag_grid.py` - Migrated with compact toggle

### instruments/ (0 remaining - COMPLETED)
- [x] `instrument_data_ag_grid.py` - Migrated with compact toggle
- [x] `instrument_term_ag_grid.py` - Migrated with compact toggle
- [x] `special_term_ag_grid.py` - Migrated with compact toggle
- [x] `stock_screener_ag_grid.py` - Migrated with compact toggle
- [x] `ticker_data_ag_grid.py` - Migrated with compact toggle

### market_data/ (0 remaining - COMPLETED) - **Cell flash enabled**
- [x] `fx_data_ag_grid.py` - Migrated with cell flash & compact toggle
- [x] `historical_data_ag_grid.py` - Migrated with cell flash & compact toggle
- [x] `market_data_ag_grid.py` - Migrated with cell flash & compact toggle
- [x] `market_hours_ag_grid.py` - Migrated with cell flash & compact toggle
- [x] `trading_calendar_ag_grid.py` - Migrated with cell flash & compact toggle

### operations/ (0 remaining - COMPLETED)
- [x] `daily_procedure_check_ag_grid.py` - Migrated with compact toggle
- [x] `operation_process_ag_grid.py` - Migrated with compact toggle

### pnl/ (0 remaining - COMPLETED) - **Enable cell flash**
- [x] `pnl_change_ag_grid.py` - Migrated with compact toggle
- [x] `pnl_currency_ag_grid.py` - Migrated with compact toggle
- [x] `pnl_summary_ag_grid.py` - Migrated with compact toggle
- [x] `pnl_full_ag_grid.py` - Migrated with compact toggle

### portfolio_tools/ (9)
- [ ] `cb_installments_ag_grid.py`
- [ ] `coming_resets_ag_grid.py`
- [ ] `deal_indication_ag_grid.py`
- [ ] `excess_amount_ag_grid.py`
- [ ] `pay_to_hold_ag_grid.py`
- [ ] `po_settlement_ag_grid.py`
- [ ] `reset_dates_ag_grid.py`
- [ ] `short_ecl_ag_grid.py`
- [ ] `stock_borrow_ag_grid.py`

### positions/ (5)
- [ ] `bond_position_ag_grid.py`
- [ ] `positions_ag_grid.py`
- [ ] `stock_position_ag_grid.py`
- [ ] `trade_summary_ag_grid.py`
- [ ] `warrant_position_ag_grid.py`

### reconciliation/ (5)
- [ ] `failed_trades_ag_grid.py`
- [ ] `pnl_recon_ag_grid.py`
- [ ] `pps_recon_ag_grid.py`
- [ ] `risk_input_recon_ag_grid.py`
- [ ] `settlement_recon_ag_grid.py`

### risk/ (3) - **Enable cell flash**
- [ ] `delta_change_ag_grid.py`
- [ ] `risk_inputs_ag_grid.py`
- [ ] `risk_measures_ag_grid.py`

---

## Verification

After migration, verify:
1. ✅ Export buttons (Excel, CSV) visible at top right  
2. ✅ Export buttons trigger file download  
3. ✅ Status bar shows row counts at bottom  
4. ✅ Range selection works (drag to select cells)  
5. ✅ Floating filters appear under headers  
6. ✅ Empty grids show "No rows to display"  
7. ✅ Cell flash works on real-time grids (if enabled)
8. ✅ Tab navigation between grids preserves correct data

---

## Troubleshooting

### Data Disappears When Switching Tabs (SPA Navigation)

**Symptom**: Clicking between tabs (e.g., PnL Change → PnL Currency) causes data to disappear, show wrong columns, or display data from another grid.

**Cause**: `grid_state_script()` was not passed a `grid_id`, so it defaults to `document.querySelector('.ag-root-wrapper')` which returns the **first grid** on the page instead of the intended grid.

**Fix**: Always pass `grid_id` as the second argument:

```python
# ❌ BAD - No grid_id, targets first grid on page
rx.script(grid_state_script(_STORAGE_KEY))

# ✅ GOOD - Targets specific grid by ID
rx.script(grid_state_script(_STORAGE_KEY, "my_grid_id"))
```

Make sure `grid_id` matches between:
- `grid_state_script(_STORAGE_KEY, grid_id)`
- `grid_toolbar(..., grid_id=grid_id)`
- `create_standard_grid(grid_id=grid_id, ...)`

### Empty Row at Bottom of Grid

**Symptom**: An empty row appears pinned at the bottom of the grid.

**Cause**: Using `grand_total_row="bottom"` when columns don't have aggregation functions (`agg_func`).

**Fix**: Only use `grand_total_row` on grids where numeric columns have `agg_func="sum"` or `agg_func="avg"`. For grids with rates, ratios, or categorical data, omit `grand_total_row`.

```python
# ❌ BAD - Columns without agg_func will show empty cells
create_standard_grid(
    ...,
    grand_total_row="bottom",  # Remove this
)

# ✅ GOOD - Only enable when aggregations are meaningful
create_standard_grid(
    ...,
    # grand_total_row omitted for currency/rate grids
)
```

### Compact Toggle Not Appearing

**Symptom**: The Compact button doesn't show in the toolbar despite `show_compact_toggle=True`.

**Cause**: Missing or mismatched `grid_id` between `grid_toolbar` and `create_standard_grid`.

**Fix**: Ensure both use the exact same `grid_id`:

```python
_GRID_ID = "my_grid"

grid_toolbar(
    ...,
    grid_id=_GRID_ID,  # Must match
    show_compact_toggle=True,
)
create_standard_grid(
    grid_id=_GRID_ID,  # Must match
    ...
)
```

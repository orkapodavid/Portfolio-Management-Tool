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

rx.vstack(
    rx.script(grid_state_script(_STORAGE_KEY)),
    grid_toolbar(
        storage_key=_STORAGE_KEY,
        page_name="my_table",
        search_value=MyState.search_text,
        on_search_change=MyState.set_search,
        on_search_clear=MyState.clear_search,
        grid_id="my_grid",           # Required for Compact toggle
        show_compact_toggle=True,     # Optional: Show Compact mode button
    ),
    create_standard_grid(
        grid_id="my_grid",  # Must match grid_id in grid_toolbar
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

rx.vstack(
    rx.script(grid_state_script(_STORAGE_KEY)),
    rx.hstack(
        export_button(page_name="my_table"),
        grid_state_buttons(_STORAGE_KEY),
    ),
    create_standard_grid(...),
)
```

### What Gets Saved

| Category | State Saved |
|----------|-------------|
| **Columns** | Width, order, visibility, pinning |
| **Filters** | All column filter configurations |
| **Sorting** | Sort column and direction |

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

## Files to Migrate (45 remaining)

### compliance/ (3 remaining)
- [ ] `beneficial_ownership_ag_grid.py`
- [ ] `monthly_exercise_limit_ag_grid.py`
- [ ] `restricted_list_ag_grid.py`

### emsx/ (2)
- [ ] `emsa_order_ag_grid.py`
- [ ] `emsa_route_ag_grid.py`

### events/ (3)
- [ ] `event_calendar_ag_grid.py`
- [ ] `event_stream_ag_grid.py`
- [ ] `reverse_inquiry_ag_grid.py`

### instruments/ (5)
- [ ] `instrument_data_ag_grid.py`
- [ ] `instrument_term_ag_grid.py`
- [ ] `special_term_ag_grid.py`
- [ ] `stock_screener_ag_grid.py`
- [ ] `ticker_data_ag_grid.py`

### market_data/ (5) - **Enable cell flash**
- [ ] `fx_data_ag_grid.py`
- [ ] `historical_data_ag_grid.py`
- [ ] `market_data_ag_grid.py`
- [ ] `market_hours_ag_grid.py`
- [ ] `trading_calendar_ag_grid.py`

### operations/ (2)
- [ ] `daily_procedure_check_ag_grid.py`
- [ ] `operation_process_ag_grid.py`

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


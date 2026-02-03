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

## Column State Persistence

Save and restore column layout (order, widths, visibility):

```python
from app.components.shared.ag_grid_config import column_state_buttons

# Define a unique storage key for this grid
_STORAGE_KEY = "my_grid_column_state"

# Add to toolbar alongside export button
rx.hstack(
    export_button(page_name="my_table"),
    column_state_buttons(_STORAGE_KEY, show_save=True),
    justify="end",
    width="100%",
    gap="4",
)
```

**Buttons provided**:
- **Save Layout** - Manually save current column layout
- **Restore** - Restore saved layout
- **Reset** - Reset to default column order

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

### pnl/ (3 remaining) - **Enable cell flash**
- [ ] `pnl_change_ag_grid.py`
- [ ] `pnl_currency_ag_grid.py`
- [ ] `pnl_summary_ag_grid.py`

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


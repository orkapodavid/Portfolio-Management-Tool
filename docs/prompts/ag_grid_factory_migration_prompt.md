# AG Grid Factory Migration

## Quick Start

Use `create_standard_grid()` with `grid_toolbar()` for all grids:

```python
from app.components.shared.ag_grid_config import (
    create_standard_grid, grid_state_script, grid_toolbar
)

_STORAGE_KEY = "my_grid_state"
_GRID_ID = "my_grid"

def my_component() -> rx.Component:
    return rx.vstack(
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="my_table",
            search_value=MyState.search_text,
            on_search_change=MyState.set_search,
            on_search_clear=MyState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MyState.data,
            column_defs=_get_column_defs(),
        ),
    )
```

**Toolbar Layout:**
```
[Search: _______________]     [Compact] | [Excel] | [Save] [Restore] [Reset]
                              ↑ violet   ↑ green   ↑ blue  ↑ blue    ↑ red
```

---

## Tier 2 Enhancements

Add flags based on component needs:

```python
create_standard_grid(
    grid_id="my_grid",
    row_data=MyState.data,
    column_defs=_get_column_defs(),
    # Tier 2 options:
    enable_cell_flash=True,      # Real-time grids (market_data/, pnl/, risk/)
    enable_row_numbers=True,     # Auto row numbering
    enable_multi_select=True,    # Checkbox selection
    enable_compact_mode=True,    # Dense rows (28px)
    row_group_panel_show="always",  # Enable drag-to-group
    group_default_expanded=-1,      # Expand all groups
    grand_total_row="bottom",       # Pinned totals (only with agg_func columns)
)
```

---

## Column Definitions

### Filters by Type

| Column Type | Filter | Example |
|-------------|--------|---------|
| Text/ID | `AGFilters.text` | ticker, symbol |
| Numeric | `AGFilters.number` | price, qty |
| Date | `AGFilters.date` | trade_date |
| Categorical | `"agSetColumnFilter"` | status, sector |

### Common Column Options

```python
ag_grid.column_def(
    field="ticker",
    header_name="Ticker",
    filter=AGFilters.text,
    pinned="left",              # Keep visible on scroll
    lock_position=True,         # Prevent drag reorder
    tooltip_field="ticker",     # Show full text on hover
    min_width=100,
)

ag_grid.column_def(
    field="pnl_ytd",
    enable_row_group=True,      # Allow drag to group panel
    agg_func="sum",             # sum, avg, count, min, max
)
```

### Value Formatting (Lightweight)

```python
# ✅ Use value formatters (no extra DOM)
ag_grid.column_def(
    field="price",
    value_formatter=rx.Var("(p) => '$' + p.value.toFixed(2)"),
)

# For financial values (green/red)
_VALUE_STYLE = rx.Var("""(params) => {
    const val = String(params.value || '');
    const isNegative = val.startsWith('-') || val.startsWith('(');
    return {
        color: isNegative ? '#dc2626' : '#059669',
        fontWeight: '700',
        fontFamily: 'monospace'
    };
}""")

ag_grid.column_def(field="pnl", cell_style=_VALUE_STYLE)
```

---

## Export Parameters

For context menu exports with timestamped filenames:

```python
from app.components.shared.ag_grid_config import (
    get_default_export_params, get_default_csv_export_params
)

create_standard_grid(
    grid_id="my_grid",
    ...,
    default_excel_export_params=get_default_export_params("my_table"),
    default_csv_export_params=get_default_csv_export_params("my_table"),
)
```

**Export Behavior**: No selection → all rows; rows selected → selected only.

---

## Troubleshooting

### Data Disappears When Switching Tabs

**Fix**: Pass `grid_id` to `grid_state_script`:

```python
# ✅ Correct
rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID))
```

### Empty Row at Bottom

**Fix**: Remove `grand_total_row` if columns lack `agg_func`.

### Compact Toggle Not Appearing

**Fix**: Ensure `grid_id` matches in both `grid_toolbar()` and `create_standard_grid()`.

---

## Grid Files (48 components)

### compliance/ (4)
- `beneficial_ownership_ag_grid.py`
- `monthly_exercise_limit_ag_grid.py`
- `restricted_list_ag_grid.py`
- `undertakings_ag_grid.py`

### emsx/ (2)
- `emsa_order_ag_grid.py`
- `emsa_route_ag_grid.py`

### events/ (3)
- `event_calendar_ag_grid.py`
- `event_stream_ag_grid.py`
- `reverse_inquiry_ag_grid.py`

### instruments/ (5)
- `instrument_data_ag_grid.py`
- `instrument_term_ag_grid.py`
- `special_term_ag_grid.py`
- `stock_screener_ag_grid.py`
- `ticker_data_ag_grid.py`

### market_data/ (5) — *cell flash enabled*
- `fx_data_ag_grid.py`
- `historical_data_ag_grid.py`
- `market_data_ag_grid.py`
- `market_hours_ag_grid.py`
- `trading_calendar_ag_grid.py`

### operations/ (2)
- `daily_procedure_check_ag_grid.py`
- `operation_process_ag_grid.py`

### pnl/ (4) — *cell flash enabled*
- `pnl_change_ag_grid.py`
- `pnl_currency_ag_grid.py`
- `pnl_full_ag_grid.py`
- `pnl_summary_ag_grid.py`

### portfolio_tools/ (9)
- `cb_installments_ag_grid.py`
- `coming_resets_ag_grid.py`
- `deal_indication_ag_grid.py`
- `excess_amount_ag_grid.py`
- `pay_to_hold_ag_grid.py`
- `po_settlement_ag_grid.py`
- `reset_dates_ag_grid.py`
- `short_ecl_ag_grid.py`
- `stock_borrow_ag_grid.py`

### positions/ (5)
- `bond_position_ag_grid.py`
- `positions_ag_grid.py`
- `stock_position_ag_grid.py`
- `trade_summary_ag_grid.py`
- `warrant_position_ag_grid.py`

### reconciliation/ (5)
- `failed_trades_ag_grid.py`
- `pnl_recon_ag_grid.py`
- `pps_recon_ag_grid.py`
- `risk_input_recon_ag_grid.py`
- `settlement_recon_ag_grid.py`

### risk/ (3) — *cell flash enabled*
- `delta_change_ag_grid.py`
- `risk_inputs_ag_grid.py`
- `risk_measures_ag_grid.py`

### shared/ (1)
- `ag_grid_config.py` — Factory and utilities

---

## v35 Notes

| ❌ Deprecated | ✅ Use Instead |
|---------------|----------------|
| `checkboxSelection` on column | `enable_multi_select=True` |
| `row_selection="multiple"` | Wrapper auto-transforms |
| `enable_range_selection` | `cell_selection=True` |

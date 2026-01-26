# AG-Grid Batch Migration Prompt: Phases 6.2 - 6.11

## Objective
Complete the batch migration of 44 remaining `rx.el.table` tables to AG-Grid across 10 components. Each phase follows a **split-then-migrate** workflow. **Do not stop until all tables are migrated and tested.**

---

## Base URL
All routes use: `http://localhost:3001/pmt/` prefix.

---

## Migration Pattern (MUST FOLLOW)

Use this exact template for every AG-Grid component:

```python
"""
[Component Name] AG-Grid Component.

AG-Grid based implementation for [description], replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.[module].[state_file] import [StateClass]


# =============================================================================
# CELL STYLES (if needed)
# =============================================================================

# Example: Link style for clickable text
_LINK_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Example: Conditional color based on value
_VALUE_STYLE = rx.Var(
    """(params) => {
        const val = parseFloat(params.value);
        if (isNaN(val)) return {};
        return { color: val >= 0 ? '#059669' : '#dc2626', fontWeight: '500' };
    }"""
)

# Example: Status badge style (for Success/Failed/Active/Inactive)
_STATUS_STYLE = rx.Var(
    """(params) => {
        const status = (params.value || '').toLowerCase();
        const colors = {
            'success': { backgroundColor: '#dcfce7', color: '#166534' },
            'filled': { backgroundColor: '#dcfce7', color: '#166534' },
            'active': { backgroundColor: '#dcfce7', color: '#166534' },
            'failed': { backgroundColor: '#fee2e2', color: '#dc2626' },
            'error': { backgroundColor: '#fee2e2', color: '#dc2626' },
            'inactive': { backgroundColor: '#f3f4f6', color: '#6b7280' },
            'running': { backgroundColor: '#fef3c7', color: '#d97706' },
            'warning': { backgroundColor: '#fef3c7', color: '#d97706' },
        };
        return {
            ...(colors[status] || { backgroundColor: '#dbeafe', color: '#2563eb' }),
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '9px',
            fontWeight: '700',
            textTransform: 'uppercase',
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================

def _get_column_defs() -> list:
    """Return column definitions for the [table name] grid."""
    return [
        ag_grid.column_def(
            field="field_name",
            header_name="Display Name",
            filter=AGFilters.text,  # or AGFilters.number, AGFilters.date
            min_width=100,
            cell_style=_LINK_STYLE,  # optional
        ),
        # Add more columns...
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

def [table_name]_ag_grid() -> rx.Component:
    """
    [Table Name] AG-Grid component.

    [Description of what this table displays].
    """
    return ag_grid(
        id="[table_name]_grid",
        row_data=[StateClass].filtered_[data_var],
        column_defs=_get_column_defs(),
        row_id_key="id",  # or appropriate unique key
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="calc(100vh - 300px)",
        width="100%",
    )
```

---

## Workflow Per Phase

### Step 1: Analyze Legacy Views
1. Read `[component]_views.py` to understand:
   - Table function names
   - Column structure (headers, data fields)
   - Row item types (from state types)
   - Cell styling patterns (status_badge, value_cell with colors, clickable links)
   - State data source (`[State].filtered_[data]`)

### Step 2: Create AG-Grid File
1. Create `[table_name]_ag_grid.py` following the template above
2. Map legacy columns to `ag_grid.column_def()`
3. Convert styling patterns:
   - `text_cell(clickable=True)` → `_LINK_STYLE` 
   - `status_badge()` → `_STATUS_STYLE`
   - `value_cell` with colors → `_VALUE_STYLE`
   - Plain `text_cell()` → no cell_style needed

### Step 3: Update Imports
1. Update `[component]/__init__.py`:
   ```python
   from app.components.[component].[table_name]_ag_grid import [table_name]_ag_grid
   ```

2. Update `app/components/shared/contextual_workspace.py`:
   - Find old import: `from app.components.[component] import [old_function]`
   - Replace with: `from app.components.[component] import [new_ag_grid_function]`
   - Update usage in the file

3. Update page files (if any) in `app/pages/[component]/`:
   - Import new AG-Grid component
   - Replace legacy table calls

### Step 4: Test
1. Navigate to the relevant page in browser
2. Verify table renders with all columns
3. Test sorting (click headers)
4. Test filtering (column filters)
5. Confirm no console errors

### Step 5: Delete Legacy
1. Remove legacy table function from `[component]_views.py`
2. Remove unused helper functions if no longer referenced
3. If `*_views.py` is empty after migration, delete the file

---

## Phase Checklist

### Phase 6.2: Operations (2 tables)
**Source:** `app/components/operations/operations_views.py`
**State:** `app/states/operations/operations_state.py` → `OperationsState`
**Types:** `DailyProcedureItem`, `OperationProcessItem`

| Legacy Function | AG-Grid File | Cols | Special Styling |
|-----------------|--------------|------|-----------------|
| `daily_procedure_check_table()` | `daily_procedure_check_ag_grid.py` | 10 | `status_badge` |
| `operation_process_table()` | `operation_process_ag_grid.py` | 3 | status color |

Columns for `daily_procedure_check`:
- check_date, host_run_date, scheduled_time, procedure_name, status (STATUS_STYLE), error_message, frequency, scheduled_day, created_by, created_time

Columns for `operation_process`:
- process, status (STATUS_STYLE), last_run_time

---

### Phase 6.3: EMSX (2 tables)
**Source:** `app/components/emsx/emsx_views.py`
**State:** `app/states/emsx/emsx_state.py` → `EMSXState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `emsa_order_table()` | `emsa_order_ag_grid.py` | 11 |
| `emsa_route_table()` | `emsa_route_ag_grid.py` | 11 |

---

### Phase 6.4: Risk (3 tables)
**Source:** `app/components/risk/risk_views.py`
**State:** `app/states/risk/risk_state.py` → `RiskState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `delta_change_table()` | `delta_change_ag_grid.py` | 10 |
| `risk_measures_table()` | `risk_measures_ag_grid.py` | 13 |
| `risk_inputs_table()` | `risk_inputs_ag_grid.py` | 13 |

---

### Phase 6.5: Events (3 tables)
**Source:** `app/components/events/events_views.py`
**State:** `app/states/events/events_state.py` → `EventsState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `event_calendar_table()` | `event_calendar_ag_grid.py` | 4 |
| `event_stream_table()` | `event_stream_ag_grid.py` | 6 |
| `reverse_inquiry_table()` | `reverse_inquiry_ag_grid.py` | 5 |

---

### Phase 6.6: Compliance (4 tables)
**Source:** `app/components/compliance/compliance_views.py`
**State:** `app/states/compliance/compliance_state.py` → `ComplianceState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `restricted_list_table()` | `restricted_list_ag_grid.py` | 9 |
| `undertakings_table()` | `undertakings_ag_grid.py` | 7 |
| `beneficial_ownership_table()` | `beneficial_ownership_ag_grid.py` | 10 |
| `monthly_exercise_limit_table()` | `monthly_exercise_limit_ag_grid.py` | 9 |

---

### Phase 6.7: PnL (4 tables)
**Source:** `app/components/pnl/pnl_views.py`
**State:** `app/states/pnl/pnl_state.py` → `PnLState`

| Legacy Function | AG-Grid File | Cols | Special |
|-----------------|--------------|------|---------|
| `pnl_full_table()` | `pnl_full_ag_grid.py` | 6 | value colors |
| `pnl_change_table()` | `pnl_change_ag_grid.py` | 5 | value colors |
| `pnl_summary_table()` | `pnl_summary_ag_grid.py` | 6 | value colors |
| `pnl_currency_table()` | `pnl_currency_ag_grid.py` | 6 | value colors |

---

### Phase 6.8: Positions (5 tables)
**Source:** `app/components/positions/positions_views.py`
**State:** `app/states/positions/positions_state.py` → `PositionsState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `positions_table()` | `positions_ag_grid.py` | 5 |
| `stock_position_table()` | `stock_position_ag_grid.py` | 6 |
| `warrant_position_table()` | `warrant_position_ag_grid.py` | 7 |
| `bond_position_table()` | `bond_position_ag_grid.py` | 6 |
| `trade_summary_table()` | `trade_summary_ag_grid.py` | 7 |

---

### Phase 6.9: Reconciliation (5 tables)
**Source:** `app/components/reconciliation/reconciliation_views.py`
**State:** `app/states/reconciliation/reconciliation_state.py` → `ReconciliationState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `pps_recon_table()` | `pps_recon_ag_grid.py` | 5 |
| `settlement_recon_table()` | `settlement_recon_ag_grid.py` | 6 |
| `failed_trades_table()` | `failed_trades_ag_grid.py` | 8 |
| `pnl_recon_table()` | `pnl_recon_ag_grid.py` | 6 |
| `risk_input_recon_table()` | `risk_input_recon_ag_grid.py` | 5 |

---

### Phase 6.10: Instruments (5 tables)
**Source:** `app/components/instruments/instrument_views.py`
**State:** `app/states/instruments/instruments_state.py` → `InstrumentsState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `ticker_data_table()` | `ticker_data_ag_grid.py` | 6 |
| `stock_screener_table()` | `stock_screener_ag_grid.py` | 7 |
| `special_term_table()` | `special_term_ag_grid.py` | 5 |
| `instrument_data_table()` | `instrument_data_ag_grid.py` | 5 |
| `instrument_term_table()` | `instrument_term_ag_grid.py` | 5 |

---

### Phase 6.11: Portfolio Tools (9 tables) - LARGEST
**Source:** `app/components/portfolio_tools/portfolio_tools_views.py`
**State:** `app/states/portfolio_tools/portfolio_tools_state.py` → `PortfolioToolsState`

| Legacy Function | AG-Grid File | Cols |
|-----------------|--------------|------|
| `pay_to_hold_table()` | `pay_to_hold_ag_grid.py` | 7 |
| `short_ecl_table()` | `short_ecl_ag_grid.py` | 6 |
| `stock_borrow_table()` | `stock_borrow_ag_grid.py` | 5 |
| `po_settlement_table()` | `po_settlement_ag_grid.py` | 6 |
| `deal_indication_table()` | `deal_indication_ag_grid.py` | 6 |
| `reset_dates_table()` | `reset_dates_ag_grid.py` | 6 |
| `coming_resets_table()` | `coming_resets_ag_grid.py` | 5 |
| `cb_installments_table()` | `cb_installments_ag_grid.py` | 6 |
| `excess_amount_table()` | `excess_amount_ag_grid.py` | 5 |

---

## Final Cleanup

After ALL phases complete:
1. Update `app/components/shared/contextual_workspace.py` - replace all legacy imports
2. Remove all empty `*_views.py` files
3. Remove unused helpers (`header_cell`, `text_cell`, `value_cell`) from deleted files
4. Run full app smoke test: navigate all pages, verify no errors

---

## Success Criteria

- [ ] All 44 tables migrated to AG-Grid
- [ ] All pages load without errors
- [ ] Sorting works on all tables
- [ ] Filtering works on all tables
- [ ] Status badges display correctly (colored pills)
- [ ] Value colors apply correctly (green/red)
- [ ] Legacy `*_views.py` files deleted
- [ ] `__init__.py` files updated with new exports

---

## Commands

```bash
# Run dev server
uv run reflex run

# Test page loads (browser)
http://localhost:3001/pmt/operations
http://localhost:3001/pmt/emsx
http://localhost:3001/pmt/risk
http://localhost:3001/pmt/events
http://localhost:3001/pmt/compliance
http://localhost:3001/pmt/pnl
http://localhost:3001/pmt/positions
http://localhost:3001/pmt/reconciliation
http://localhost:3001/pmt/instruments
http://localhost:3001/pmt/portfolio-tools
```

**DO NOT STOP UNTIL ALL TABLES ARE MIGRATED AND TESTED.**

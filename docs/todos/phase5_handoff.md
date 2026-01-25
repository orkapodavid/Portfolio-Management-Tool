# Phase 5 Handoff: Holdings Table Migration

## Context

You are continuing work on the **Portfolio Management Tool** project. Phases 1-4 of the AG Grid table improvement plan have been completed:

- ✅ **Phase 1-3**: Built core AG Grid Enterprise wrapper (`reflex_ag_grid`) with features like cell flash, grouping, validation, WebSocket updates, etc.
- ✅ **Phase 4**: Documentation, refactoring, and demo gallery created.

## Your Task: Phase 5 - Pilot Migration

Migrate the first real production table (`holdings_table.py`) to use the new AG Grid wrapper. This validates that the wrapper works in a real-world scenario.

## Key Files to Know

| File | Purpose |
|------|---------|
| `docs/todos/table_improvement.md` | Master task list - see Phase 5 section (L694-L720) |
| `reflex_ag_grid/` | The AG Grid wrapper package |
| `reflex_ag_grid/components/ag_grid.py` | Main `ag_grid()` component |
| `reflex_ag_grid/components/ag_grid_state.py` | `AGGridStateMixin` for state helpers |
| `reflex_ag_grid/models/validation.py` | `FieldValidation` / `ValidationSchema` |
| `reflex_ag_grid/docs/` | Documentation (migration guide, performance, etc.) |
| `reflex_ag_grid/examples/demo_app/` | Demo app with 15 feature pages |
| `app/components/portfolio/holdings_table.py` | **Current table to migrate** (uses `rx.el.table`) |
| `app/states/portfolio_state.py` | State containing holdings data |

## Phase 5 Checklist

```markdown
- [ ] **5.1** Analyze current `holdings_table.py`
  - [ ] Document current columns and data types
  - [ ] Document current styling/behavior

- [ ] **5.2** Create column definition config
  - [ ] Define columns: symbol, shares, price, value, gain_loss, change
  - [ ] Set types, formatters, styles

- [ ] **5.3** Create `holdings_ag_grid.py` using wrapper
  - [ ] Use `ag_grid()` component with config
  - [ ] Wire up to `PortfolioState`

- [ ] **5.4** Add validation config for holdings
  - [ ] Price validation (min 0)
  - [ ] Shares validation (min 1)

- [ ] **5.5** Style matching
  - [ ] Match or improve current visual design
  - [ ] Dark/light theme support

- [ ] **5.6** Side-by-side comparison
  - [ ] Create toggle between old/new table
  - [ ] Verify feature parity

- [ ] **5.7** Remove old implementation (after validation)

- [ ] **5.8** Document migration learnings
```

## How to Use the Wrapper

```python
from reflex_ag_grid import ag_grid, FieldValidation, ValidationSchema

# Define columns
column_defs = [
    ag_grid.column_def(field="symbol", header_name="Symbol", sortable=True),
    ag_grid.column_def(field="shares", header_name="Shares", editable=True),
    ag_grid.column_def(field="price", header_name="Price", 
                       value_formatter=rx.Var("(p) => '$' + p.value.toFixed(2)")),
    # ... more columns
]

# Create grid
ag_grid(
    id="holdings_grid",
    row_data=PortfolioState.holdings,
    column_defs=column_defs,
    row_id_key="id",
    theme="quartz",
    enable_cell_change_flash=True,
)
```

## Running the Demo App (for reference)

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
# Visit http://localhost:3000 for Example Gallery
```

## First Steps

1. Read `app/components/portfolio/holdings_table.py` to understand current implementation
2. Read `app/states/portfolio_state.py` to understand data structure
3. Check `docs/todos/table_improvement.md` Phase 5 section
4. Start with Task 5.1: Document current columns and behavior
5. Create `holdings_ag_grid.py` following the migration guide in `reflex_ag_grid/docs/migration_guide.md`

## Additional Resources

- **Migration Guide**: `reflex_ag_grid/docs/migration_guide.md`
- **Performance Guide**: `reflex_ag_grid/docs/performance.md`
- **Demo Gallery**: Run demo app and visit http://localhost:3000
- **AG Grid Docs**: Use `mcp_ag-mcp_search_docs` tool for AG Grid API questions

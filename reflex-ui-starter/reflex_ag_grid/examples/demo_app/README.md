# AG Grid Demo App

A multi-page Reflex application demonstrating 25 AG Grid requirements with **AG Grid v35.0.1**.

## Running the Demo

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
```

Open http://localhost:3000 in your browser.

## Demo Pages (25 total)

| # | Route | Feature |
|---|-------|---------|
| 01 | `/01-context-menu` | Custom right-click menu |
| 02 | `/02-range-selection` | Cell range selection (E) |
| 03 | `/03-cell-flash` | Value change highlighting |
| 04 | `/04-jump-highlight` | Cross-component navigation |
| 05 | `/05-grouping` | Row grouping + Grand Total (E) |
| 06 | `/06-notifications` | Event-driven notifications |
| 07 | `/07-validation` | Schema-based validation |
| 08 | `/08-clipboard` | Copy/paste with Excel |
| 09 | `/09-excel-export` | Native Excel export (E) |
| 10 | `/10-websocket` | Real-time streaming |
| 11 | `/11-cell-editors` | Rich cell editors |
| 12 | `/12-edit-pause` | Pause updates + Undo/Redo |
| 13 | `/13-transaction-api` | Delta updates |
| 14 | `/14-background-tasks` | Background task integration |
| 15 | `/15-column-state` | Column state persistence |
| 16 | `/16-cell-renderers` | Custom cell formatting |
| 17 | `/17-tree-data` | Hierarchical data (E) |
| 18 | `/18-perf-test` | 10,000+ row performance |
| 19 | `/19-status-bar` | Status bar with aggregations (E) |
| 20 | `/20-overlays` | Loading/no-rows overlays |
| 21 | `/21-crud` | CRUD operations |
| 22 | `/22-advanced-filter` | Advanced Filter builder (E) |
| 23 | `/23-set-filter` | Multi-select Set Filter (E) |
| 24 | `/24-multi-filter` | Combined filter types (E) |
| 25 | `/25-row-numbers` | Automatic row numbering |

**(E)** = Enterprise feature

## Version History

- **v35.0.1** (Phase 3): Advanced Filter, Set/Multi Filter, Row Numbers, Grand Total Pinning, Undo/Redo
- **v32.3.0** (Phase 2): Tree Data, Status Bar, Overlays, CRUD, Performance Testing
- **v32.0.0** (Phase 1): Core features, 17 demo pages

## E2E Testing

```bash
# Run tests (requires demo app running)
uv run python reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000
```


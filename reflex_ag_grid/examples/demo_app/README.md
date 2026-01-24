# AG Grid Demo App

A multi-page Reflex application demonstrating all features of the AG Grid Enterprise wrapper.

## Pages

1. **Basic Grid** - Simple data display with sorting and filtering
2. **Editable Grid** - Cell editing with validation and notifications
3. **Grouped Grid** - Row grouping with aggregation functions
4. **Streaming Data** - Mock real-time updates with manual/auto toggle

## Running the Demo

```bash
cd reflex_ag_grid/examples/demo_app
reflex init  # First time only
reflex run
```

Then open http://localhost:3000 in your browser.

## Features Demonstrated

- ✅ Column definitions with Pydantic models
- ✅ Formatters (currency, percentage, number)
- ✅ Cell editors (text, number, enum dropdown)
- ✅ Cell styling and conditional formatting
- ✅ Context menu (right-click)
- ✅ Excel/CSV export
- ✅ Column state persistence
- ✅ Notifications with jump-to-row
- ✅ Row grouping and aggregation
- ✅ Mock streaming data with toggle

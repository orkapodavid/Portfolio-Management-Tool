# Status Bar Rollout Plan (Updated)

Add `last_updated` timestamp, `auto_refresh` toggle, and **simulated delta updates** to all 48 AG Grid components.

## Architecture Overview

```
┌───────────────────┐     ┌─────────────────────────────┐     ┌────────────────┐
│     Service       │────▶│   Mixin (State)             │────▶│ Grid Component │
│ (data fetching)   │     │ *_last_updated: str         │     │ (UI only)      │
│                   │     │ *_auto_refresh: bool        │     │                │
│                   │     │ simulate_*_update()         │     │ rx.moment()    │
└───────────────────┘     └─────────────────────────────┘     └────────────────┘
```

**Principle:** Grid component states are "dummy" — timestamps and auto-refresh logic live in mixins.

---

## Static vs Ticking Grids

| Grid Type | Refresh Method | Pattern |
|-----------|----------------|---------|
| **Ticking** (FX, Market Data, Historical) | Auto-refresh toggle + background task | `@rx.event(background=True)` loop with `asyncio.sleep()` |
| **Static** (Trading Calendar, Market Hours) | Force Refresh button | `show_refresh=True` + `force_refresh_*()` method |

### Force Refresh Pattern (Static Grids)

For grids with infrequently changing data, use a **Force Refresh button** instead of auto-refresh:

```python
# Mixin - force refresh method
async def force_refresh_trading_calendar(self):
    """Force refresh - reloads data from service (all cells flash)."""
    await self.load_trading_calendar()

# Grid component - toolbar config
grid_toolbar(
    show_refresh=True,
    on_refresh=MarketDataState.force_refresh_trading_calendar,
    is_loading=MarketDataState.is_loading_trading_calendar,
    last_updated=MarketDataState.trading_calendar_last_updated,
    # NO auto_refresh or on_auto_refresh_toggle
)

# Grid component - loading overlay
create_standard_grid(
    ...
    loading=MarketDataState.is_loading_trading_calendar,
    overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
)
```

**Key props:**
- `loading`: `rx.Var[bool]` — shows AG Grid's built-in loading overlay when `True`
- `overlay_loading_template`: Custom message (optional)

See [20_overlays.md](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/reflex_ag_grid/docs/20_overlays.md) for details.

---

## Key AG Grid Performance Patterns

Based on [18_performance.md](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/reflex_ag_grid/docs/18_performance.md) and [req18_perf_testing.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/reflex_ag_grid/examples/demo_app/ag_grid_demo/pages/req18_perf_testing.py):

| Pattern | Purpose | Usage |
|---------|---------|-------|
| `row_id_key="ticker"` | Delta detection — AG Grid only rerenders changed rows | Required on all grids |
| `enable_cell_change_flash=True` | Visual feedback on cell updates | Already enabled on market data grids |
| `rx.moment(interval=N)` | Timer for auto-refresh ticks | Add to grid components |
| State mutation pattern | In-place update of list items | See example below |

### Delta Update Pattern (from Performance Demo)

```python
# In mixin - simulates random price updates
def simulate_fx_update(self):
    """Called by rx.moment interval - simulates price changes."""
    if not self.fx_auto_refresh or len(self.fx_data) < 1:
        return
    
    import random
    # Update 1-5 random rows
    for _ in range(random.randint(1, 5)):
        idx = random.randint(0, len(self.fx_data) - 1)
        self.fx_data[idx]["last_price"] = round(
            self.fx_data[idx].get("last_price", 100) * random.uniform(0.99, 1.01), 4
        )
    
    from datetime import datetime
    self.fx_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

### Component Integration Pattern

```python
# In grid component — conditional rx.moment timer
rx.cond(
    MarketDataState.fx_auto_refresh,
    rx.moment(interval=2000, on_change=MarketDataState.simulate_fx_update),
    rx.fragment(),
),
create_standard_grid(
    row_data=MarketDataState.filtered_fx_data,
    row_id_key="ticker",  # CRITICAL for delta updates
    ...
)
```

---

## Implementation Pattern

### 1. Mixin Changes (per data type)

Each mixin adds:
- `*_auto_refresh: bool = True` — controls interval timer
- `simulate_*_update()` — random delta updates for demo
- Updates `*_last_updated` on each tick

**Example: FXDataMixin**

```python
class FXDataMixin(rx.State, mixin=True):
    fx_data: list[FXDataItem] = []
    fx_data_last_updated: str = "—"
    fx_auto_refresh: bool = True  # NEW
    
    async def load_fx_data(self):
        # ... existing load logic ...
        self.fx_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def toggle_fx_auto_refresh(self, value: bool):  # NEW
        self.fx_auto_refresh = value
    
    def simulate_fx_update(self):  # NEW
        """Simulated delta update for demo purposes."""
        if not self.fx_auto_refresh or len(self.fx_data) < 1:
            return
        
        import random
        for _ in range(random.randint(1, 5)):
            idx = random.randint(0, len(self.fx_data) - 1)
            self.fx_data[idx]["last_price"] = round(
                self.fx_data[idx].get("last_price", 100) * random.uniform(0.99, 1.01), 4
            )
        
        from datetime import datetime
        self.fx_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

### 2. Grid Component Changes

Remove local `auto_refresh` state — use mixin state instead:

```python
# Remove FxDataGridState.auto_refresh — now lives in mixin

def fx_data_ag_grid() -> rx.Component:
    return rx.vstack(
        # Interval timer (conditional)
        rx.cond(
            MarketDataState.fx_auto_refresh,
            rx.moment(interval=2000, on_change=MarketDataState.simulate_fx_update),
            rx.fragment(),
        ),
        grid_toolbar(
            last_updated=MarketDataState.fx_data_last_updated,
            auto_refresh=MarketDataState.fx_auto_refresh,  # FROM MIXIN
            on_auto_refresh_toggle=MarketDataState.toggle_fx_auto_refresh,  # FROM MIXIN
        ),
        create_standard_grid(
            row_data=MarketDataState.filtered_fx_data,
            row_id_key="ticker",  # CRITICAL: enables delta updates
            enable_cell_flash=True,
            ...
        ),
    )
```

---

## Rollout Phases

### Phase 1: Market Data Grids (5 grids) — *Completed*

| Grid | Mixin | Type | `last_updated` | Refresh | `simulate_*` | `row_id_key` |
|------|-------|:----:|:--------------:|:-------:|:------------:|:------------:|
| [fx_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/fx_data_ag_grid.py) | `FXDataMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [market_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/market_data_ag_grid.py) | `MarketDataMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [historical_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/historical_data_ag_grid.py) | `HistoricalDataMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [market_hours_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/market_hours_ag_grid.py) | `MarketHoursMixin` | Static | ✅ | ✅ force | — | [ ] `market` |
| [trading_calendar_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/trading_calendar_ag_grid.py) | `TradingCalendarMixin` | Static | ✅ | ✅ force | — | [ ] `trade_date` |

### Phase 2: PnL & Risk Grids (7 grids)

| Grid | Mixin | `last_updated` | `auto_refresh` | `simulate_*` | `row_id_key` |
|------|-------|:--------------:|:--------------:|:------------:|:------------:|
| pnl_change_ag_grid.py | PnLChangeMixin | [ ] | [ ] | [ ] | [ ] |
| pnl_currency_ag_grid.py | PnLCurrencyMixin | [ ] | [ ] | [ ] | [ ] |
| pnl_full_ag_grid.py | PnLFullMixin | [ ] | [ ] | [ ] | [ ] |
| pnl_summary_ag_grid.py | PnLSummaryMixin | [ ] | [ ] | [ ] | [ ] |
| delta_change_ag_grid.py | RiskMixin | [ ] | [ ] | [ ] | [ ] |
| risk_inputs_ag_grid.py | RiskMixin | [ ] | [ ] | [ ] | [ ] |
| risk_measures_ag_grid.py | RiskMixin | [ ] | [ ] | [ ] | [ ] |

### Phase 3: Positions & Reconciliation (10 grids)

*(Same pattern — see original doc)*

### Phase 4: Portfolio Tools & Static Grids (26+ grids)

*(Same pattern — see original doc)*

---

## Files to Modify

### Mixins (add `auto_refresh` + `simulate_*` methods)

| File | Key Field | ID Field |
|------|-----------|----------|
| [fx_data_mixin.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/market_data/mixins/fx_data_mixin.py) | `last_price`, `bid`, `ask` | `ticker` |
| [historical_data_mixin.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/market_data/mixins/historical_data_mixin.py) | `close_price` | `ticker` |
| [market_data_mixin.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/market_data/mixins/market_data_mixin.py) | `last_price`, `change` | `ticker` |
| [market_hours_mixin.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/market_data/mixins/market_hours_mixin.py) | — (static) | `market` |
| [trading_calendar_mixin.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/market_data/mixins/trading_calendar_mixin.py) | — (static) | `market` |

### Grid Components (add `rx.moment` + `row_id_key`)

| File | Timer Interval | Notes |
|------|----------------|-------|
| [fx_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/fx_data_ag_grid.py) | 2000ms | Remove FxDataGridState.auto_refresh |
| [historical_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/historical_data_ag_grid.py) | 5000ms | Less frequent for historical |
| [market_data_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/market_data_ag_grid.py) | 2000ms | Real-time feel |
| [market_hours_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/market_hours_ag_grid.py) | 30000ms | Static data, rare updates |
| [trading_calendar_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/market_data/trading_calendar_ag_grid.py) | 30000ms | Static data, rare updates |

---

## Verification Checklist

### Per Grid
1. [ ] Status bar shows timestamp from mixin state
2. [ ] Toggle controls auto_refresh in mixin (not local state)
3. [ ] When auto_refresh=True, `rx.moment` triggers updates
4. [ ] Cell flash highlights changed cells
5. [ ] Timestamp updates on each tick
6. [ ] No console errors
7. [ ] Grid still functions (filtering, sorting, selection)

### Manual Testing
1. Navigate to `/pmt/market-data/fx-data`
2. Verify auto-refresh toggle is ON by default
3. Observe cells flashing as prices update (~every 2s)
4. Toggle OFF — updates should stop
5. Toggle ON — updates should resume
6. Check "Last Updated" timestamp updates with each tick

---

## Services to Update (Future — Real Database)

When connecting to real database, update services to return `_refreshed_at`:

| Service | Change |
|---------|--------|
| All data services | Return `_refreshed_at` from backend |
| Mixins | Read `_refreshed_at` from service response instead of simulating |
| WebSocket | Replace `rx.moment` with WebSocket push for real-time |

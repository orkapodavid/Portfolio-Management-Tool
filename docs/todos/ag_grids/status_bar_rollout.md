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
| **Ticking** (FX, Market Data, Historical) | Auto-refresh toggle + background task | `@rx.event(background=True)` recursive step pattern |
| **Static** (Trading Calendar, Market Hours) | Force Refresh button | `show_refresh=True` + `force_refresh_*()` method |

### Force Refresh Pattern (Static Grids)

For grids with infrequently changing data, use a **Force Refresh button** instead of auto-refresh:

```python
# Mixin - force refresh method with debounce
async def force_refresh_trading_calendar(self):
    """Force refresh - reloads data from service (all cells flash).
    
    Uses yield + is_loading guard to:
    1. Prevent multiple clicks while loading
    2. Show loading overlay immediately
    """
    if self.is_loading_trading_calendar:
        return  # Debounce: ignore clicks while loading
    
    import asyncio
    self.is_loading_trading_calendar = True
    yield  # Send loading state to client immediately
    await asyncio.sleep(0.5)  # Brief delay to show loading overlay
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

> [!IMPORTANT]
> **Force refresh must include debounce protection:**
> 1. Check `if self.is_loading_*: return` at start to ignore clicks while loading
> 2. Set `is_loading = True` then `yield` to send state to client immediately
> 3. The refresh button is automatically disabled when `is_loading=True`

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

### ⚠️ Cell Flash Requirements (Critical)

> [!IMPORTANT]
> **For AG Grid cell flash to work correctly, ALL of these are required:**
>
> 1. **Immutable Updates**: Create new list + new row dict objects — do NOT mutate in-place
> 2. **Correct Field Names**: Update fields that actually exist in the data structure
> 3. **`row_id_key`**: Each grid must specify a unique identifier field (e.g., `ticker`, `currency`)
> 4. **`enable_cell_change_flash=True`**: Enabled by `create_standard_grid(enable_cell_flash=True)`

**Correct (immutable) pattern:**

```python
def simulate_update(self):
    # Create a NEW list
    new_list = list(self.data_list)
    
    for _ in range(random.randint(1, 3)):
        idx = random.randint(0, len(new_list) - 1)
        # Create a NEW row dict
        new_row = dict(new_list[idx])
        new_row["price"] = round(new_row["price"] * random.uniform(0.99, 1.01), 2)
        new_list[idx] = new_row  # Replace with new object
    
    self.data_list = new_list  # Assign new list to trigger detection
```

**Incorrect (in-place mutation) — CELL FLASH WILL NOT WORK:**

```python
# ❌ BAD - Mutates existing row objects
self.data_list[idx]["price"] = new_price
```

### ⚠️ One Mixin Per Tab (Critical)

> [!WARNING]
> **Each tab must have its own mixin with independent state.** Do NOT share `last_updated` or `auto_refresh` across tabs!
>
> If multiple tabs share the same `auto_refresh` toggle, toggling one will affect all tabs.

**Correct pattern — separate mixin per tab:**

```
app/states/risk/
├── mixins/
│   ├── delta_change_mixin.py      # delta_change_auto_refresh, delta_change_last_updated
│   ├── risk_measures_mixin.py     # risk_measures_auto_refresh, risk_measures_last_updated
│   └── risk_inputs_mixin.py       # risk_inputs_auto_refresh, risk_inputs_last_updated
└── risk_state.py                  # Composes all mixins
```

Each mixin must define:

```python
class DeltaChangeMixin(rx.State, mixin=True):
    # Tab-specific data
    delta_changes: list[DeltaChangeItem] = []
    
    # Tab-specific timestamps (NOT shared!)
    delta_change_last_updated: str = "—"
    delta_change_auto_refresh: bool = True
    
    # Tab-specific background task (while True loop pattern)
    @rx.event(background=True)
    async def start_delta_change_auto_refresh(self):
        """Background task for Delta Change auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.delta_change_auto_refresh:
                    break
                self.simulate_delta_change_update()
            await asyncio.sleep(2)

    def toggle_delta_change_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.delta_change_auto_refresh = value
        if value:
            # Use type(self) here - this is OUTSIDE background context
            return type(self).start_delta_change_auto_refresh
```

> [!CAUTION]
> **Recursive step pattern does NOT work with mixins!**
> Returning `MixinClass.method` from a background task returns a raw function, not an EventHandler.
> Use the `while True` loop pattern instead.

> [!TIP]
> **`type(self)` works in the toggle method** because it's called outside the background task context.
> The toggle method runs synchronously, so `type(self)` returns the composed State class.

**Incorrect — shared state across tabs:**

```python
# ❌ BAD - All tabs share one auto_refresh toggle
class RiskState(rx.State):
    risk_auto_refresh: bool = True  # Affects ALL tabs!
```

See [PnL mixins](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/pnl/mixins/) and [Risk mixins](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/states/risk/mixins/) for reference implementations.



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

### Phase 2: PnL & Risk Grids (7 grids) — *Completed*

| Grid | Mixin | Type | `last_updated` | Refresh | `simulate_*` | `row_id_key` |
|------|-------|:----:|:--------------:|:-------:|:------------:|:------------:|
| [pnl_change_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/pnl/pnl_change_ag_grid.py) | `PnLChangeMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [pnl_currency_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/pnl/pnl_currency_ag_grid.py) | `PnLCurrencyMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `currency` |
| [pnl_full_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/pnl/pnl_full_ag_grid.py) | `PnLFullMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [pnl_summary_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/pnl/pnl_summary_ag_grid.py) | `PnLSummaryMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `underlying` |
| [delta_change_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/risk/delta_change_ag_grid.py) | `RiskState` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |
| [risk_inputs_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/risk/risk_inputs_ag_grid.py) | `RiskState` | Ticking | ✅ | ✅ auto | ✅ | ✅ `seed` |
| [risk_measures_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/risk/risk_measures_ag_grid.py) | `RiskState` | Ticking | ✅ | ✅ auto | ✅ | ✅ `ticker` |

### Phase 3: Positions & Reconciliation (10 grids) — *Completed*

**Positions Grids (5):**

| Grid | Mixin | Type | `last_updated` | Refresh | `simulate_*` | `row_id_key` |
|------|-------|:----:|:--------------:|:-------:|:------------:|:------------:|
| [positions_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/positions/positions_ag_grid.py) | `PositionsMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `id` |
| [stock_position_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/positions/stock_position_ag_grid.py) | `StockPositionMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `id` |
| [warrant_position_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/positions/warrant_position_ag_grid.py) | `WarrantPositionMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `id` |
| [bond_position_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/positions/bond_position_ag_grid.py) | `BondPositionsMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `id` |
| [trade_summary_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/positions/trade_summary_ag_grid.py) | `TradeSummaryMixin` | Ticking | ✅ | ✅ auto | ✅ | ✅ `id` |

**Reconciliation Grids (5):**

| Grid | Mixin | Type | `last_updated` | Refresh | Loading Overlay | `row_id_key` |
|------|-------|:----:|:--------------:|:-------:|:---------------:|:------------:|
| [pps_recon_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/reconciliation/pps_recon_ag_grid.py) | `PPSReconMixin` | Static | ✅ | ✅ force | ✅ | ✅ `id` |
| [settlement_recon_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/reconciliation/settlement_recon_ag_grid.py) | `SettlementReconMixin` | Static | ✅ | ✅ force | ✅ | ✅ `id` |
| [failed_trades_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/reconciliation/failed_trades_ag_grid.py) | `FailedTradesMixin` | Static | ✅ | ✅ force | ✅ | ✅ `id` |
| [pnl_recon_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/reconciliation/pnl_recon_ag_grid.py) | `PnLReconMixin` | Static | ✅ | ✅ force | ✅ | ✅ `id` |
| [risk_input_recon_ag_grid.py](file:///home/kuro/Desktop/projects/Portfolio-Management-Tool/app/components/reconciliation/risk_input_recon_ag_grid.py) | `RiskInputReconMixin` | Static | ✅ | ✅ force | ✅ | ✅ `id` |

### Phase 4: Portfolio Tools & Static Grids (25 grids)

> [!IMPORTANT]
> **All Phase 4 grids already use the `create_standard_grid()` factory pattern** with Tier 1 enhancements (status bar, floating filters, quick filter, export). The remaining work is to add:
> 1. `last_updated` timestamp in toolbar
> 2. Force Refresh button (for Static grids)
> 3. `row_id_key` for delta detection
> 4. Mixin updates for each state

---

#### 4.1 Compliance Grids (4) — Static ✅ COMPLETE

All grids use **Force Refresh** pattern (infrequently changing compliance data).

| Grid | File | Mixin | `last_updated` | Refresh | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|
| Beneficial Ownership | [beneficial_ownership_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/compliance/beneficial_ownership_ag_grid.py) | `ComplianceState` | ✅ | ✅ force | ✅ `ticker` |
| Monthly Exercise Limit | [monthly_exercise_limit_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/compliance/monthly_exercise_limit_ag_grid.py) | `ComplianceState` | ✅ | ✅ force | ✅ `underlying` |
| Restricted List | [restricted_list_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/compliance/restricted_list_ag_grid.py) | `ComplianceState` | ✅ | ✅ force | ✅ `ticker` |
| Undertakings | [undertakings_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/compliance/undertakings_ag_grid.py) | `ComplianceState` | ✅ | ✅ force | ✅ `deal_num` |

**Mixin additions needed in `ComplianceState`:**
```python
# app/states/compliance/compliance_state.py
beneficial_ownership_last_updated: str = "—"
is_loading_beneficial_ownership: bool = False

monthly_exercise_limit_last_updated: str = "—"
is_loading_monthly_exercise_limit: bool = False

restricted_list_last_updated: str = "—"
is_loading_restricted_list: bool = False

undertakings_last_updated: str = "—"
is_loading_undertakings: bool = False

async def force_refresh_beneficial_ownership(self):
    if self.is_loading_beneficial_ownership:
        return
    self.is_loading_beneficial_ownership = True
    yield
    await asyncio.sleep(0.5)
    await self.load_beneficial_ownership()
    self.beneficial_ownership_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.is_loading_beneficial_ownership = False
```

---

#### 4.2 EMSX Grids (2) — Ticking ✅ COMPLETE

Order and route data is real-time → use **Auto-Refresh** pattern.

| Grid | File | Mixin | `last_updated` | Refresh | `simulate_*` | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|:------------:|
| EMSA Order | [emsa_order_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/emsx/emsa_order_ag_grid.py) | `EMSXState` | [x] | [x] auto | [x] | [x] `id` |
| EMSA Route | [emsa_route_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/emsx/emsa_route_ag_grid.py) | `EMSXState` | [x] | [x] auto | [x] | [x] `id` |


**Mixin additions needed in `EMSXState`:**
```python
# app/states/emsx/emsx_state.py
emsa_order_last_updated: str = "—"
emsa_order_auto_refresh: bool = True

emsa_route_last_updated: str = "—"
emsa_route_auto_refresh: bool = True

def toggle_emsa_order_auto_refresh(self, value: bool):
    self.emsa_order_auto_refresh = value
    if value:
        return type(self).start_emsa_order_auto_refresh

@rx.event(background=True)
async def start_emsa_order_auto_refresh(self):
    while True:
        async with self:
            if not self.emsa_order_auto_refresh:
                break
            self.simulate_emsa_order_update()
        await asyncio.sleep(2)

def simulate_emsa_order_update(self):
    # Simulate order fill updates
    ...
```

---

#### 4.3 Events Grids (3) — Static

Event calendar and stream data is reference data → use **Force Refresh** pattern.

| Grid | File | Mixin | `last_updated` | Refresh | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|
| Event Calendar | [event_calendar_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/events/event_calendar_ag_grid.py) | `EventsState` | [ ] | [ ] force | [ ] `id` |
| Event Stream | [event_stream_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/events/event_stream_ag_grid.py) | `EventsState` | [ ] | [ ] force | [ ] `id` |
| Reverse Inquiry | [reverse_inquiry_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/events/reverse_inquiry_ag_grid.py) | `EventsState` | [ ] | [ ] force | [ ] `id` |

**Mixin additions needed in `EventsState`:**
```python
# app/states/events/events_state.py
event_calendar_last_updated: str = "—"
is_loading_event_calendar: bool = False

event_stream_last_updated: str = "—"
is_loading_event_stream: bool = False

reverse_inquiry_last_updated: str = "—"
is_loading_reverse_inquiry: bool = False
```

---

#### 4.4 Instruments Grids (5) — Static

Instrument reference data → use **Force Refresh** pattern.

| Grid | File | Mixin | `last_updated` | Refresh | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|
| Instrument Data | [instrument_data_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/instruments/instrument_data_ag_grid.py) | `InstrumentState` | [ ] | [ ] force | [ ] `deal_num` |
| Instrument Term | [instrument_term_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/instruments/instrument_term_ag_grid.py) | `InstrumentState` | [ ] | [ ] force | [ ] `id` |
| Special Term | [special_term_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/instruments/special_term_ag_grid.py) | `InstrumentState` | [ ] | [ ] force | [ ] `id` |
| Stock Screener | [stock_screener_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/instruments/stock_screener_ag_grid.py) | `InstrumentState` | [ ] | [ ] force | [ ] `ticker` |
| Ticker Data | [ticker_data_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/instruments/ticker_data_ag_grid.py) | `InstrumentState` | [ ] | [ ] force | [ ] `ticker` |

---

#### 4.5 Operations Grids (2) — Static

Operations tracking data → use **Force Refresh** pattern.

| Grid | File | Mixin | `last_updated` | Refresh | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|
| Daily Procedure Check | [daily_procedure_check_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/operations/daily_procedure_check_ag_grid.py) | `OperationsState` | [ ] | [ ] force | [ ] `id` |
| Operation Process | [operation_process_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/operations/operation_process_ag_grid.py) | `OperationsState` | [ ] | [ ] force | [ ] `id` |

---

#### 4.6 Portfolio Tools Grids (9) — Static

Portfolio reference and configuration data → use **Force Refresh** pattern.

| Grid | File | Mixin | `last_updated` | Refresh | `row_id_key` |
|------|------|-------|:--------------:|:-------:|:------------:|
| CB Installments | [cb_installments_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/cb_installments_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Coming Resets | [coming_resets_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/coming_resets_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Deal Indication | [deal_indication_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/deal_indication_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Excess Amount | [excess_amount_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/excess_amount_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Pay to Hold | [pay_to_hold_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/pay_to_hold_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| PO Settlement | [po_settlement_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/po_settlement_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Reset Dates | [reset_dates_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/reset_dates_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Short ECL | [short_ecl_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/short_ecl_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `id` |
| Stock Borrow | [stock_borrow_ag_grid.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/portfolio_tools/stock_borrow_ag_grid.py) | `PortfolioToolsState` | [ ] | [ ] force | [ ] `ticker` |

---

## Phase 4 Implementation Checklist

### Per Grid (25 total):

1. **Grid Component (`*_ag_grid.py`)**:
   - [ ] Add `row_id_key="<unique_field>"` to `create_standard_grid()`
   - [ ] Add `loading=<State>.is_loading_*` to `create_standard_grid()` for loading overlay
   - [ ] Add `last_updated=<State>.*_last_updated` to `grid_toolbar()`
   - [ ] Add `show_refresh=True` and `on_refresh=<State>.force_refresh_*()` to `grid_toolbar()`
   - [ ] Add `is_loading=<State>.is_loading_*` to `grid_toolbar()`

> [!IMPORTANT]
> **`row_id_key` MUST be a truly unique field per row** (e.g., `"id"`, `"deal_num"` if unique).
> Using non-unique fields like `"ticker"` or `"underlying"` causes AG Grid to **deduplicate rows**,
> resulting in only the last row with each unique value being displayed.
> **Symptom**: Grid shows fewer rows than expected (e.g., 8 rows → 1 row after refresh).

2. **State/Mixin Architecture (`*_mixin.py` + `*_state.py`)**:
   - [ ] Each grid has its own mixin file (e.g., `emsa_order_mixin.py`)
   - [ ] Mixin inherits from `rx.State, mixin=True`
   - [ ] Main state inherits from all relevant mixins (e.g., `EMSXState(EMSAOrderMixin, EMSARouteMixin, rx.State)`)
   - [ ] Add `*_last_updated: str = "—"` state variable in mixin
   - [ ] Add `is_loading_*: bool = False` state variable in mixin
   - [ ] Add `async def force_refresh_*()` method with debounce guard in mixin
   - [ ] Add `async def load_*()` method to set `*_last_updated` timestamp in mixin
   - [ ] Grid uses raw data (e.g., `emsa_orders`) with `quick_filter_text` for filtering

> [!NOTE]
> **AG Grid handles filtering client-side** via `quick_filter_text` prop.
> **Do NOT create `filtered_*` computed vars** in mixins referencing `current_search_query`.
> Instead, pass raw data (e.g., `row_data=EMSXState.emsa_orders`) and let AG Grid filter.

3. **Terminal Verification (MANDATORY after each grid)**:
   - [ ] Check terminal for compilation errors after code changes
   - [ ] Watch for `ValueError`, `TypeError`, or `AttributeError` on page navigation
   - [ ] Confirm no "returning empty" log messages (indicates missing mock data)
   - [ ] Verify no `AttributeError: 'NoneType'` for missing state variables

4. **Browser Verification (MANDATORY after each grid)**:
   - [ ] Navigate to the grid page in browser
   - [ ] Verify grid shows data rows (check "Total Rows: N" in status bar > 0)
   - [ ] **Verify row count matches mock data** (e.g., if mock returns 8 items, status bar should show "Total Rows: 8")
   - [ ] Verify "Last Updated" timestamp is displayed in toolbar
   - [ ] Click Refresh button — verify **loading overlay** appears on grid
   - [ ] After refresh completes — verify timestamp updates and **row count unchanged**
   - [ ] Verify no console errors (F12 → Console tab)
   - [ ] Test Quick Filter — type text, verify rows filter
   - [ ] Test Excel export button — verify file downloads
   - [ ] Test Save/Restore/Reset layout buttons
   - [ ] For Ticking grids: verify Auto-Refresh toggle ON/OFF works

> [!CAUTION]
> **DO NOT proceed to next grid until all verification steps pass!**
> Each grid must be verified working before moving on.

### Summary by Category:

| Category | Grids | Type | Pattern |
|----------|-------|------|---------|
| Compliance | 4 | Static | Force Refresh |
| EMSX | 2 | Ticking | Auto-Refresh + simulate |
| Events | 3 | Static | Force Refresh |
| Instruments | 5 | Static | Force Refresh |
| Operations | 2 | Static | Force Refresh |
| Portfolio Tools | 9 | Static | Force Refresh |
| **Total** | **25** | | |

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

### Terminal Verification (Critical)

> [!IMPORTANT]
> **Always check the terminal output when testing AG Grids.** Watch for:
> - `ValueError` or `TypeError` in simulation methods
> - `AttributeError` for missing state methods
> - Log messages like `"returning empty"` indicating missing mock data

**Example terminal check:**
```bash
# Watch for errors after navigating to a grid page
2026-02-05 19:01:09 - pmt_core.repositories.positions.position_repository - INFO - Returning mock positions  # ✅ Good
get_trade_summary not implemented in core yet, returning empty.  # ❌ Missing mock data!
ValueError: invalid literal for int() with base 10: 'WD004'  # ❌ Data parsing error!
```

### Browser Data Verification (Critical)

> [!WARNING]
> **The grid MUST show data rows in the browser.** An empty grid indicates:
> 1. Service/repository returns empty list
> 2. Initial data load not called in background task
> 3. Data filtering returns no matches

**Verify in browser:**
- Check "Total Rows: N" at bottom of grid — should be > 0
- Verify row data appears (not "No rows to display")
- Confirm "Last Updated" timestamp updates every ~2 seconds

### Mock Data Implementation Checklist

If a grid shows no data, implement mock data in the following order:

1. **Repository Layer** (`pmt_core_pkg/pmt_core/repositories/`):
   ```python
   async def get_positions(self) -> List[PositionRecord]:
       if self.mock_mode:
           logger.info("Returning mock positions")
           return [
               PositionRecord(id=i, ticker=f"TKR{i}", ...)
               for i in range(10)
           ]
       return []
   ```

2. **Service Layer** (`app/services/`):
   ```python
   async def get_trade_summary(self) -> list[dict]:
       # Add mock data directly if core not implemented
       return [
           {"id": i, "ticker": f"TRD{i}", ...}
           for i in range(8)
       ]
   ```

3. **Mixin Layer** (add initial data load to background task):
   ```python
   @rx.event(background=True)
   async def start_*_auto_refresh(self):
       # Load initial data if empty
       async with self:
           if len(self.data_list) == 0:
               await self.load_*_data()
       
       while True:
           async with self:
               if not self.*_auto_refresh:
                   break
               self.simulate_*_update()
           await asyncio.sleep(2)
   ```

### Common Error Patterns & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: invalid literal for int()` with `'WD004'` | Alphanumeric ID parsing | Use regex: `re.match(r"([A-Za-z]*)(\d+)", val)` |
| `ValueError` with `'$300,000.00'` | Formatted currency string | Use `parse_currency()` helper to strip symbols |
| `AttributeError: 'AgGridNamespace' has no attribute 'value_formatter'` | Non-existent AG Grid API | Remove `value_formatter`, use `AGFilters.number` |
| `"returning empty"` log message | Service not implemented | Add mock data to service or repository |
| Grid shows "No rows to display" | Initial load not called | Add `if len(self.data) == 0: await self.load_*()` |

**Alphanumeric ID parsing helper:**
```python
def parse_alphanumeric_id(val: str) -> tuple[str, int]:
    """Parse 'WD004' into ('WD', 4)."""
    match = re.match(r"([A-Za-z]*)(\d+)", str(val))
    if match:
        return match.group(1), int(match.group(2))
    return "", 0
```

**Currency parsing helper:**
```python
def parse_currency(val) -> float:
    """Parse '$300,000.00' to 300000.00."""
    if isinstance(val, (int, float)):
        return float(val)
    cleaned = re.sub(r"[^\d.\-]", "", str(val))
    return float(cleaned) if cleaned else 0.0
```

### Manual Testing Procedure

1. **Start the app:** `uv run reflex run`
2. **Monitor terminal** for compilation and runtime errors
3. **Navigate to grid page** (e.g., `/pmt/market-data/fx-data`)
4. **Verify in terminal:**
   - No `ValueError`, `TypeError`, or `AttributeError`
   - Log shows data being returned (e.g., `Returning mock positions`)
5. **Verify in browser:**
   - Grid shows data rows (check "Total Rows: N")
   - Auto-refresh toggle is ON by default
   - Cells flash as values update (~every 2s)
   - "Last Updated" timestamp updates with each tick
6. **Test toggle:**
   - Toggle OFF — updates should stop immediately
   - Toggle ON — updates should resume
7. **Test grid features:**
   - Filtering still works
   - Sorting still works
   - Selection still works

---

## Services to Update (Future — Real Database)

When connecting to real database, update services to return `_refreshed_at`:

| Service | Change |
|---------|--------|
| All data services | Return `_refreshed_at` from backend |
| Mixins | Read `_refreshed_at` from service response instead of simulating |
| WebSocket | Replace `rx.moment` with WebSocket push for real-time |

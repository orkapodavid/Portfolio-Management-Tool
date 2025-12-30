# Table Column Review and Remediation Plan

## Context
Systematic review of all table-like UIs in the Portfolio Management Dashboard against industry-standard financial specifications.

---

## Phase 1: Discovery & Mapping - Identify All Tables ✅
- [x] Scan codebase for all table components
- [x] Map tables to modules and tabs
- [x] Document current column structures

**Current Table Mapping:**
| Module | Tab | Implementation File |
|--------|-----|---------------------|
| PnL | PnL Change | `components/pnl_views.py` - `pnl_change_table()` |
| PnL | PnL Full | `components/pnl_views.py` - `pnl_full_table()` |
| PnL | PnL Summary | `components/pnl_views.py` - `pnl_summary_table()` |
| PnL | PnL Currency | `components/pnl_views.py` - `pnl_currency_table()` |
| Positions | Positions | `components/positions_views.py` - `positions_table()` |
| Positions | Stock Position | `components/positions_views.py` - `stock_position_table()` |
| Positions | Warrant Position | `components/positions_views.py` - `warrant_position_table()` |
| Positions | Bond Position | `components/positions_views.py` - `bond_position_table()` |
| Positions | Trade Summary | `components/positions_views.py` - `trade_summary_table()` |
| Market Data | Market Data | `components/contextual_workspace.py` - `mock_data_table()` |

---

## Phase 2: PnL Module Tables - Column Alignment
- [ ] PnL Change: Add missing columns (Underlying ID, Strategy), fix column ordering
- [ ] PnL Full: Extend with Unrealized/Realized PnL breakdown, Cost Basis
- [ ] PnL Summary: Add Price Source, Dividend Yield columns
- [ ] PnL Currency: Add CCY Pair, Forward Points columns

---

## Phase 3: Positions Module Tables - Column Alignment
- [ ] Positions: Add Account, Custodian, Settlement Date columns
- [ ] Stock Position: Add Exchange, ISIN, Dividend columns
- [ ] Warrant Position: Add Vega, Rho, Implied Vol columns
- [ ] Bond Position: Add Accrued Interest, Convexity, Clean/Dirty Price columns
- [ ] Trade Summary: Add Counterparty, Commission, Fees columns

---

## Phase 4: Remaining Modules - Stub Tables Implementation
- [ ] Risk module tables (5 tabs)
- [ ] Recon module tables (7 tabs)
- [ ] Compliance module tables (4 tabs)
- [ ] Portfolio Tools module tables (10 tabs)
- [ ] Instruments module tables (5 tabs)
- [ ] Events module tables (3 tabs)
- [ ] Operations module tables (2 tabs)
- [ ] Orders module tables (1 tab)

---

## Notes
- Requirements document not found in codebase
- Using industry-standard financial table conventions
- Maintaining existing styling patterns (green positive, red negative)
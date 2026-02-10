# PMT Web Application Pages Reference

Complete list of all pages and tabs in the Portfolio Management Tool web application.

> **Base URL**: `http://localhost:3001/pmt`

## Module Pages Overview

| Module | Route | Default Tab |
|--------|-------|-------------|
| Market Data | `/market-data` | Market Data |
| Positions | `/positions` | Positions |
| PnL | `/pnl` | PnL Change |
| Risk | `/risk` | Delta Change |
| Recon | `/recon` | PPS Recon |
| Compliance | `/compliance` | Restricted List |
| Portfolio Tools | `/portfolio-tools` | Pay-To-Hold |
| Instruments | `/instruments` | Ticker Data |
| Events | `/events` | Event Calendar |
| Operations | `/operations` | Daily Procedure Check |
| Orders | `/orders` | EMSX Order |

---

## Detailed Page Routes

### Market Data Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Market Data | `/market-data/market-data` | `market_data_page` | `MarketDataState.load_market_data` |
| FX Data | `/market-data/fx-data` | `fx_data_page` | `MarketDataState.load_fx_data` |
| Reference Data | `/market-data/reference-data` | `ticker_data_page` | `MarketDataState.load_ticker_data` |
| Historical Data | `/market-data/historical-data` | `historical_data_page` | `MarketDataState.load_historical_data` |
| Trading Calendar | `/market-data/trading-calendar` | `trading_calendar_page` | `MarketDataState.load_trading_calendar` |
| Market Hours | `/market-data/market-hours` | `market_hours_page` | `MarketDataState.load_market_hours` |

### Positions Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Positions | `/positions/positions` | `positions_page` | `PositionsState.load_positions_data` |
| Stock Position | `/positions/stock-position` | `stock_position_page` | `PositionsState.load_stock_positions_data` |
| Warrant Position | `/positions/warrant-position` | `warrant_position_page` | `PositionsState.load_warrant_positions_data` |
| Bond Positions | `/positions/bond-positions` | `bond_positions_page` | `PositionsState.load_bond_positions_data` |
| Trade Summary | `/positions/trade-summary` | `trade_summary_page` | `PositionsState.load_trade_summary_data` |

### PnL Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| PnL Change | `/pnl/pnl-change` | `pnl_change_page` | `PnLState.load_pnl_change_data` |
| PnL Summary | `/pnl/pnl-summary` | `pnl_summary_page` | `PnLState.load_pnl_summary_data` |
| PnL Currency | `/pnl/pnl-currency` | `pnl_currency_page` | `PnLState.load_pnl_currency_data` |
| PnL Full | `/pnl/pnl-full` | `pnl_full_page` | `PnLState.load_pnl_full_data` |

### Risk Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Delta Change | `/risk/delta-change` | `delta_change_page` | `RiskState.load_risk_data` |
| Risk Measures | `/risk/risk-measures` | `risk_measures_page` | `RiskState.load_risk_data` |
| Risk Inputs | `/risk/risk-inputs` | `risk_inputs_page` | `RiskState.load_risk_data` |
| Pricer Warrant | `/risk/pricer-warrant` | `pricer_warrant_page` | - |
| Pricer Bond | `/risk/pricer-bond` | `pricer_bond_page` | - |

### Recon Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| PPS Recon | `/recon/pps-recon` | `pps_recon_page` | `ReconciliationState.load_reconciliation_data` |
| Settlement Recon | `/recon/settlement-recon` | `settlement_recon_page` | `ReconciliationState.load_reconciliation_data` |
| Failed Trades | `/recon/failed-trades` | `failed_trades_page` | `ReconciliationState.load_reconciliation_data` |
| PnL Recon | `/recon/pnl-recon` | `pnl_recon_page` | `ReconciliationState.load_reconciliation_data` |
| Risk Input Recon | `/recon/risk-input-recon` | `risk_input_recon_page` | `ReconciliationState.load_reconciliation_data` |

### Compliance Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Restricted List | `/compliance/restricted-list` | `restricted_list_page` | `ComplianceState.load_compliance_data` |
| Undertakings | `/compliance/undertakings` | `undertakings_page` | `ComplianceState.load_compliance_data` |
| Beneficial Ownership | `/compliance/beneficial-ownership` | `beneficial_ownership_page` | `ComplianceState.load_compliance_data` |
| Monthly Exercise Limit | `/compliance/monthly-exercise-limit` | `monthly_exercise_limit_page` | `ComplianceState.load_compliance_data` |

### Portfolio Tools Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Pay-To-Hold | `/portfolio-tools/pay-to-hold` | `pay_to_hold_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Short ECL | `/portfolio-tools/short-ecl` | `short_ecl_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Stock Borrow | `/portfolio-tools/stock-borrow` | `stock_borrow_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| PO Settlement | `/portfolio-tools/po-settlement` | `po_settlement_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Deal Indication | `/portfolio-tools/deal-indication` | `deal_indication_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Reset Dates | `/portfolio-tools/reset-dates` | `reset_dates_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Coming Resets | `/portfolio-tools/coming-resets` | `coming_resets_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| CB Installments | `/portfolio-tools/cb-installments` | `cb_installments_page` | `PortfolioToolsState.load_portfolio_tools_data` |
| Excess Amount | `/portfolio-tools/excess-amount` | `excess_amount_page` | `PortfolioToolsState.load_portfolio_tools_data` |

### Instruments Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Ticker Data | `/instruments/ticker-data` | `inst_ticker_data_page` | `InstrumentState.load_instruments_data` |
| Stock Screener | `/instruments/stock-screener` | `stock_screener_page` | `InstrumentState.load_instruments_data` |
| Special Term | `/instruments/special-term` | `special_term_page` | `InstrumentState.load_instruments_data` |
| Instrument Data | `/instruments/instrument-data` | `instrument_data_page` | `InstrumentState.load_instruments_data` |
| Instrument Term | `/instruments/instrument-term` | `instrument_term_page` | `InstrumentState.load_instruments_data` |

### Events Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Event Calendar | `/events/event-calendar` | `event_calendar_page` | `EventsState.load_events_data` |
| Event Stream | `/events/event-stream` | `event_stream_page` | `EventsState.load_events_data` |
| Reverse Inquiry | `/events/reverse-inquiry` | `reverse_inquiry_page` | `EventsState.load_events_data` |

### Operations Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| Daily Procedure Check | `/operations/daily-procedure-check` | `daily_procedure_check_page` | `OperationsState.load_operations_data` |
| Operation Process | `/operations/operation-process` | `operation_process_page` | `OperationsState.load_operations_data` |

### Orders Module
| Tab | Route | Page Function | State |
|-----|-------|---------------|-------|
| EMSX Order | `/orders/emsx-order` | `emsx_order_page` | `EMSXState.load_emsx_data` |
| EMSX Route | `/orders/emsx-route` | `emsx_route_page` | `EMSXState.load_emsx_data` |

---

## Other Pages

| Route | Page Function | Description |
|-------|---------------|-------------|
| `/` | `index` | Main dashboard |
| `/portfolios` | `portfolio_page` | Portfolio overview |
| `/watchlist` | `watchlist_page` | Watchlist |
| `/research` | `research_page` | Research section |
| `/reports` | `reports_page` | Reports |
| `/goals` | `goals_page` | Investment goals |
| `/profile` | `profile_page` | User profile |
| `/notifications` | `notifications_page` | Notifications |
| `/settings` | `settings_page` | Settings |

---

## File Structure

```
app/pages/
├── market_data/          # Market data pages
├── positions/            # Position pages
├── pnl/                  # P&L pages
├── risk/                 # Risk analysis pages
├── reconciliation/       # Reconciliation pages
├── compliance/           # Compliance pages
├── portfolio_tools/      # Portfolio tool pages
├── instruments/          # Instrument pages
├── events/               # Event pages
├── operations/           # Operations pages
├── orders/               # Order pages
├── portfolio/            # Portfolio/watchlist/goals pages
├── research/             # Research pages
├── reports/              # Report pages
├── user/                 # User profile/settings pages
└── notifications/        # Notification pages
```

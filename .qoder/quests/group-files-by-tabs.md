# File Organization Design: Group Files by Tabs

## Objective

Reorganize the application's component, state, and page files by introducing an additional subfolder layer that groups files belonging to the same functional page together. Tabs that appear on the same page should be placed within a common folder.

## Current Structure Analysis

The application currently uses a flat directory structure within three main folders:

| Folder | Current Count | Organization Pattern |
|--------|---------------|---------------------|
| app/components | 28 files | Flat structure with view files named by domain |
| app/states | 12 files | Flat structure with state files named by domain |
| app/pages | 8 files | Flat structure with page files |

The main navigation system organizes content into 10 core functional modules, each containing multiple tabs as defined in the UI requirements document.

## Mapping: Pages to Tabs to Files

Based on the requirements document and code analysis, the following mapping organizes files into logical page groupings:

### 3.1 Positions & Trade Summary View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Positions | positions_views.py (positions_table) | portfolio_dashboard_state.py |
| Stock Position | positions_views.py (stock_position_table) | portfolio_dashboard_state.py |
| Warrant Position | positions_views.py (warrant_position_table) | portfolio_dashboard_state.py |
| Bond Positions | positions_views.py (bond_position_table) | portfolio_dashboard_state.py |
| Trade Summary (War/Bond) | positions_views.py (trade_summary_table) | portfolio_dashboard_state.py |

### 3.2 Compliance & Holdings View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Restricted List | compliance_views.py (restricted_list_table) | portfolio_dashboard_state.py |
| Undertakings | compliance_views.py (undertakings_table) | portfolio_dashboard_state.py |
| Beneficial Ownership | compliance_views.py (beneficial_ownership_table) | portfolio_dashboard_state.py |
| Monthly Exercise Limit | compliance_views.py (monthly_exercise_limit_table) | portfolio_dashboard_state.py |

### 3.3 Pay-To-Hold & Settlement View (Portfolio Tools)

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Pay-To-Hold | portfolio_tools_views.py (pay_to_hold_table) | portfolio_dashboard_state.py |
| Short ECL | portfolio_tools_views.py (short_ecl_table) | portfolio_dashboard_state.py |
| Stock Borrow | portfolio_tools_views.py (stock_borrow_table) | portfolio_dashboard_state.py |
| PO Settlement | portfolio_tools_views.py (po_settlement_table) | portfolio_dashboard_state.py |
| Deal Indication | portfolio_tools_views.py (deal_indication_table) | portfolio_dashboard_state.py |
| Reset Dates | portfolio_tools_views.py (reset_dates_table) | portfolio_dashboard_state.py |
| Coming Resets | portfolio_tools_views.py (coming_resets_table) | portfolio_dashboard_state.py |
| CB Installments | portfolio_tools_views.py (cb_installments_table) | portfolio_dashboard_state.py |
| Excess Amount | portfolio_tools_views.py (excess_amount_table) | portfolio_dashboard_state.py |

### 3.4 PnL View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| PnL Change | pnl_views.py (pnl_change_table) | portfolio_dashboard_state.py |
| PnL Summary | pnl_views.py (pnl_summary_table) | portfolio_dashboard_state.py |
| PnL Currency | pnl_views.py (pnl_currency_table) | portfolio_dashboard_state.py |

### 3.5 Reconciliation View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| PPS Recon | reconciliation_views.py (pps_recon_table) | portfolio_dashboard_state.py |
| Settlement Recon | reconciliation_views.py (settlement_recon_table) | portfolio_dashboard_state.py |
| Failed Trades | reconciliation_views.py (failed_trades_table) | portfolio_dashboard_state.py |
| PnL Recon | reconciliation_views.py (pnl_recon_table) | portfolio_dashboard_state.py |
| Risk Input Recon | reconciliation_views.py (risk_input_recon_table) | portfolio_dashboard_state.py |

### 3.6 Operational Processes View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Daily Procedure Check | operations_views.py (daily_procedure_check_table) | portfolio_dashboard_state.py |
| Operation Process | operations_views.py (operation_process_table) | portfolio_dashboard_state.py |

### 3.7 Market Data & Events View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Market Data | market_data_views.py (market_data_table) | portfolio_dashboard_state.py |
| FX Data | market_data_views.py (fx_data_table) | portfolio_dashboard_state.py |
| Historical Data | market_data_views.py (historical_data_table) | portfolio_dashboard_state.py |
| Trading Calendar | market_data_views.py (trading_calendar_table) | portfolio_dashboard_state.py |
| Market Hours | market_data_views.py (market_hours_table) | portfolio_dashboard_state.py |
| Event Calendar | market_data_views.py (event_calendar_table) | portfolio_dashboard_state.py |
| Event Stream | market_data_views.py (event_stream_view) | portfolio_dashboard_state.py |
| Reverse Inquiry | market_data_views.py (reverse_inquiry_table) | portfolio_dashboard_state.py |

### 3.8 Ticker & Instrument Analysis View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Ticker Data | instrument_views.py (ticker_data_table) | portfolio_dashboard_state.py |
| Stock Screener | instrument_views.py (stock_screener_view) | portfolio_dashboard_state.py |
| Special Term | instrument_views.py (special_term_table) | portfolio_dashboard_state.py |
| Instrument Data | instrument_views.py (instrument_data_table) | portfolio_dashboard_state.py |
| Instrument Term | instrument_views.py (instrument_term_table) | portfolio_dashboard_state.py |

### 3.9 Risk & Pricing View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| Delta Change | risk_views.py (delta_change_table) | portfolio_dashboard_state.py |
| Risk Measures | risk_views.py (risk_measures_table) | portfolio_dashboard_state.py |
| Risk Inputs | risk_views.py (risk_inputs_table) | portfolio_dashboard_state.py |
| Pricer Warrant | risk_views.py (pricer_warrant_view) | portfolio_dashboard_state.py |
| Price Bond | risk_views.py (pricer_bond_view) | portfolio_dashboard_state.py |

### 3.10 EMSA Order Management View

| Tab Name | Component File | State File |
|----------|---------------|------------|
| EMSA Order | emsa_views.py (emsa_order_table) | portfolio_dashboard_state.py |
| EMSA Route | emsa_views.py (emsa_route_table) | portfolio_dashboard_state.py |

## Proposed Directory Structure

The new organization will introduce domain-specific subfolders within each main directory:

```
app/
├── components/
│   ├── positions/
│   │   └── positions_views.py
│   ├── compliance/
│   │   └── compliance_views.py
│   ├── portfolio_tools/
│   │   └── portfolio_tools_views.py
│   ├── pnl/
│   │   └── pnl_views.py
│   ├── reconciliation/
│   │   └── reconciliation_views.py
│   ├── operations/
│   │   └── operations_views.py
│   ├── market_data/
│   │   └── market_data_views.py
│   ├── instruments/
│   │   └── instrument_views.py
│   ├── risk/
│   │   └── risk_views.py
│   ├── emsa/
│   │   └── emsa_views.py
│   ├── shared/
│   │   ├── sidebar.py
│   │   ├── top_navigation.py
│   │   ├── performance_header.py
│   │   ├── notification_sidebar.py
│   │   ├── contextual_workspace.py
│   │   └── mobile_nav.py
│   └── portfolio/
│       ├── alerts_panel.py
│       ├── allocation_chart.py
│       ├── dividend_tracker.py
│       ├── goal_components.py
│       ├── holdings_table.py
│       ├── news_feed.py
│       ├── performers_widget.py
│       ├── portfolio_modals.py
│       ├── report_charts.py
│       ├── research_components.py
│       ├── sector_breakdown.py
│       ├── stock_card.py
│       ├── summary_cards.py
│       └── transaction_history.py
├── states/
│   ├── dashboard/
│   │   ├── portfolio_dashboard_state.py
│   │   └── dashboard_state.py
│   ├── portfolio/
│   │   ├── portfolio_state.py
│   │   ├── goals_state.py
│   │   └── watchlist_state.py
│   ├── user/
│   │   ├── profile_state.py
│   │   └── settings_state.py
│   ├── reports/
│   │   └── reports_state.py
│   ├── research/
│   │   └── research_state.py
│   ├── notifications/
│   │   ├── notification_state.py
│   │   └── notification_pagination_state.py
│   └── navigation/
│       └── mobile_nav_state.py
└── pages/
    ├── portfolio/
    │   ├── portfolio_page.py
    │   ├── goals_page.py
    │   └── watchlist_page.py
    ├── user/
    │   ├── profile_page.py
    │   └── settings_page.py
    ├── reports/
    │   └── reports_page.py
    ├── research/
    │   └── research_page.py
    └── notifications/
        └── notifications_page.py
```

## Folder Naming Conventions

| Folder Name | Purpose | Contents |
|-------------|---------|----------|
| positions | Positions & Trade Summary View | All position-related tabs and components |
| compliance | Compliance & Holdings View | Compliance monitoring tabs |
| portfolio_tools | Pay-To-Hold & Settlement View | Settlement, borrow, and special terms tabs |
| pnl | PnL View | Profit and loss analysis tabs |
| reconciliation | Reconciliation View | Data reconciliation tabs |
| operations | Operational Processes View | Operational monitoring tabs |
| market_data | Market Data & Events View | Market information and events tabs |
| instruments | Ticker & Instrument Analysis View | Instrument screening and analysis tabs |
| risk | Risk & Pricing View | Risk metrics and pricing tabs |
| emsa | EMSA Order Management View | Order management tabs |
| shared | Global UI Elements | Navigation, headers, sidebars used across pages |
| portfolio | Portfolio Management Features | User portfolio-specific components |
| dashboard | Dashboard States | Main dashboard state management |
| user | User-Related Features | Profile and settings |
| notifications | Notification Features | Notification display and pagination |
| navigation | Navigation States | Mobile and menu navigation |

## File Migration Strategy

The migration will follow a phased approach to minimize disruption:

### Phase 1: Component Organization

Organize components by functional domain based on the requirements document's page structure.

| Source File | Destination Path | Rationale |
|------------|------------------|-----------|
| positions_views.py | components/positions/ | Contains 5 tabs for Section 3.1 |
| compliance_views.py | components/compliance/ | Contains 4 tabs for Section 3.2 |
| portfolio_tools_views.py | components/portfolio_tools/ | Contains 9 tabs for Section 3.3 |
| pnl_views.py | components/pnl/ | Contains 3 tabs for Section 3.4 |
| reconciliation_views.py | components/reconciliation/ | Contains 5 tabs for Section 3.5 |
| operations_views.py | components/operations/ | Contains 2 tabs for Section 3.6 |
| market_data_views.py | components/market_data/ | Contains 8 tabs for Section 3.7 |
| instrument_views.py | components/instruments/ | Contains 5 tabs for Section 3.8 |
| risk_views.py | components/risk/ | Contains 5 tabs for Section 3.9 |
| emsa_views.py | components/emsa/ | Contains 2 tabs for Section 3.10 |

### Phase 2: State Organization

Group state files by their functional responsibility and usage patterns.

| Source File | Destination Path | Primary Consumers |
|------------|------------------|-------------------|
| portfolio_dashboard_state.py | states/dashboard/ | All 10 main view components |
| dashboard_state.py | states/dashboard/ | Performance header, summary cards |
| portfolio_state.py | states/portfolio/ | Portfolio page |
| goals_state.py | states/portfolio/ | Goals page |
| watchlist_state.py | states/portfolio/ | Watchlist page |
| profile_state.py | states/user/ | Profile page |
| settings_state.py | states/user/ | Settings page |
| reports_state.py | states/reports/ | Reports page |
| research_state.py | states/research/ | Research page |
| notification_state.py | states/notifications/ | Notification sidebar |
| notification_pagination_state.py | states/notifications/ | Notification pagination |
| mobile_nav_state.py | states/navigation/ | Mobile navigation |

### Phase 3: Page Organization

Organize pages by feature domain for logical grouping.

| Source File | Destination Path | Related Components |
|------------|------------------|-------------------|
| portfolio_page.py | pages/portfolio/ | Portfolio components |
| goals_page.py | pages/portfolio/ | Goal components |
| watchlist_page.py | pages/portfolio/ | Watchlist components |
| profile_page.py | pages/user/ | Profile components |
| settings_page.py | pages/user/ | Settings components |
| reports_page.py | pages/reports/ | Report charts |
| research_page.py | pages/research/ | Research components |
| notifications_page.py | pages/notifications/ | Notification components |

### Phase 4: Shared Component Organization

Separate globally-used components from domain-specific ones.

| Source File | Destination Path | Usage Scope |
|------------|------------------|-------------|
| sidebar.py | components/shared/ | Global navigation element |
| top_navigation.py | components/shared/ | Global header element |
| performance_header.py | components/shared/ | Global dashboard header |
| notification_sidebar.py | components/shared/ | Global notification panel |
| contextual_workspace.py | components/shared/ | Global workspace container |
| mobile_nav.py | components/shared/ | Global mobile navigation |

### Phase 5: Portfolio-Specific Components

Group user portfolio management components separately from the main dashboard views.

| Source File | Destination Path | Page Association |
|------------|------------------|------------------|
| alerts_panel.py | components/portfolio/ | Portfolio page |
| allocation_chart.py | components/portfolio/ | Portfolio page |
| dividend_tracker.py | components/portfolio/ | Portfolio page |
| goal_components.py | components/portfolio/ | Goals page |
| holdings_table.py | components/portfolio/ | Portfolio page |
| news_feed.py | components/portfolio/ | Portfolio page |
| performers_widget.py | components/portfolio/ | Portfolio page |
| portfolio_modals.py | components/portfolio/ | Portfolio page |
| report_charts.py | components/portfolio/ | Reports page |
| research_components.py | components/portfolio/ | Research page |
| sector_breakdown.py | components/portfolio/ | Portfolio page |
| stock_card.py | components/portfolio/ | Portfolio page |
| summary_cards.py | components/portfolio/ | Dashboard/Portfolio page |
| transaction_history.py | components/portfolio/ | Portfolio page |

## Import Path Update Strategy

The reorganization requires updating import paths throughout the codebase. The following pattern describes the transformation:

### Import Transformation Pattern

| Import Type | Before | After |
|-------------|--------|-------|
| Component imports | `from app.components.positions_views import positions_table` | `from app.components.positions.positions_views import positions_table` |
| State imports | `from app.states.portfolio_state import PortfolioState` | `from app.states.portfolio.portfolio_state import PortfolioState` |
| Page imports | `from app.pages.portfolio_page import portfolio_page` | `from app.pages.portfolio.portfolio_page import portfolio_page` |

### Files Requiring Import Updates

| File Category | Affected Files | Update Scope |
|--------------|----------------|--------------|
| Workspace orchestrator | contextual_workspace.py | Updates imports for all 10 view components |
| Page files | All 8 page files | Update component and state imports |
| Main application | app.py | Update page imports |
| Cross-referencing components | Components importing other components | Update sibling imports |

## Module Initialization Requirements

Each new subfolder requires an `__init__.py` file to maintain Python module structure.

### Purpose of __init__.py Files

| File Location | Export Strategy | Purpose |
|--------------|----------------|---------|
| components/positions/__init__.py | Re-export view functions | Simplify external imports |
| components/compliance/__init__.py | Re-export view functions | Simplify external imports |
| components/portfolio_tools/__init__.py | Re-export view functions | Simplify external imports |
| components/pnl/__init__.py | Re-export view functions | Simplify external imports |
| components/reconciliation/__init__.py | Re-export view functions | Simplify external imports |
| components/operations/__init__.py | Re-export view functions | Simplify external imports |
| components/market_data/__init__.py | Re-export view functions | Simplify external imports |
| components/instruments/__init__.py | Re-export view functions | Simplify external imports |
| components/risk/__init__.py | Re-export view functions | Simplify external imports |
| components/emsa/__init__.py | Re-export view functions | Simplify external imports |
| components/shared/__init__.py | Re-export shared components | Global component access |
| components/portfolio/__init__.py | Re-export portfolio components | Portfolio feature access |

### Example __init__.py Structure

For domain-specific component folders, the initialization file will re-export all public functions from the views file to maintain clean import paths:

```
Example for components/positions/__init__.py:

Re-exports all position view functions including:
- positions_table
- stock_position_table
- warrant_position_table
- bond_position_table
- trade_summary_table
```

For state folders, similar re-export patterns apply to state classes.

## Benefits of This Organization

| Benefit Category | Description | Impact |
|-----------------|-------------|---------|
| Maintainability | Related tabs grouped together in a single folder | Easier to locate and modify related functionality |
| Scalability | New tabs can be added to existing folders | Avoids folder-level clutter as features grow |
| Navigation | Clear mapping between UI pages and file structure | Developers can quickly find files by page name |
| Collaboration | Reduced merge conflicts when working on different pages | Teams can work on separate folders independently |
| Documentation Alignment | Folder structure mirrors requirements document sections | Direct correspondence between specs and code |
| Import Clarity | Import paths reflect functional domains | More semantic and self-documenting code |
| Testing Organization | Test files can mirror the same folder structure | Easier to organize and locate tests |

## Migration Validation Checklist

After reorganization, validate the following:

| Validation Item | Success Criteria | Verification Method |
|----------------|------------------|---------------------|
| Import resolution | All imports resolve correctly | Run application without import errors |
| Functional integrity | All 10 main views render correctly | Navigate through all tabs and verify display |
| State management | State updates propagate correctly | Test interactive features on each page |
| Build process | Application builds without errors | Execute build command successfully |
| Component accessibility | All exported components remain accessible | Verify imports from external modules |
| Module structure | All folders contain __init__.py | Check folder structure completeness |
| Path consistency | All import paths follow new convention | Code review of import statements |
| Navigation flows | Tab switching works correctly | Test navigation within each main view |

## Conclusion

This reorganization strategy transforms the flat file structure into a hierarchical organization that directly reflects the application's functional architecture as defined in the requirements document. By grouping tabs from the same page into dedicated folders, the codebase becomes more maintainable, navigable, and aligned with the documented UI structure.

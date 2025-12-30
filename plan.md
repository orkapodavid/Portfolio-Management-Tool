# PnL View Module Enhancement Plan

## Phase 1: PnL View Data Structure & State Management ✅
- [x] Add PnL-specific data structures (PnLChange, PnLSummary, PnLCurrency TypedDicts)
- [x] Include missing columns from gap analysis: PnL Chg 2D, PnL Chg% 2D
- [x] Resolve truncated field: POS C → POS CCY PnL (full name)
- [x] Add mock data for all three PnL tabs with realistic financial values
- [x] Add sparkline data for PnL YTD and Daily Change metrics

## Phase 2: PnL View UI Components ✅
- [x] Create PnL Change tab with all columns including 2D change metrics
- [x] Create PnL Summary tab with DTL column (from 5% DTL)
- [x] Create PnL Currency tab with full POS CCY PnL column
- [x] Implement red/green color-coding for all PnL change values
- [x] Add sparkline mini-trend components for PnL YTD and Daily Change
- [x] Replace text status indicators with checkmark/alert icons for REC column

## Phase 3: Functional Improvements & Action Bar ✅
- [x] Move "Generate" button from bottom to top-left action area
- [x] Add PnL Full tab integration (keep separate but accessible)
- [x] Add export and refresh actions in top action bar
- [x] Implement consistent $(X,XXX.XX) negative formatting across all PnL values
- [x] Add right-alignment for all currency/numeric columns
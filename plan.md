# Portfolio Dashboard - Critical Layout Fixes (8 Issues)

## Current Goal
Address all 8 critical issues from detailed UI review to maximize data density and usability

---

## Phase 1: Top Navigation & KPI Deep Compaction
- [ ] Reduce top nav icons to 14px inline with text (not stacked)
- [ ] Compress top nav height to 48px total
- [ ] Convert KPIs to ultra-compact single-row format with 3px colored left borders
- [ ] Remove all large icon circles from KPI cards
- [ ] Target combined header (nav + KPIs): ~80px total height

---

## Phase 2: Top Movers Vertical Stack & Data Table Maximization
- [ ] Stack Top Movers grids vertically in a scrollable container (not horizontal)
- [ ] Make Top Movers collapsible (hidden by default)
- [ ] Reduce grid row heights to 22px
- [ ] Maximize data table to 80%+ viewport height
- [ ] Reduce table row height to 20px with 8px padding
- [ ] Add 50+ mock rows for proper scroll demonstration

---

## Phase 3: Responsive Layout & Sidebar Fixes
- [ ] Make notification sidebar toggleable via bell icon
- [ ] Add slide-in/out animation for sidebar (300ms transition)
- [ ] Make performance header sticky below nav (z-index 50)
- [ ] Add unread notification count badge to bell icon
- [ ] Standardize all spacing: 4-8px gaps, 8-12px padding
- [ ] Final layout verification

---

## Target Layout After Fixes
```
┌─────────────────────────────────────────────────────┐
│ [Icon] Market [Icon] Positions [Icon] PnL ...       │ ← 40px
├─────────────────────────────────────────────────────┤
│ DAILY PnL: +$1.2M │ YTD DISC: +$45.8M │ YTD R/U:.. │ ← 32px (sticky)
├─────────────────────────────────────────────────────┤
│ [▼ Top Movers] (collapsible, hidden by default)     │
├─────────────────────────────────────────────────────┤
│ [📅 Date] [🔍 Search] [Auto-Refresh ⟳]             │ ← 36px
├─────────────────────────────────────────────────────┤
│  MAIN DATA TABLE (80%+ viewport, 20px rows)       │ 🔔
│  Ticker │ Desc │ Class │ Qty │ Price │ MktVal... │ Sidebar
│  AAPL   │ Apple│ Equity│15.4K│182.50 │ 2.8M ...  │ (toggle)
│  ... (50+ rows with virtual scroll)               │
├─────────────────────────────────────────────────────┤
│               [GENERATE MARKET DATA]                │
└─────────────────────────────────────────────────────┘
```

# Task: Refactor Codebase to Module-Based Page/Tab Structure

## Goal
Refactor the codebase (specifically `pmt_core_pkg/pmt_core`) to ensure that all Python scripts are layered by folder based on the **Pages/Tab Module Implementation**.

## Reference
- **Project Structure**: See `README.md` for the target structure.
- **Rules**: See `AGENTS.md` -> "Page/Tab Folder Architecture".
- **Concept**: See `docs/style_guides/reflex-module-layout-tabs-prompt.md` for the conceptual layout.

## Instructions

1. **Analyze the Current Structure**
   - Identify files in `pmt_core_pkg/pmt_core/models`, `pmt_core_pkg/pmt_core/services`, and `pmt_core_pkg/pmt_core/repositories` that use a flat structure (e.g., `enums.py`, `types.py` in root models).

2. **Categorize by Module**
   - Determine which module each file or class belongs to.
     - `PositionRecord` -> `positions`
     - `PnLRecord` -> `pnl`
     - `PricingService` -> `pricing` (or `analytics`?)
     - `ReportService` -> `reports`
     - `InstrumentType` -> `instruments` or `common`

3. **Create Module Subdirectories**
   - Create subdirectories matching the module names in `pmt_core_pkg/pmt_core/[layer]/[module]/`.

4. **Move and Split Files**
   - **For Models**: Split `types.py` and `enums.py` into module-specific files.
     - `models/pnl/types.py` (PnLRecord)
     - `models/positions/types.py` (PositionRecord)
     - `models/common/enums.py` (Common enums like InstrumentType)
   - **For Services**: Move service files into their respective folders.
     - `services/pricing_service.py` -> `services/pricing/pricing_service.py`
     - `services/report_service.py` -> `services/reports/report_service.py`

5. **Update Imports**
   - **Crucial**: Trace all usages of the moved/split classes and update imports across the entire codebase (`app/` and `pmt_core_pkg/pmt_core/`).
   - Use `pmt_core_pkg/pmt_core/__init__.py` to re-export common types if necessary to maintain backward compatibility during the transition, OR perform a clean refactor by updating all import paths.

6. **Verify**
   - Run `uv run pytest` to ensure no import errors or broken logic.
   - Run `uv run reflex run` to confirm the app starts.
   - **Visual Verification** (see `docs/web/pages.md` for complete list):
     - **Market Data**: `/market-data`, `/market-data/fx-data`, `/market-data/reference-data`, `/market-data/historical-data`, `/market-data/trading-calendar`, `/market-data/market-hours`
     - **Positions**: `/positions`, `/positions/stock-position`, `/positions/warrant-position`, `/positions/bond-positions`, `/positions/trade-summary`
     - **PnL**: `/pnl`, `/pnl/pnl-change`, `/pnl/pnl-summary`, `/pnl/pnl-currency`, `/pnl/pnl-full`
     - **Risk**: `/risk`, `/risk/delta-change`, `/risk/risk-measures`, `/risk/risk-inputs`, `/risk/pricer-warrant`, `/risk/pricer-bond`
     - **Recon**: `/recon`, `/recon/pps-recon`, `/recon/settlement-recon`, `/recon/failed-trades`, `/recon/pnl-recon`, `/recon/risk-input-recon`
     - **Compliance**: `/compliance`, `/compliance/restricted-list`, `/compliance/undertakings`, `/compliance/beneficial-ownership`, `/compliance/monthly-exercise-limit`
     - **Portfolio Tools**: `/portfolio-tools`, `/portfolio-tools/pay-to-hold`, `/portfolio-tools/short-ecl`, `/portfolio-tools/stock-borrow`, `/portfolio-tools/po-settlement`, `/portfolio-tools/deal-indication`, `/portfolio-tools/reset-dates`, `/portfolio-tools/coming-resets`, `/portfolio-tools/cb-installments`, `/portfolio-tools/excess-amount`
     - **Instruments**: `/instruments`, `/instruments/ticker-data`, `/instruments/stock-screener`, `/instruments/special-term`, `/instruments/instrument-data`, `/instruments/instrument-term`
     - **Events**: `/events`, `/events/event-calendar`, `/events/event-stream`, `/events/reverse-inquiry`
     - **Operations**: `/operations`, `/operations/daily-procedure-check`, `/operations/operation-process`
     - **Orders**: `/orders`, `/orders/emsx-order`, `/orders/emsx-route`
     - **Confirm**: Tables are rendering with mock data (not empty).
     - **Confirm**: The Notification Sidebar on the right is populated with alerts.

## Scope
- **Primary Target**: `pmt_core_pkg/pmt_core/`
- **Secondary Target**: Verify `app/` follows the structure (it largely does, but check for outliers).

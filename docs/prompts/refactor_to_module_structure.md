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

## Scope
- **Primary Target**: `pmt_core_pkg/pmt_core/`
- **Secondary Target**: Verify `app/` follows the structure (it largely does, but check for outliers).

# Refactor Pricer Views and Add Plotly Charts Implementation Plan

## Goal Description
Refactor `pricer_bond_view` and `pricer_warrant_view` from `app/components/risk/risk_views.py` into separate files: `app/components/risk/pricer_bond_view.py` and `app/components/risk/pricer_warrant_view.py`.
Implement a 2D Plotly chart (Yield Curve) for `pricer_bond_view` and a 3D Plotly chart (Volatility Surface) for `pricer_warrant_view` using mock data.

## User Review Required
None.

## Proposed Changes

### app/components/risk

#### [NEW] [pricer_bond_view.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/risk/pricer_bond_view.py)
- Move `pricer_bond_view` logic here.
- Import `header_cell`, `text_cell` from `.risk_views`.
- Implement `PricerBondState`:
    - Add `x_axis`, `y_axis`, `z_axis` state variables.
    - Implement `generate_chart` method to return `go.Figure`.
    - Logic: If `z_axis` is "None", render 2D chart (X vs Y). Else, render 3D chart (X vs Y vs Z).
- Update UI Layout:
    - **Top section**: Preserve existing 2-column layout (Terms vs Pricing Results) exactly as is.
    - **Middle section**: Selectors for X, Y, and Z axes.
    - **Bottom section**: `rx.plotly` chart occupying full width.

#### [NEW] [pricer_warrant_view.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/risk/pricer_warrant_view.py)
- Move `pricer_warrant_view` logic here.
- Import `header_cell`, `text_cell` from `.risk_views`.
- Implement `PricerWarrantState`:
    - Add `x_axis`, `y_axis`, `z_axis` state variables.
    - Implement `generate_chart` method to return `go.Figure`.
    - Logic: If `z_axis` is "None", render 2D chart (X vs Y). Else, render 3D chart (X vs Y vs Z).
- Update UI Layout:
    - **Top section**: Preserve existing 2-column layout (Terms vs Simulations & Outputs) exactly as is.
    - **Middle section**: Selectors for X, Y, and Z axes.
    - **Bottom section**: `rx.plotly` chart occupying full width.

#### [MODIFY] [risk_views.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/risk/risk_views.py)
- Remove `pricer_bond_view` and `pricer_warrant_view`.
- Ensure `header_cell` and `text_cell` are available for import.

#### [MODIFY] [__init__.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/risk/__init__.py)
- Update imports to pull views from the new files.

### app/pages/risk

#### [MODIFY] [pricer_bond_page.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/pages/risk/pricer_bond_page.py)
- Update import to `from app.components.risk.pricer_bond_view import pricer_bond_view`.

#### [MODIFY] [pricer_warrant_page.py](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/pages/risk/pricer_warrant_page.py)
- Update import to `from app.components.risk.pricer_warrant_view import pricer_warrant_view`.

## Verification Plan

### Automated Tests
- Run `uv run reflex run` to check for import errors.
- (Implicit) The user can verify the charts by navigating to:
    - `http://localhost:3001/pmt/risk/pricer-warrant`
    - `http://localhost:3001/pmt/risk/pricer-bond`

### Manual Verification
- **Pricer Bond**:
    - Verify Top Section still has 2 columns (Terms/Results).
    - Verify Bottom Section has Chart controls and Chart.
    - Switch 2D/3D via Z-axis selection.
- **Pricer Warrant**:
    - Verify Top Section still has 2 columns (Terms/Simulations).
    - Verify Bottom Section has Chart controls and Chart.
    - Switch 2D/3D via Z-axis selection.

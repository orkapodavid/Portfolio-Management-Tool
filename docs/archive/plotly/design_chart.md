> [!NOTE]
> **Status: ✅ Archived** — 2026-02-19
> Design implemented in `pricer_bond_view.py` and `pricer_warrant_view.py` with 2D/3D Plotly charts.

# Design Chart: Dynamic Pricer Visualization

This document outlines the design for integrating dynamic 2D/3D Plotly charts into the Pricer Bond and Pricer Warrant views.

## User Flow & State Logic

```mermaid
graph TD
    User[User] -->|Selects Axes| UI_Controls
    
    subgraph UI_Controls [Axis Selection]
        X[X-Axis Dropdown]
        Y[Y-Axis Dropdown]
        Z[Z-Axis Dropdown]
    end

    X -->|Update| State
    Y -->|Update| State
    Z -->|Update| State
    
    State -->|Check Z-Axis| Logic{Z Selected?}
    Logic -->|No (None)| Mode2D[2D Mode]
    Logic -->|Yes| Mode3D[3D Mode]
    
    Mode2D -->|Render| Chart2D[2D Line/Scatter]
    Mode3D -->|Render| Chart3D[3D Surface/Mesh]
    
    Chart2D --> View
    Chart3D --> View
```

## Chart Specifications

### 1. Pricer Bond Visualization

| Feature | 2D Mode | 3D Mode |
| :--- | :--- | :--- |
| **Logic** | Z-Axis == "None" | Z-Axis != "None" |
| **Available Axes** | Yield, Maturity, Coupon, Price, Duration, Convexity | Same |
| **Interaction** | Hover, Zoom, Pan | Rotate, Zoom, Hover |

### 2. Pricer Warrant Visualization

| Feature | 2D Mode | 3D Mode |
| :--- | :--- | :--- |
| **Logic** | Z-Axis == "None" | Z-Axis != "None" |
| **Available Axes** | Spot Price, Strike, Volatility, Time, Gamma, Delta, Value | Same |
| **Interaction** | Hover, Zoom, Pan | Rotate, Zoom, Hover |

## Visual Layout

The layout preserves the existing 2-column structure for the inputs and results at the top. The new visualization section is added below.

```
+-------------------------------------------------------+
|  Top Section (Unchanged Layout)                       |
|                                                       |
|  +---------------------+   +-----------------------+  |
|  | Column 1: Terms     |   | Column 2: Results     |  |
|  |                     |   |                       |  |
|  | Valuation Date: [..]|   | Simulation #: ...     |  |
|  | Strike Price:   [..]|   | Fair Value: $45.20    |  |
|  | ...                 |   | Delta: 0.65           |  |
|  |                     |   |                       |  |
|  +---------------------+   +-----------------------+  |
|                                                       |
+-------------------------------------------------------+
|  Visualization Controls                               |
|  X-Axis: [ Select v]   Y-Axis: [ Select v]   Z-Axis: [ Select (Optional) v] |
+-------------------------------------------------------+
|  Visualization Panel (Bottom Section, Full Width)     |
|                                                       |
|   +-----------------------------------------------+   |
|   |                                               |   |
|   |             [ Dynamic Plotly Chart ]          |   |
|   |         (Resizes to fill this container)      |   |
|   |                                               |   |
|   +-----------------------------------------------+   |
|                                                       |
+-------------------------------------------------------+
```

## Technical Components

### State Management
- **`RiskState`**: Base state.
- **`BondState` / `WarrantState`**:
    - `x_axis`: str (Default e.g., "Maturity")
    - `y_axis`: str (Default e.g., "Yield")
    - `z_axis`: str (Default "None")
    - `computed_fig`: `go.Figure` (Computed var based on axes)

### UI Components
- **`axis_selector`**: Helper component for the dropdowns.
- **`chart_container`**: `rx.box` wrapper with `width="100%"` and `height="50vh"` (or similar) to ensure responsiveness.

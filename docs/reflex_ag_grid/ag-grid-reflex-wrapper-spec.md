# AG Grid Custom Wrapper for Reflex Python

## Executive Summary

Build a **generic, reusable AG Grid Enterprise wrapper** as a custom Reflex component for high-frequency real-time data grids. The wrapper must handle 1000+ rows with cell-level updates every 200ms while maintaining responsive UI and supporting trading-terminal features.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Project Structure](#2-project-structure)
3. [Core Requirements](#3-core-requirements)
4. [Component Specifications](#4-component-specifications)
5. [JavaScript Wrapper Implementation](#5-javascript-wrapper-implementation)
6. [Python Backend Services](#6-python-backend-services)
7. [Reflex Integration](#7-reflex-integration)
8. [Configuration Formats](#8-configuration-formats)
9. [API Reference](#9-api-reference)
10. [Usage Examples](#10-usage-examples)
11. [Performance Guidelines](#11-performance-guidelines)
12. [Testing Requirements](#12-testing-requirements)

---

## 1. Architecture Overview

### 1.1 Design Principles

**Critical Constraint:** At 200ms update frequency with 1000 rows, tick data CANNOT flow through Reflex state. Each Reflex state change triggers full component reconciliation, causing unacceptable latency.

**Solution:** Hybrid architecture with two data paths:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BROWSER                                         │
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                    AG Grid Enterprise                               │    │
│   │   - Direct DOM updates via AG Grid API                              │    │
│   │   - flashCells() for visual feedback                                │    │
│   │   - applyTransactionAsync() for batch updates                       │    │
│   └───────────────────────────▲────────────────────────────────────────┘    │
│                               │                                              │
│           ┌───────────────────┴───────────────────┐                         │
│           │                                       │                         │
│   ┌───────┴────────┐                    ┌────────┴────────┐                 │
│   │ Tick WebSocket │                    │  Reflex State   │                 │
│   │  (Fast Path)   │                    │  (Slow Path)    │                 │
│   │                │                    │                 │                 │
│   │ - 200ms ticks  │                    │ - User actions  │                 │
│   │ - Delta only   │                    │ - Config        │                 │
│   │ - Direct to JS │                    │ - Notifications │                 │
│   └───────┬────────┘                    └────────┬────────┘                 │
│           │                                      │                          │
└───────────┼──────────────────────────────────────┼──────────────────────────┘
            │                                      │
            │ WebSocket (dedicated)                │ Reflex WebSocket
            │                                      │
┌───────────┼──────────────────────────────────────┼──────────────────────────┐
│           │                 BACKEND              │                          │
│   ┌───────┴────────┐                    ┌────────┴────────┐                 │
│   │ Tick Publisher │                    │  Reflex State   │                 │
│   │   (FastAPI)    │                    │    Handlers     │                 │
│   └───────┬────────┘                    └─────────────────┘                 │
│           │                                                                  │
│   ┌───────┴────────────────────────────────────────────────────────────┐    │
│   │                      Data Layer                                     │    │
│   │   - Database polling (configurable interval)                        │    │
│   │   - Scheduled refresh times                                         │    │
│   │   - .ini validation config loader                                   │    │
│   └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow Paths

| Path | Purpose | Latency Target | Mechanism |
|------|---------|----------------|-----------|
| **Fast Path** | Tick data updates | <50ms | Dedicated WebSocket → JS API |
| **Slow Path** | User interactions, config | <500ms | Reflex state management |

---

## 2. Project Structure

```
reflex_ag_grid/
├── __init__.py
├── components/
│   ├── __init__.py
│   ├── ag_grid.py              # Reflex custom component definition
│   ├── ag_grid_state.py        # Shared state management
│   └── notification_panel.py   # Notification UI component
├── services/
│   ├── __init__.py
│   ├── tick_publisher.py       # WebSocket tick broadcasting
│   ├── validation_loader.py    # .ini config parser
│   └── scheduled_refresh.py    # Timed database refresh
├── static/
│   └── ag_grid_wrapper.js      # Core AG Grid React wrapper
├── config/
│   └── validation.example.ini  # Example validation config
└── examples/
    ├── basic_grid.py           # Minimal example
    ├── realtime_trading.py     # Full trading grid example
    └── grouped_data.py         # Grouping/aggregation example
```

---

## 3. Core Requirements

### Requirements Matrix

| # | Requirement | Priority | Component | Implementation |
|---|-------------|----------|-----------|----------------|
| 1 | Right-click context menu | High | JS Wrapper | `getContextMenuItems()` callback |
| 2 | Bulk state changes | High | JS Wrapper | `applyTransactionAsync({ update: [...] })` |
| 3 | Blinking cell changes | High | JS Wrapper | `api.flashCells()` after delta |
| 4 | Notification → row jump | Medium | JS + Reflex | `ensureNodeVisible()` + highlight |
| 5 | Table grouping + summary | Medium | JS Wrapper | `rowGroup` + `aggFunc` columns |
| 6 | Notification publisher | Medium | Python | Reflex state + UI component |
| 7 | Validation from .ini | Medium | Python + JS | ConfigParser → props → validators |
| 8 | Copy cell/with header | High | JS Wrapper | Context menu + Clipboard API |
| 9 | Export to Excel | Medium | JS Wrapper | `api.exportDataAsExcel()` |
| 10 | WebSocket tick data | Critical | Python + JS | FastAPI WS + JS client |
| 11 | Cell editors by type | High | JS Wrapper | Editor mapping per column type |
| 12 | Pause updates on edit | Critical | JS Wrapper | Track editing cells, skip updates |
| 13 | Cell-by-cell delta update | Critical | Python + JS | Delta computation + batch apply |
| 14 | Scheduled DB refresh | Low | Python | Cron-like scheduler |
| 15 | Persist grid state | Medium | JS Wrapper | localStorage for columns/filters |

---

## 4. Component Specifications

### 4.1 AG Grid Reflex Component

**File:** `components/ag_grid.py`

```python
"""
AG Grid Custom Component for Reflex

This module defines the Reflex wrapper around AG Grid Enterprise.
The component handles:
- Column definitions with type-based editors
- Initial data loading
- WebSocket URL configuration
- Validation config pass-through
- Event callbacks to Reflex state
"""

import reflex as rx
from typing import Any, Callable, Optional
from reflex.components.component import Component, NoSSRComponent


class AGGrid(NoSSRComponent):
    """
    Custom AG Grid wrapper component for Reflex.
    
    This component renders AG Grid Enterprise with real-time update capabilities.
    Tick data flows directly via WebSocket to avoid Reflex state overhead.
    
    Props:
        column_defs: List of column definition objects
        row_data: Initial row data (subsequent updates via WebSocket)
        websocket_url: URL for tick data WebSocket connection
        validation_config: Dict of field -> validation rules
        auto_refresh: Whether to apply incoming tick updates
        grid_options: Additional AG Grid options to merge
        
    Events:
        on_cell_edit: Fired when user edits a cell
        on_row_right_click: Fired on right-click (before context menu)
        on_selection_change: Fired when row selection changes
        on_grid_ready: Fired when grid is initialized
    """
    
    # Import from our custom JS wrapper
    library = "/static/ag_grid_wrapper.js"
    tag = "AGGridWrapper"
    
    # Disable SSR - AG Grid requires browser APIs
    is_default = False
    
    # ===== Props =====
    
    column_defs: rx.Var[list[dict]]
    """
    Column definitions following AG Grid ColDef interface.
    Extended with custom properties:
    - type: 'str' | 'int' | 'float' | 'bool' | 'enum' | 'date'
    - enumValues: list[str] for enum type
    - validation: dict with min/max/pattern rules
    """
    
    row_data: rx.Var[list[dict]]
    """Initial row data. Each row MUST have unique 'id' field."""
    
    websocket_url: rx.Var[str]
    """WebSocket URL for tick data. Example: 'ws://localhost:8000/ws/ticks'"""
    
    validation_config: rx.Var[dict]
    """
    Validation rules per field, typically loaded from .ini file.
    Format: { field_name: { min, max, pattern, type, enum_values } }
    """
    
    auto_refresh: rx.Var[bool] = True
    """Whether to apply incoming WebSocket updates. Toggle for edit mode."""
    
    grid_options: rx.Var[dict] = {}
    """Additional AG Grid options to merge with defaults."""
    
    row_id_field: rx.Var[str] = "id"
    """Field name to use as unique row identifier."""
    
    theme: rx.Var[str] = "ag-theme-balham-dark"
    """AG Grid theme class name."""
    
    height: rx.Var[str] = "100%"
    """Grid container height."""
    
    width: rx.Var[str] = "100%"
    """Grid container width."""
    
    # ===== Event Handlers =====
    
    on_cell_edit: rx.EventHandler[lambda data: [data]]
    """
    Fired when cell edit is completed.
    Payload: { rowId, field, oldValue, newValue, rowData }
    """
    
    on_row_right_click: rx.EventHandler[lambda row_id, row_data, x, y: [row_id, row_data, x, y]]
    """
    Fired on row right-click before context menu.
    Payload: rowId, full row data, mouse x, mouse y
    """
    
    on_selection_change: rx.EventHandler[lambda selected_rows: [selected_rows]]
    """
    Fired when row selection changes.
    Payload: list of selected row data objects
    """
    
    on_grid_ready: rx.EventHandler[lambda: []]
    """Fired when grid is fully initialized."""
    
    on_cell_value_changed: rx.EventHandler[lambda data: [data]]
    """
    Fired immediately when cell value changes (before edit complete).
    Payload: { rowId, field, oldValue, newValue }
    """

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create an AGGrid component instance."""
        # Ensure required props
        if "column_defs" not in props:
            raise ValueError("column_defs is required")
        if "websocket_url" not in props:
            raise ValueError("websocket_url is required")
            
        return super().create(*children, **props)


# Convenience function for creating grid
def ag_grid(**props) -> AGGrid:
    """
    Create an AG Grid component.
    
    Example:
        ag_grid(
            column_defs=[
                {"field": "id", "headerName": "ID"},
                {"field": "price", "headerName": "Price", "type": "int", "editable": True}
            ],
            row_data=State.initial_data,
            websocket_url="ws://localhost:8000/ws/ticks",
            on_cell_edit=State.handle_cell_edit
        )
    """
    return AGGrid.create(**props)
```

### 4.2 AG Grid State Management

**File:** `components/ag_grid_state.py`

```python
"""
Shared state management for AG Grid component.

This module provides base state classes that can be extended
for specific grid implementations.
"""

import reflex as rx
from typing import Any, Optional
from datetime import datetime


class AGGridBaseState(rx.State):
    """
    Base state class for AG Grid functionality.
    
    Extend this class to add application-specific state.
    Provides common functionality for:
    - Auto-refresh toggle
    - Notification management  
    - Grid control via JavaScript calls
    """
    
    # ===== Core State =====
    
    auto_refresh: bool = True
    """Global toggle for WebSocket updates."""
    
    editing_row_id: Optional[str] = None
    """Currently editing row ID (for UI indicators)."""
    
    notifications: list[dict] = []
    """
    List of notifications to display.
    Each notification: { id, message, row_id, type, timestamp }
    """
    
    validation_config: dict = {}
    """Loaded validation configuration from .ini file."""
    
    selected_rows: list[dict] = []
    """Currently selected rows in grid."""
    
    # ===== Auto Refresh Control =====
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh and sync to JavaScript."""
        self.auto_refresh = not self.auto_refresh
        return rx.call_script(
            f"window.gridController?.setAutoRefresh({str(self.auto_refresh).lower()})"
        )
    
    def set_auto_refresh(self, enabled: bool):
        """Set auto-refresh to specific value."""
        self.auto_refresh = enabled
        return rx.call_script(
            f"window.gridController?.setAutoRefresh({str(enabled).lower()})"
        )
    
    # ===== Notification Management =====
    
    def add_notification(
        self,
        message: str,
        row_id: Optional[str] = None,
        notification_type: str = "info"
    ):
        """
        Add a notification to the list.
        
        Args:
            message: Notification text
            row_id: Optional row ID for jump-to functionality
            notification_type: 'info' | 'warning' | 'error' | 'success'
        """
        notification = {
            "id": f"notif_{datetime.now().timestamp()}",
            "message": message,
            "row_id": row_id,
            "type": notification_type,
            "timestamp": datetime.now().isoformat()
        }
        self.notifications = [notification] + self.notifications[:99]  # Keep last 100
    
    def clear_notification(self, notification_id: str):
        """Remove a specific notification."""
        self.notifications = [
            n for n in self.notifications if n["id"] != notification_id
        ]
    
    def clear_all_notifications(self):
        """Clear all notifications."""
        self.notifications = []
    
    # ===== Grid Control Methods =====
    
    def jump_to_row(self, row_id: str):
        """
        Scroll to and highlight a specific row.
        Typically called when clicking a notification.
        """
        return rx.call_script(f"window.gridController?.jumpToRow('{row_id}')")
    
    def refresh_grid(self):
        """Force refresh all cells."""
        return rx.call_script("window.gridController?.refresh()")
    
    def export_to_excel(self):
        """Trigger Excel export."""
        return rx.call_script("window.gridController?.exportExcel()")
    
    def export_to_csv(self):
        """Trigger CSV export."""
        return rx.call_script("window.gridController?.exportCsv()")
    
    def clear_filters(self):
        """Clear all column filters."""
        return rx.call_script("window.gridController?.clearFilters()")
    
    def reset_column_state(self):
        """Reset columns to default state."""
        return rx.call_script("window.gridController?.resetColumnState()")
    
    # ===== Event Handlers (Override in subclass) =====
    
    def handle_cell_edit(self, data: dict):
        """
        Handle cell edit event.
        
        Override in subclass to implement save logic.
        
        Args:
            data: { rowId, field, oldValue, newValue, rowData }
        """
        pass
    
    def handle_selection_change(self, selected_rows: list[dict]):
        """Handle row selection change."""
        self.selected_rows = selected_rows
    
    def handle_notification_click(self, notification: dict):
        """Handle notification click - jump to row."""
        if notification.get("row_id"):
            return self.jump_to_row(notification["row_id"])
```

### 4.3 Notification Panel Component

**File:** `components/notification_panel.py`

```python
"""
Notification panel component for displaying grid notifications.
"""

import reflex as rx
from .ag_grid_state import AGGridBaseState


def notification_item(notification: dict, on_click: callable, on_dismiss: callable) -> rx.Component:
    """Single notification item."""
    
    type_colors = {
        "info": "blue",
        "warning": "yellow",
        "error": "red",
        "success": "green"
    }
    
    return rx.box(
        rx.hstack(
            rx.box(
                width="4px",
                height="100%",
                bg=f"{type_colors.get(notification.get('type', 'info'), 'blue')}.500",
                border_radius="2px",
            ),
            rx.vstack(
                rx.text(
                    notification["message"],
                    font_size="sm",
                    color="gray.200",
                ),
                rx.text(
                    notification.get("timestamp", "")[:19],
                    font_size="xs",
                    color="gray.500",
                ),
                align_items="start",
                spacing="1",
                flex="1",
            ),
            rx.icon_button(
                rx.icon("x", size=14),
                size="xs",
                variant="ghost",
                on_click=lambda: on_dismiss(notification["id"]),
            ),
            spacing="2",
            width="100%",
        ),
        padding="3",
        bg="gray.800",
        border_radius="md",
        cursor="pointer" if notification.get("row_id") else "default",
        _hover={"bg": "gray.700"} if notification.get("row_id") else {},
        on_click=lambda: on_click(notification) if notification.get("row_id") else None,
    )


def notification_panel(
    state: AGGridBaseState,
    width: str = "320px",
    position: str = "right"
) -> rx.Component:
    """
    Notification panel sidebar.
    
    Args:
        state: AGGridBaseState instance with notifications
        width: Panel width
        position: 'left' or 'right'
    """
    
    position_styles = {
        "right": {"right": "0", "left": "auto"},
        "left": {"left": "0", "right": "auto"}
    }
    
    return rx.box(
        # Header
        rx.hstack(
            rx.text("Notifications", font_weight="bold", color="gray.200"),
            rx.spacer(),
            rx.badge(
                rx.text(f"{len(state.notifications)}"),
                color_scheme="blue",
                variant="solid",
            ),
            rx.icon_button(
                rx.icon("trash-2", size=14),
                size="xs",
                variant="ghost",
                on_click=state.clear_all_notifications,
                title="Clear all",
            ),
            width="100%",
            padding="3",
            border_bottom="1px solid",
            border_color="gray.700",
        ),
        
        # Notification list
        rx.box(
            rx.cond(
                len(state.notifications) > 0,
                rx.vstack(
                    rx.foreach(
                        state.notifications,
                        lambda n: notification_item(
                            n,
                            on_click=state.handle_notification_click,
                            on_dismiss=state.clear_notification
                        )
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.center(
                    rx.text("No notifications", color="gray.500", font_size="sm"),
                    height="100px",
                ),
            ),
            padding="2",
            overflow_y="auto",
            flex="1",
        ),
        
        # Styles
        position="fixed",
        top="0",
        width=width,
        height="100vh",
        bg="gray.900",
        border_left="1px solid" if position == "right" else "none",
        border_right="1px solid" if position == "left" else "none",
        border_color="gray.700",
        z_index="1000",
        display="flex",
        flex_direction="column",
        **position_styles.get(position, position_styles["right"]),
    )
```

---

## 5. JavaScript Wrapper Implementation

**File:** `static/ag_grid_wrapper.js`

This is the core JavaScript component that wraps AG Grid Enterprise.

```javascript
/**
 * AG Grid Wrapper for Reflex
 * 
 * This module provides a React component that wraps AG Grid Enterprise
 * with real-time update capabilities optimized for high-frequency data.
 * 
 * Features:
 * - WebSocket integration for tick data (bypasses React reconciliation)
 * - Delta updates with cell flashing
 * - Edit mode protection (pauses updates for edited cells)
 * - Context menu with copy/export actions
 * - Column state persistence to localStorage
 * - Type-based cell editors
 * - Validation integration
 */

import React, { useRef, useEffect, useCallback, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-enterprise';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-balham.css';

// ============================================================================
// GLOBAL CONTROLLER
// ============================================================================

/**
 * Global controller exposed for Reflex to call via rx.call_script()
 * 
 * Available methods:
 * - jumpToRow(rowId): Scroll to and highlight row
 * - setAutoRefresh(bool): Enable/disable tick updates
 * - refresh(): Force refresh all cells
 * - exportExcel(): Trigger Excel export
 * - exportCsv(): Trigger CSV export
 * - clearFilters(): Clear all filters
 * - resetColumnState(): Reset column positions/widths
 * - getSelectedRows(): Get currently selected rows
 * - selectRows(rowIds): Programmatically select rows
 */
window.gridController = null;

// ============================================================================
// CELL EDITORS CONFIGURATION
// ============================================================================

/**
 * Map column type to AG Grid cell editor
 */
function getCellEditor(type) {
    const editors = {
        'str': 'agTextCellEditor',
        'string': 'agTextCellEditor',
        'int': 'agNumberCellEditor',
        'integer': 'agNumberCellEditor',
        'float': 'agNumberCellEditor',
        'number': 'agNumberCellEditor',
        'bool': 'agCheckboxCellEditor',
        'boolean': 'agCheckboxCellEditor',
        'enum': 'agSelectCellEditor',
        'select': 'agSelectCellEditor',
        'date': 'agDateCellEditor',
        'datetime': 'agDateCellEditor',
        'largeText': 'agLargeTextCellEditor',
        'text': 'agLargeTextCellEditor',
    };
    return editors[type] || 'agTextCellEditor';
}

/**
 * Get cell editor params based on column type and config
 */
function getCellEditorParams(col) {
    const type = col.type || 'str';
    
    switch (type) {
        case 'enum':
        case 'select':
            return {
                values: col.enumValues || col.cellEditorParams?.values || []
            };
        
        case 'int':
        case 'integer':
            return {
                precision: 0,
                min: col.min ?? col.validation?.min,
                max: col.max ?? col.validation?.max,
                step: 1
            };
        
        case 'float':
        case 'number':
            return {
                precision: col.precision ?? 2,
                min: col.min ?? col.validation?.min,
                max: col.max ?? col.validation?.max,
                step: col.step ?? 0.01
            };
        
        case 'largeText':
        case 'text':
            return {
                maxLength: col.maxLength ?? 1000,
                rows: col.rows ?? 5,
                cols: col.cols ?? 50
            };
        
        default:
            return {};
    }
}

// ============================================================================
// VALIDATION
// ============================================================================

/**
 * Create value parser with validation
 */
function createValueParser(col, validationConfig) {
    const fieldValidation = validationConfig?.[col.field] || col.validation || {};
    const type = col.type || fieldValidation.type || 'str';
    
    return (params) => {
        let value = params.newValue;
        
        // Type coercion
        if (type === 'int' || type === 'integer') {
            value = parseInt(value, 10);
            if (isNaN(value)) return params.oldValue;
        } else if (type === 'float' || type === 'number') {
            value = parseFloat(value);
            if (isNaN(value)) return params.oldValue;
        } else if (type === 'bool' || type === 'boolean') {
            value = Boolean(value);
        }
        
        // Range validation
        if (fieldValidation.min !== undefined && value < fieldValidation.min) {
            console.warn(`Validation failed: ${col.field} below min ${fieldValidation.min}`);
            return params.oldValue;
        }
        if (fieldValidation.max !== undefined && value > fieldValidation.max) {
            console.warn(`Validation failed: ${col.field} above max ${fieldValidation.max}`);
            return params.oldValue;
        }
        
        // Pattern validation
        if (fieldValidation.pattern) {
            const regex = new RegExp(fieldValidation.pattern);
            if (!regex.test(String(value))) {
                console.warn(`Validation failed: ${col.field} doesn't match pattern`);
                return params.oldValue;
            }
        }
        
        // Enum validation
        if ((type === 'enum' || type === 'select') && fieldValidation.enum_values) {
            const allowed = fieldValidation.enum_values;
            if (!allowed.includes(value)) {
                console.warn(`Validation failed: ${col.field} not in allowed values`);
                return params.oldValue;
            }
        }
        
        return value;
    };
}

// ============================================================================
// CONTEXT MENU
// ============================================================================

/**
 * Build context menu items
 */
function buildContextMenuItems(params, customItems = []) {
    const defaultItems = [
        {
            name: 'Copy Cell',
            shortcut: 'Ctrl+C',
            icon: '<span class="ag-icon ag-icon-copy"></span>',
            action: () => {
                copyToClipboard(params.value);
            }
        },
        {
            name: 'Copy Cell with Header',
            action: () => {
                const header = params.colDef.headerName || params.colDef.field;
                copyToClipboard(`${header}\n${params.value}`);
            }
        },
        {
            name: 'Copy Row',
            action: () => {
                const columns = params.api.getAllDisplayedColumns();
                const headers = columns.map(c => c.getColDef().headerName || c.getColId());
                const values = columns.map(c => params.node.data[c.getColId()]);
                copyToClipboard(`${headers.join('\t')}\n${values.join('\t')}`);
            }
        },
        {
            name: 'Copy Row with Headers',
            action: () => {
                const columns = params.api.getAllDisplayedColumns();
                const headers = columns.map(c => c.getColDef().headerName || c.getColId());
                const values = columns.map(c => params.node.data[c.getColId()]);
                copyToClipboard(`${headers.join('\t')}\n${values.join('\t')}`);
            }
        },
        'separator',
        {
            name: 'Copy Selected Rows',
            disabled: !params.api.getSelectedRows().length,
            action: () => {
                const columns = params.api.getAllDisplayedColumns();
                const headers = columns.map(c => c.getColDef().headerName || c.getColId());
                const rows = params.api.getSelectedRows().map(row => 
                    columns.map(c => row[c.getColId()]).join('\t')
                );
                copyToClipboard(`${headers.join('\t')}\n${rows.join('\n')}`);
            }
        },
        'separator',
        {
            name: 'Export to Excel',
            icon: '<span class="ag-icon ag-icon-excel"></span>',
            action: () => {
                params.api.exportDataAsExcel({
                    fileName: `export_${new Date().toISOString().slice(0,10)}.xlsx`
                });
            }
        },
        {
            name: 'Export to CSV',
            icon: '<span class="ag-icon ag-icon-csv"></span>',
            action: () => {
                params.api.exportDataAsCsv({
                    fileName: `export_${new Date().toISOString().slice(0,10)}.csv`
                });
            }
        },
        'separator',
        {
            name: 'Reset Columns',
            action: () => {
                params.api.resetColumnState();
                localStorage.removeItem('gridColumnState');
            }
        }
    ];
    
    // Insert custom items after separator
    if (customItems.length > 0) {
        return [...customItems, 'separator', ...defaultItems];
    }
    
    return defaultItems;
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(String(text ?? ''));
    } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = String(text ?? '');
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
}

// ============================================================================
// LOCAL STORAGE PERSISTENCE
// ============================================================================

const STORAGE_KEY = 'ag_grid_column_state';

function saveColumnState(api, gridId) {
    try {
        const state = {
            columns: api.getColumnState(),
            filters: api.getFilterModel(),
            sort: api.getState().sort || []
        };
        const allStates = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        allStates[gridId] = state;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allStates));
    } catch (err) {
        console.warn('Failed to save column state:', err);
    }
}

function restoreColumnState(api, gridId) {
    try {
        const allStates = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        const state = allStates[gridId];
        if (!state) return;
        
        if (state.columns) {
            api.applyColumnState({ state: state.columns, applyOrder: true });
        }
        if (state.filters) {
            api.setFilterModel(state.filters);
        }
    } catch (err) {
        console.warn('Failed to restore column state:', err);
    }
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const AGGridWrapper = ({
    // Data props
    columnDefs = [],
    rowData = [],
    rowIdField = 'id',
    
    // WebSocket props
    websocketUrl,
    autoRefresh = true,
    
    // Configuration
    validationConfig = {},
    gridOptions = {},
    theme = 'ag-theme-balham-dark',
    height = '100%',
    width = '100%',
    gridId = 'default',
    
    // Event handlers (Reflex callbacks)
    onCellEdit,
    onRowRightClick,
    onSelectionChange,
    onGridReady,
    onCellValueChanged,
    
    // Custom context menu items
    contextMenuItems = []
}) => {
    // Refs
    const gridRef = useRef(null);
    const wsRef = useRef(null);
    const autoRefreshRef = useRef(autoRefresh);
    const editingCellsRef = useRef(new Set()); // Track cells being edited
    const reconnectTimeoutRef = useRef(null);
    
    // Keep autoRefresh ref in sync
    useEffect(() => {
        autoRefreshRef.current = autoRefresh;
    }, [autoRefresh]);
    
    // =========================================================================
    // COLUMN DEFINITIONS PROCESSING
    // =========================================================================
    
    const processedColumnDefs = useMemo(() => {
        return columnDefs.map(col => ({
            ...col,
            // Cell editor based on type
            cellEditor: col.cellEditor || getCellEditor(col.type),
            cellEditorParams: col.cellEditorParams || getCellEditorParams(col),
            
            // Value parser with validation
            valueParser: col.valueParser || createValueParser(col, validationConfig),
            
            // Cell class rules for styling
            cellClassRules: {
                ...col.cellClassRules,
                'ag-cell-flash': params => params.data?._flash?.[col.field],
                'ag-cell-invalid': params => params.data?._invalid?.[col.field],
                'ag-cell-editing-protected': params => 
                    editingCellsRef.current.has(`${params.data?.[rowIdField]}:${col.field}`)
            },
            
            // Ensure getRowId works
            getRowId: undefined  // Let grid level handle this
        }));
    }, [columnDefs, validationConfig, rowIdField]);
    
    // =========================================================================
    // WEBSOCKET CONNECTION
    // =========================================================================
    
    const connectWebSocket = useCallback(() => {
        if (!websocketUrl) return;
        
        // Close existing connection
        if (wsRef.current) {
            wsRef.current.close();
        }
        
        console.log(`[AGGrid] Connecting to WebSocket: ${websocketUrl}`);
        wsRef.current = new WebSocket(websocketUrl);
        
        wsRef.current.onopen = () => {
            console.log('[AGGrid] WebSocket connected');
        };
        
        wsRef.current.onmessage = (event) => {
            // Skip if auto-refresh is disabled
            if (!autoRefreshRef.current) return;
            
            try {
                const message = JSON.parse(event.data);
                
                if (message.type === 'snapshot') {
                    // Full data refresh
                    handleSnapshotUpdate(message.data);
                } else if (message.type === 'delta') {
                    // Incremental updates
                    handleDeltaUpdate(message.data);
                }
            } catch (err) {
                console.error('[AGGrid] Failed to process message:', err);
            }
        };
        
        wsRef.current.onclose = (event) => {
            console.log('[AGGrid] WebSocket closed, reconnecting in 2s...');
            reconnectTimeoutRef.current = setTimeout(connectWebSocket, 2000);
        };
        
        wsRef.current.onerror = (error) => {
            console.error('[AGGrid] WebSocket error:', error);
        };
    }, [websocketUrl]);
    
    // Connect on mount
    useEffect(() => {
        connectWebSocket();
        
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
        };
    }, [connectWebSocket]);
    
    // =========================================================================
    // DATA UPDATE HANDLERS
    // =========================================================================
    
    /**
     * Handle full snapshot update
     */
    const handleSnapshotUpdate = useCallback((data) => {
        const api = gridRef.current?.api;
        if (!api || !data) return;
        
        api.setGridOption('rowData', data);
    }, []);
    
    /**
     * Handle delta (incremental) updates
     * 
     * Each update: { id: string, changes: { field: value, ... } }
     */
    const handleDeltaUpdate = useCallback((updates) => {
        const api = gridRef.current?.api;
        if (!api || !updates || updates.length === 0) return;
        
        const rowUpdates = [];
        const cellsToFlash = [];
        
        updates.forEach(update => {
            const rowId = update.id;
            const rowNode = api.getRowNode(rowId);
            
            if (!rowNode) {
                // New row - add it
                rowUpdates.push({ add: [{ [rowIdField]: rowId, ...update.changes }] });
                return;
            }
            
            // Filter out fields being edited
            const editingFields = editingCellsRef.current;
            const fieldsToUpdate = Object.keys(update.changes || {}).filter(
                field => !editingFields.has(`${rowId}:${field}`)
            );
            
            if (fieldsToUpdate.length === 0) return;
            
            // Determine which cells changed (for flashing)
            fieldsToUpdate.forEach(field => {
                if (rowNode.data[field] !== update.changes[field]) {
                    cellsToFlash.push({ rowNode, columns: [field] });
                }
            });
            
            // Build updated row data
            const updatedData = {
                ...rowNode.data,
                ...Object.fromEntries(
                    fieldsToUpdate.map(f => [f, update.changes[f]])
                )
            };
            
            rowUpdates.push(updatedData);
        });
        
        // Batch apply updates
        if (rowUpdates.length > 0) {
            // Check if we have any add operations
            const addOps = rowUpdates.filter(u => u.add);
            const updateOps = rowUpdates.filter(u => !u.add);
            
            const transaction = {};
            if (addOps.length > 0) {
                transaction.add = addOps.flatMap(u => u.add);
            }
            if (updateOps.length > 0) {
                transaction.update = updateOps;
            }
            
            api.applyTransactionAsync(transaction, () => {
                // Flash cells after update completes
                cellsToFlash.forEach(({ rowNode, columns }) => {
                    api.flashCells({
                        rowNodes: [rowNode],
                        columns: columns,
                        flashDuration: 300,
                        fadeDuration: 500
                    });
                });
            });
        }
    }, [rowIdField]);
    
    // =========================================================================
    // EDIT MODE HANDLING
    // =========================================================================
    
    const handleCellEditingStarted = useCallback((params) => {
        const cellKey = `${params.data[rowIdField]}:${params.colDef.field}`;
        editingCellsRef.current.add(cellKey);
    }, [rowIdField]);
    
    const handleCellEditingStopped = useCallback((params) => {
        const cellKey = `${params.data[rowIdField]}:${params.colDef.field}`;
        editingCellsRef.current.delete(cellKey);
        
        // Notify Reflex if value changed
        if (params.valueChanged && onCellEdit) {
            onCellEdit({
                rowId: params.data[rowIdField],
                field: params.colDef.field,
                oldValue: params.oldValue,
                newValue: params.newValue,
                rowData: params.data
            });
        }
    }, [rowIdField, onCellEdit]);
    
    // =========================================================================
    // CONTEXT MENU
    // =========================================================================
    
    const getContextMenuItems = useCallback((params) => {
        // Notify Reflex of right-click
        if (onRowRightClick && params.node) {
            onRowRightClick(
                params.node.data[rowIdField],
                params.node.data,
                params.event?.clientX,
                params.event?.clientY
            );
        }
        
        return buildContextMenuItems(params, contextMenuItems);
    }, [rowIdField, onRowRightClick, contextMenuItems]);
    
    // =========================================================================
    // COLUMN STATE PERSISTENCE
    // =========================================================================
    
    const handleColumnStateChanged = useCallback(() => {
        const api = gridRef.current?.api;
        if (!api) return;
        
        // Debounce saves
        if (handleColumnStateChanged.timeout) {
            clearTimeout(handleColumnStateChanged.timeout);
        }
        handleColumnStateChanged.timeout = setTimeout(() => {
            saveColumnState(api, gridId);
        }, 500);
    }, [gridId]);
    
    // =========================================================================
    // GRID READY
    // =========================================================================
    
    const handleGridReady = useCallback((params) => {
        // Restore column state from localStorage
        restoreColumnState(params.api, gridId);
        
        // Notify Reflex
        if (onGridReady) {
            onGridReady();
        }
    }, [gridId, onGridReady]);
    
    // =========================================================================
    // SELECTION CHANGE
    // =========================================================================
    
    const handleSelectionChanged = useCallback((params) => {
        if (onSelectionChange) {
            const selectedRows = params.api.getSelectedRows();
            onSelectionChange(selectedRows);
        }
    }, [onSelectionChange]);
    
    // =========================================================================
    // GLOBAL CONTROLLER
    // =========================================================================
    
    useEffect(() => {
        window.gridController = {
            /**
             * Jump to and highlight a specific row
             */
            jumpToRow: (rowId) => {
                const api = gridRef.current?.api;
                if (!api) return;
                
                const rowNode = api.getRowNode(rowId);
                if (!rowNode) {
                    console.warn(`[AGGrid] Row not found: ${rowId}`);
                    return;
                }
                
                // Scroll row into view
                api.ensureNodeVisible(rowNode, 'middle');
                
                // Flash the row
                api.flashCells({
                    rowNodes: [rowNode],
                    flashDuration: 500,
                    fadeDuration: 1000
                });
                
                // Select the row temporarily
                rowNode.setSelected(true);
                setTimeout(() => {
                    rowNode.setSelected(false);
                }, 3000);
            },
            
            /**
             * Enable/disable auto-refresh
             */
            setAutoRefresh: (enabled) => {
                autoRefreshRef.current = enabled;
            },
            
            /**
             * Force refresh all cells
             */
            refresh: () => {
                gridRef.current?.api?.refreshCells({ force: true });
            },
            
            /**
             * Export to Excel
             */
            exportExcel: () => {
                gridRef.current?.api?.exportDataAsExcel({
                    fileName: `export_${new Date().toISOString().slice(0, 10)}.xlsx`
                });
            },
            
            /**
             * Export to CSV
             */
            exportCsv: () => {
                gridRef.current?.api?.exportDataAsCsv({
                    fileName: `export_${new Date().toISOString().slice(0, 10)}.csv`
                });
            },
            
            /**
             * Clear all filters
             */
            clearFilters: () => {
                gridRef.current?.api?.setFilterModel(null);
            },
            
            /**
             * Reset column state to defaults
             */
            resetColumnState: () => {
                const api = gridRef.current?.api;
                if (api) {
                    api.resetColumnState();
                    localStorage.removeItem(STORAGE_KEY);
                }
            },
            
            /**
             * Get currently selected rows
             */
            getSelectedRows: () => {
                return gridRef.current?.api?.getSelectedRows() || [];
            },
            
            /**
             * Programmatically select rows
             */
            selectRows: (rowIds) => {
                const api = gridRef.current?.api;
                if (!api) return;
                
                api.deselectAll();
                rowIds.forEach(id => {
                    const node = api.getRowNode(id);
                    if (node) node.setSelected(true);
                });
            },
            
            /**
             * Get grid API for advanced usage
             */
            getApi: () => gridRef.current?.api
        };
        
        return () => {
            window.gridController = null;
        };
    }, []);
    
    // =========================================================================
    // DEFAULT GRID OPTIONS
    // =========================================================================
    
    const defaultGridOptions = {
        // Row identification
        getRowId: (params) => String(params.data[rowIdField]),
        
        // Selection
        rowSelection: 'multiple',
        suppressRowClickSelection: false,
        
        // Grouping
        groupDefaultExpanded: 1,
        autoGroupColumnDef: {
            headerName: 'Group',
            minWidth: 200,
            cellRendererParams: {
                suppressCount: false
            }
        },
        
        // Performance optimizations
        animateRows: false,
        suppressRowVirtualisation: false,
        rowBuffer: 20,
        debounceVerticalScrollbar: true,
        
        // Enterprise features
        enableRangeSelection: true,
        enableRangeHandle: true,
        enableFillHandle: true,
        rowGroupPanelShow: 'onlyWhenGrouping',
        
        // Clipboard
        enableCellTextSelection: true,
        ensureDomOrder: true,
        
        // Suppress some default behaviors
        suppressCopyRowsToClipboard: false,
        suppressClipboardPaste: false,
        
        // Status bar (optional)
        statusBar: {
            statusPanels: [
                { statusPanel: 'agTotalRowCountComponent', align: 'left' },
                { statusPanel: 'agFilteredRowCountComponent', align: 'left' },
                { statusPanel: 'agSelectedRowCountComponent', align: 'center' },
                { statusPanel: 'agAggregationComponent', align: 'right' }
            ]
        }
    };
    
    // Merge with custom options
    const mergedGridOptions = {
        ...defaultGridOptions,
        ...gridOptions
    };
    
    // =========================================================================
    // RENDER
    // =========================================================================
    
    return (
        <div 
            className={theme}
            style={{ height, width }}
        >
            <AgGridReact
                ref={gridRef}
                columnDefs={processedColumnDefs}
                rowData={rowData}
                
                // Grid options
                {...mergedGridOptions}
                
                // Event handlers
                onGridReady={handleGridReady}
                onCellEditingStarted={handleCellEditingStarted}
                onCellEditingStopped={handleCellEditingStopped}
                onSelectionChanged={handleSelectionChanged}
                
                // Column state persistence
                onColumnMoved={handleColumnStateChanged}
                onColumnResized={handleColumnStateChanged}
                onColumnVisible={handleColumnStateChanged}
                onColumnPinned={handleColumnStateChanged}
                onSortChanged={handleColumnStateChanged}
                onFilterChanged={handleColumnStateChanged}
                
                // Context menu
                getContextMenuItems={getContextMenuItems}
            />
        </div>
    );
};

// Add custom CSS for cell states
const style = document.createElement('style');
style.textContent = `
    .ag-cell-flash {
        background-color: rgba(255, 215, 0, 0.3) !important;
        transition: background-color 0.5s ease-out;
    }
    
    .ag-cell-invalid {
        background-color: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid red !important;
    }
    
    .ag-cell-editing-protected {
        background-color: rgba(0, 100, 255, 0.1) !important;
    }
    
    /* Custom flash animation */
    @keyframes cellFlash {
        0% { background-color: rgba(255, 215, 0, 0.5); }
        100% { background-color: transparent; }
    }
`;
document.head.appendChild(style);

export default AGGridWrapper;
```

---

## 6. Python Backend Services

### 6.1 Tick Publisher Service

**File:** `services/tick_publisher.py`

```python
"""
WebSocket Tick Publisher Service

Handles:
- WebSocket connection management
- Delta computation (only send changed fields)
- Broadcasting to all connected clients
- Database polling at configurable intervals
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from fastapi import WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)


@dataclass
class TickPublisher:
    """
    Manages WebSocket connections and broadcasts tick data updates.
    
    Usage:
        publisher = TickPublisher(db_poll_interval=5)
        
        # In FastAPI route
        @app.websocket("/ws/ticks")
        async def websocket_endpoint(websocket: WebSocket):
            await publisher.connect(websocket)
            try:
                while True:
                    await websocket.receive_text()  # Keep alive
            except WebSocketDisconnect:
                publisher.disconnect(websocket)
    """
    
    db_poll_interval: float = 5.0
    """Interval in seconds between database polls."""
    
    row_id_field: str = "id"
    """Field name used as unique row identifier."""
    
    connections: list[WebSocket] = field(default_factory=list)
    """Active WebSocket connections."""
    
    last_snapshot: dict[str, dict] = field(default_factory=dict)
    """Last known state of all rows (for delta computation)."""
    
    validation_config: dict = field(default_factory=dict)
    """Validation rules loaded from config."""
    
    _running: bool = False
    """Internal flag for polling loop."""
    
    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept new WebSocket connection and send initial snapshot.
        
        Args:
            websocket: FastAPI WebSocket instance
        """
        await websocket.accept()
        self.connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.connections)}")
        
        # Send initial snapshot
        if self.last_snapshot:
            await websocket.send_json({
                "type": "snapshot",
                "data": list(self.last_snapshot.values()),
                "validation": self.validation_config,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove WebSocket from active connections.
        
        Args:
            websocket: WebSocket to remove
        """
        if websocket in self.connections:
            self.connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total connections: {len(self.connections)}")
    
    def compute_delta(self, new_data: list[dict]) -> list[dict]:
        """
        Compute changed fields between current and new data.
        
        Args:
            new_data: List of row dictionaries with current values
            
        Returns:
            List of delta objects: [{ id: str, changes: { field: value } }]
        """
        deltas = []
        new_ids = set()
        
        for row in new_data:
            row_id = str(row.get(self.row_id_field))
            new_ids.add(row_id)
            
            old_row = self.last_snapshot.get(row_id, {})
            changes = {}
            
            for field, value in row.items():
                if field != self.row_id_field and old_row.get(field) != value:
                    changes[field] = value
            
            if changes:
                deltas.append({
                    "id": row_id,
                    "changes": changes
                })
            
            # Update snapshot
            self.last_snapshot[row_id] = row
        
        # Handle removed rows (optional - uncomment if needed)
        # removed_ids = set(self.last_snapshot.keys()) - new_ids
        # for row_id in removed_ids:
        #     deltas.append({"id": row_id, "removed": True})
        #     del self.last_snapshot[row_id]
        
        return deltas
    
    async def broadcast_delta(self, deltas: list[dict]) -> None:
        """
        Broadcast delta updates to all connected clients.
        
        Args:
            deltas: List of delta objects to broadcast
        """
        if not deltas or not self.connections:
            return
        
        message = json.dumps({
            "type": "delta",
            "data": deltas,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Broadcast to all connections, handle failures gracefully
        disconnected = []
        for ws in self.connections:
            try:
                await ws.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to send to WebSocket: {e}")
                disconnected.append(ws)
        
        # Clean up disconnected
        for ws in disconnected:
            self.disconnect(ws)
    
    async def broadcast_snapshot(self, data: list[dict]) -> None:
        """
        Broadcast full snapshot to all connected clients.
        
        Args:
            data: Full dataset to broadcast
        """
        if not self.connections:
            return
        
        # Update internal snapshot
        self.last_snapshot = {
            str(row.get(self.row_id_field)): row 
            for row in data
        }
        
        message = json.dumps({
            "type": "snapshot",
            "data": data,
            "validation": self.validation_config,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        disconnected = []
        for ws in self.connections:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)
        
        for ws in disconnected:
            self.disconnect(ws)
    
    async def start_polling(
        self, 
        fetch_data: Callable[[], list[dict]],
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """
        Start polling database at configured interval.
        
        Args:
            fetch_data: Async function that returns list of row dicts
            on_error: Optional error callback
        """
        self._running = True
        logger.info(f"Starting tick publisher with {self.db_poll_interval}s interval")
        
        while self._running:
            try:
                # Fetch current data
                if asyncio.iscoroutinefunction(fetch_data):
                    new_data = await fetch_data()
                else:
                    new_data = fetch_data()
                
                # Compute and broadcast delta
                deltas = self.compute_delta(new_data)
                if deltas:
                    await self.broadcast_delta(deltas)
                    logger.debug(f"Broadcast {len(deltas)} updates")
                    
            except Exception as e:
                logger.error(f"Polling error: {e}")
                if on_error:
                    on_error(e)
            
            await asyncio.sleep(self.db_poll_interval)
    
    def stop(self) -> None:
        """Stop the polling loop."""
        self._running = False
        logger.info("Tick publisher stopped")
    
    def set_validation_config(self, config: dict) -> None:
        """
        Set validation configuration.
        
        Args:
            config: Validation rules dict
        """
        self.validation_config = config


# ============================================================================
# NOTIFICATION PUBLISHER
# ============================================================================

@dataclass
class NotificationPublisher:
    """
    Publishes notifications to connected clients.
    
    Can be used standalone or with TickPublisher.
    """
    
    tick_publisher: Optional[TickPublisher] = None
    """Associated tick publisher for broadcasting."""
    
    notification_handlers: list[Callable] = field(default_factory=list)
    """Callbacks for notification events."""
    
    async def publish(
        self,
        message: str,
        row_id: Optional[str] = None,
        notification_type: str = "info",
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Publish a notification to all clients.
        
        Args:
            message: Notification text
            row_id: Optional row ID for jump-to functionality
            notification_type: 'info' | 'warning' | 'error' | 'success'
            metadata: Additional data to include
            
        Returns:
            The created notification dict
        """
        notification = {
            "id": f"notif_{datetime.utcnow().timestamp()}",
            "message": message,
            "row_id": row_id,
            "type": notification_type,
            "timestamp": datetime.utcnow().isoformat(),
            **(metadata or {})
        }
        
        # Broadcast via tick publisher if available
        if self.tick_publisher and self.tick_publisher.connections:
            message_json = json.dumps({
                "type": "notification",
                "data": notification
            })
            
            for ws in self.tick_publisher.connections:
                try:
                    await ws.send_text(message_json)
                except Exception:
                    pass
        
        # Call registered handlers
        for handler in self.notification_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(notification)
                else:
                    handler(notification)
            except Exception as e:
                logger.error(f"Notification handler error: {e}")
        
        return notification
    
    def add_handler(self, handler: Callable) -> None:
        """Register a notification handler."""
        self.notification_handlers.append(handler)
```

### 6.2 Validation Loader

**File:** `services/validation_loader.py`

```python
"""
Validation Configuration Loader

Loads validation rules from .ini files for use in both
Python backend validation and frontend AG Grid validators.
"""

import configparser
from pathlib import Path
from typing import Any, Optional, Union
from dataclasses import dataclass
import json


@dataclass
class FieldValidation:
    """Validation rules for a single field."""
    
    field_name: str
    field_type: str = "str"
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None
    enum_values: Optional[list[str]] = None
    required: bool = False
    default: Optional[Any] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "type": self.field_type,
            "required": self.required
        }
        
        if self.min_value is not None:
            result["min"] = self.min_value
        if self.max_value is not None:
            result["max"] = self.max_value
        if self.pattern:
            result["pattern"] = self.pattern
        if self.enum_values:
            result["enum_values"] = self.enum_values
        if self.default is not None:
            result["default"] = self.default
        if self.error_message:
            result["error_message"] = self.error_message
            
        return result
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a value against this field's rules.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required check
        if self.required and (value is None or value == ""):
            return False, self.error_message or f"{self.field_name} is required"
        
        if value is None:
            return True, None
        
        # Type coercion and validation
        try:
            if self.field_type in ("int", "integer"):
                value = int(value)
            elif self.field_type in ("float", "number"):
                value = float(value)
            elif self.field_type in ("bool", "boolean"):
                value = bool(value)
        except (ValueError, TypeError):
            return False, f"{self.field_name} must be type {self.field_type}"
        
        # Range validation
        if self.min_value is not None and value < self.min_value:
            return False, self.error_message or f"{self.field_name} must be >= {self.min_value}"
        if self.max_value is not None and value > self.max_value:
            return False, self.error_message or f"{self.field_name} must be <= {self.max_value}"
        
        # Pattern validation
        if self.pattern:
            import re
            if not re.match(self.pattern, str(value)):
                return False, self.error_message or f"{self.field_name} doesn't match required format"
        
        # Enum validation
        if self.enum_values and value not in self.enum_values:
            return False, self.error_message or f"{self.field_name} must be one of: {', '.join(self.enum_values)}"
        
        return True, None


def load_validation_config(
    ini_path: Union[str, Path],
    encoding: str = "utf-8"
) -> dict[str, FieldValidation]:
    """
    Load validation configuration from .ini file.
    
    Args:
        ini_path: Path to .ini configuration file
        encoding: File encoding
        
    Returns:
        Dictionary mapping field names to FieldValidation objects
        
    Example .ini format:
        [price]
        type = int
        min = 0
        max = 1000000
        required = true
        
        [symbol]
        type = str
        pattern = ^[A-Z]{1,5}$
        
        [status]
        type = enum
        enum_values = Active,Pending,Cancelled
        default = Active
    """
    config = configparser.ConfigParser()
    config.read(ini_path, encoding=encoding)
    
    validations = {}
    
    for section in config.sections():
        field_name = section
        
        # Parse type
        field_type = config.get(section, "type", fallback="str")
        
        # Parse numeric constraints
        min_value = None
        max_value = None
        if config.has_option(section, "min"):
            min_value = config.getfloat(section, "min")
        if config.has_option(section, "max"):
            max_value = config.getfloat(section, "max")
        
        # Parse pattern
        pattern = config.get(section, "pattern", fallback=None)
        
        # Parse enum values
        enum_values = None
        if config.has_option(section, "enum_values"):
            enum_str = config.get(section, "enum_values")
            enum_values = [v.strip() for v in enum_str.split(",") if v.strip()]
        
        # Parse other options
        required = config.getboolean(section, "required", fallback=False)
        default = config.get(section, "default", fallback=None)
        error_message = config.get(section, "error_message", fallback=None)
        
        validations[field_name] = FieldValidation(
            field_name=field_name,
            field_type=field_type,
            min_value=min_value,
            max_value=max_value,
            pattern=pattern,
            enum_values=enum_values,
            required=required,
            default=default,
            error_message=error_message
        )
    
    return validations


def validation_config_to_dict(
    validations: dict[str, FieldValidation]
) -> dict[str, dict]:
    """
    Convert validation config to dictionary for JSON serialization.
    
    This format is passed to the frontend AG Grid component.
    """
    return {
        field_name: field_val.to_dict()
        for field_name, field_val in validations.items()
    }


def validate_row(
    row: dict,
    validations: dict[str, FieldValidation]
) -> tuple[bool, dict[str, str]]:
    """
    Validate an entire row against field rules.
    
    Returns:
        Tuple of (all_valid, errors_dict)
        errors_dict maps field names to error messages
    """
    errors = {}
    
    for field_name, field_val in validations.items():
        value = row.get(field_name)
        is_valid, error = field_val.validate(value)
        if not is_valid:
            errors[field_name] = error
    
    return len(errors) == 0, errors
```

### 6.3 Scheduled Refresh Service

**File:** `services/scheduled_refresh.py`

```python
"""
Scheduled Database Refresh Service

Provides timed refresh functionality to reload data from
database at specific times (e.g., market open/close).
"""

import asyncio
from datetime import datetime, time
from typing import Callable, Optional, Union
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ScheduleEntry:
    """A scheduled refresh entry."""
    
    hour: int
    minute: int
    action: str = "full_refresh"
    days: Optional[list[int]] = None  # 0=Monday, 6=Sunday, None=every day
    enabled: bool = True
    
    def matches(self, dt: datetime) -> bool:
        """Check if this schedule matches the given datetime."""
        if not self.enabled:
            return False
        if dt.hour != self.hour or dt.minute != self.minute:
            return False
        if self.days is not None and dt.weekday() not in self.days:
            return False
        return True


@dataclass
class ScheduledRefresh:
    """
    Manages scheduled data refresh times.
    
    Usage:
        scheduler = ScheduledRefresh()
        scheduler.add_schedule(hour=9, minute=30, action="full_refresh")  # Market open
        scheduler.add_schedule(hour=16, minute=0, action="full_refresh")   # Market close
        
        await scheduler.start(
            tick_publisher=publisher,
            fetch_data=my_fetch_function
        )
    """
    
    schedules: list[ScheduleEntry] = field(default_factory=list)
    """List of scheduled refresh times."""
    
    check_interval: int = 60
    """How often to check schedules (seconds)."""
    
    _running: bool = False
    _last_triggered: dict[str, datetime] = field(default_factory=dict)
    
    def add_schedule(
        self,
        hour: int,
        minute: int,
        action: str = "full_refresh",
        days: Optional[list[int]] = None
    ) -> None:
        """
        Add a scheduled refresh time.
        
        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
            action: Action type ('full_refresh', 'delta_refresh', etc.)
            days: List of weekdays (0=Mon, 6=Sun), None for every day
        """
        self.schedules.append(ScheduleEntry(
            hour=hour,
            minute=minute,
            action=action,
            days=days
        ))
        logger.info(f"Added schedule: {hour:02d}:{minute:02d} - {action}")
    
    def remove_schedule(self, hour: int, minute: int) -> bool:
        """Remove a scheduled refresh by time."""
        initial_count = len(self.schedules)
        self.schedules = [
            s for s in self.schedules 
            if not (s.hour == hour and s.minute == minute)
        ]
        return len(self.schedules) < initial_count
    
    def clear_schedules(self) -> None:
        """Remove all schedules."""
        self.schedules = []
    
    async def start(
        self,
        tick_publisher,  # TickPublisher instance
        fetch_data: Callable,
        on_refresh: Optional[Callable] = None
    ) -> None:
        """
        Start the scheduler loop.
        
        Args:
            tick_publisher: TickPublisher to broadcast updates
            fetch_data: Function to fetch fresh data
            on_refresh: Optional callback after refresh
        """
        self._running = True
        logger.info(f"Starting scheduler with {len(self.schedules)} schedules")
        
        while self._running:
            now = datetime.now()
            
            for schedule in self.schedules:
                if schedule.matches(now):
                    # Prevent duplicate triggers within same minute
                    key = f"{schedule.hour}:{schedule.minute}"
                    last = self._last_triggered.get(key)
                    if last and (now - last).total_seconds() < 120:
                        continue
                    
                    self._last_triggered[key] = now
                    logger.info(f"Triggering scheduled {schedule.action}")
                    
                    try:
                        # Fetch data
                        if asyncio.iscoroutinefunction(fetch_data):
                            data = await fetch_data()
                        else:
                            data = fetch_data()
                        
                        # Broadcast based on action type
                        if schedule.action == "full_refresh":
                            await tick_publisher.broadcast_snapshot(data)
                        else:
                            deltas = tick_publisher.compute_delta(data)
                            if deltas:
                                await tick_publisher.broadcast_delta(deltas)
                        
                        # Callback
                        if on_refresh:
                            if asyncio.iscoroutinefunction(on_refresh):
                                await on_refresh(schedule.action, data)
                            else:
                                on_refresh(schedule.action, data)
                                
                    except Exception as e:
                        logger.error(f"Scheduled refresh error: {e}")
            
            await asyncio.sleep(self.check_interval)
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        logger.info("Scheduler stopped")


def parse_schedule_config(config_str: str) -> list[dict]:
    """
    Parse schedule configuration string.
    
    Format: "HH:MM:action,HH:MM:action,..."
    Example: "09:30:full_refresh,16:00:full_refresh"
    
    Returns:
        List of schedule dicts
    """
    schedules = []
    
    for entry in config_str.split(","):
        entry = entry.strip()
        if not entry:
            continue
        
        parts = entry.split(":")
        if len(parts) >= 2:
            hour = int(parts[0])
            minute = int(parts[1])
            action = parts[2] if len(parts) > 2 else "full_refresh"
            
            schedules.append({
                "hour": hour,
                "minute": minute,
                "action": action
            })
    
    return schedules
```

---

## 7. Reflex Integration

### 7.1 FastAPI WebSocket Endpoint

**File:** Add to your Reflex app's `api.py` or equivalent:

```python
"""
FastAPI WebSocket endpoint for tick data.

This runs alongside the Reflex app.
"""

from fastapi import WebSocket, WebSocketDisconnect
from services.tick_publisher import TickPublisher, NotificationPublisher
from services.validation_loader import load_validation_config, validation_config_to_dict
from services.scheduled_refresh import ScheduledRefresh
import asyncio


# Initialize services
tick_publisher = TickPublisher(db_poll_interval=0.2)  # 200ms
notification_publisher = NotificationPublisher(tick_publisher=tick_publisher)
scheduler = ScheduledRefresh()

# Load validation config
validation_rules = load_validation_config("config/validation.ini")
tick_publisher.set_validation_config(validation_config_to_dict(validation_rules))


async def fetch_data_from_db():
    """
    Fetch current data from your database.
    Replace with your actual data fetching logic.
    """
    # Example - replace with real database query
    import random
    return [
        {
            "id": f"row_{i}",
            "symbol": random.choice(["AAPL", "GOOGL", "MSFT", "AMZN"]),
            "price": random.randint(100, 500),
            "quantity": random.randint(1, 1000),
            "status": random.choice(["Active", "Pending", "Cancelled"]),
            "is_active": random.choice([True, False])
        }
        for i in range(1000)
    ]


# WebSocket endpoint
async def websocket_ticks(websocket: WebSocket):
    """WebSocket endpoint for tick data."""
    await tick_publisher.connect(websocket)
    try:
        while True:
            # Keep connection alive, handle any client messages
            data = await websocket.receive_text()
            # Could handle commands here (e.g., subscribe/unsubscribe)
    except WebSocketDisconnect:
        tick_publisher.disconnect(websocket)


# Startup tasks
async def start_background_tasks():
    """Start background services."""
    # Start tick publisher polling
    asyncio.create_task(
        tick_publisher.start_polling(fetch_data_from_db)
    )
    
    # Add scheduled refreshes
    scheduler.add_schedule(hour=9, minute=30, action="full_refresh")  # Market open
    scheduler.add_schedule(hour=16, minute=0, action="full_refresh")   # Market close
    
    # Start scheduler
    asyncio.create_task(
        scheduler.start(
            tick_publisher=tick_publisher,
            fetch_data=fetch_data_from_db
        )
    )
```

### 7.2 Reflex App Integration

**File:** `app.py`

```python
"""
Main Reflex application with AG Grid integration.
"""

import reflex as rx
from components.ag_grid import ag_grid, AGGrid
from components.ag_grid_state import AGGridBaseState
from components.notification_panel import notification_panel
from services.validation_loader import load_validation_config, validation_config_to_dict


# ============================================================================
# APPLICATION STATE
# ============================================================================

class GridState(AGGridBaseState):
    """Application state extending base AG Grid state."""
    
    # Column definitions
    column_defs: list[dict] = [
        {
            "field": "id",
            "headerName": "ID",
            "type": "str",
            "editable": False,
            "pinned": "left",
            "width": 80
        },
        {
            "field": "symbol",
            "headerName": "Symbol",
            "type": "str",
            "rowGroup": True,  # Enable grouping by symbol
            "hide": True  # Hide when grouped
        },
        {
            "field": "price",
            "headerName": "Price",
            "type": "int",
            "editable": True,
            "aggFunc": "avg",  # Show average in group
            "cellStyle": {"textAlign": "right"}
        },
        {
            "field": "quantity",
            "headerName": "Qty",
            "type": "int",
            "editable": True,
            "aggFunc": "sum",  # Show sum in group
            "cellStyle": {"textAlign": "right"}
        },
        {
            "field": "status",
            "headerName": "Status",
            "type": "enum",
            "enumValues": ["Active", "Pending", "Cancelled"],
            "editable": True
        },
        {
            "field": "is_active",
            "headerName": "Active",
            "type": "bool",
            "editable": True
        }
    ]
    
    # Initial data (will be replaced by WebSocket snapshot)
    initial_data: list[dict] = []
    
    # WebSocket URL
    websocket_url: str = "ws://localhost:8000/ws/ticks"
    
    @rx.var
    def validation_config(self) -> dict:
        """Load validation config - computed var for reactivity."""
        try:
            rules = load_validation_config("config/validation.ini")
            return validation_config_to_dict(rules)
        except Exception:
            return {}
    
    # ===== Event Handlers =====
    
    async def handle_cell_edit(self, data: dict):
        """
        Handle cell edit from grid.
        
        Called when user finishes editing a cell.
        """
        row_id = data["rowId"]
        field = data["field"]
        old_value = data["oldValue"]
        new_value = data["newValue"]
        
        # TODO: Save to database
        print(f"Cell edited: {row_id}.{field} = {old_value} -> {new_value}")
        
        # Add notification
        self.add_notification(
            message=f"Updated {field}: {old_value} → {new_value}",
            row_id=row_id,
            notification_type="success"
        )
    
    def handle_right_click(self, row_id: str, row_data: dict, x: int, y: int):
        """Handle right-click on row (before context menu)."""
        print(f"Right-click on row: {row_id}")
    
    def handle_grid_ready(self):
        """Handle grid initialization."""
        print("Grid is ready")


# ============================================================================
# UI COMPONENTS
# ============================================================================

def toolbar() -> rx.Component:
    """Top toolbar with controls."""
    return rx.hstack(
        # Auto-refresh toggle
        rx.button(
            rx.cond(
                GridState.auto_refresh,
                rx.hstack(rx.icon("pause", size=16), rx.text("Pause Updates")),
                rx.hstack(rx.icon("play", size=16), rx.text("Resume Updates"))
            ),
            on_click=GridState.toggle_auto_refresh,
            variant="outline",
            color_scheme=rx.cond(GridState.auto_refresh, "green", "red"),
        ),
        
        rx.divider(orientation="vertical", height="24px"),
        
        # Export buttons
        rx.button(
            rx.hstack(rx.icon("file-spreadsheet", size=16), rx.text("Excel")),
            on_click=GridState.export_to_excel,
            variant="outline",
        ),
        rx.button(
            rx.hstack(rx.icon("file-text", size=16), rx.text("CSV")),
            on_click=GridState.export_to_csv,
            variant="outline",
        ),
        
        rx.divider(orientation="vertical", height="24px"),
        
        # Clear filters
        rx.button(
            rx.hstack(rx.icon("filter-x", size=16), rx.text("Clear Filters")),
            on_click=GridState.clear_filters,
            variant="outline",
        ),
        
        # Reset columns
        rx.button(
            rx.hstack(rx.icon("columns", size=16), rx.text("Reset Columns")),
            on_click=GridState.reset_column_state,
            variant="outline",
        ),
        
        rx.spacer(),
        
        # Connection status indicator
        rx.badge(
            "Live",
            color_scheme="green",
            variant="solid",
        ),
        
        padding="3",
        width="100%",
        bg="gray.900",
        border_bottom="1px solid",
        border_color="gray.700",
    )


def main_grid() -> rx.Component:
    """Main AG Grid component."""
    return rx.box(
        ag_grid(
            column_defs=GridState.column_defs,
            row_data=GridState.initial_data,
            websocket_url=GridState.websocket_url,
            validation_config=GridState.validation_config,
            auto_refresh=GridState.auto_refresh,
            grid_id="main_grid",
            theme="ag-theme-balham-dark",
            height="calc(100vh - 50px)",
            width="100%",
            on_cell_edit=GridState.handle_cell_edit,
            on_row_right_click=GridState.handle_right_click,
            on_selection_change=GridState.handle_selection_change,
            on_grid_ready=GridState.handle_grid_ready,
        ),
        width="100%",
        height="calc(100vh - 50px)",
    )


def index() -> rx.Component:
    """Main page."""
    return rx.box(
        toolbar(),
        rx.hstack(
            main_grid(),
            notification_panel(
                state=GridState,
                width="320px",
                position="right"
            ),
            width="100%",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        bg="gray.950",
    )


# ============================================================================
# APP SETUP
# ============================================================================

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
    )
)
app.add_page(index)
```

---

## 8. Configuration Formats

### 8.1 Validation Config (.ini)

**File:** `config/validation.ini`

```ini
# Field Validation Configuration
# 
# Each section defines validation rules for a field.
# 
# Supported options:
#   type          - Data type: str, int, float, bool, enum, date
#   min           - Minimum value (for numeric types)
#   max           - Maximum value (for numeric types)
#   pattern       - Regex pattern (for string types)
#   enum_values   - Comma-separated list of allowed values
#   required      - Whether field is required (true/false)
#   default       - Default value
#   error_message - Custom error message

[id]
type = str
required = true
pattern = ^[a-zA-Z0-9_-]+$
error_message = ID must be alphanumeric with underscores/hyphens only

[price]
type = int
min = 0
max = 1000000
required = true
error_message = Price must be between 0 and 1,000,000

[quantity]
type = int
min = 1
max = 100000
required = true
error_message = Quantity must be between 1 and 100,000

[symbol]
type = str
pattern = ^[A-Z]{1,5}$
required = true
error_message = Symbol must be 1-5 uppercase letters

[status]
type = enum
enum_values = Active,Pending,Cancelled
default = Active

[is_active]
type = bool
default = true

[email]
type = str
pattern = ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$
error_message = Invalid email format

[percentage]
type = float
min = 0
max = 100
error_message = Percentage must be between 0 and 100
```

### 8.2 Schedule Config

**File:** `config/schedules.ini`

```ini
# Scheduled Refresh Configuration
#
# Format: HH:MM:action
# Actions: full_refresh, delta_refresh

[schedules]
# Market hours (EST)
entries = 09:30:full_refresh,12:00:delta_refresh,16:00:full_refresh

# Or define individually:
[market_open]
hour = 9
minute = 30
action = full_refresh
days = 0,1,2,3,4  # Mon-Fri

[market_close]
hour = 16
minute = 0
action = full_refresh
days = 0,1,2,3,4  # Mon-Fri

[midday_refresh]
hour = 12
minute = 0
action = delta_refresh
days = 0,1,2,3,4
```

---

## 9. API Reference

### 9.1 JavaScript Global Controller

Available via `window.gridController` after grid initialization:

| Method | Parameters | Description |
|--------|------------|-------------|
| `jumpToRow(rowId)` | `rowId: string` | Scroll to row, flash, and highlight |
| `setAutoRefresh(enabled)` | `enabled: boolean` | Enable/disable WebSocket updates |
| `refresh()` | - | Force refresh all cells |
| `exportExcel()` | - | Export to Excel file |
| `exportCsv()` | - | Export to CSV file |
| `clearFilters()` | - | Clear all column filters |
| `resetColumnState()` | - | Reset columns to default |
| `getSelectedRows()` | - | Returns array of selected row data |
| `selectRows(rowIds)` | `rowIds: string[]` | Programmatically select rows |
| `getApi()` | - | Get AG Grid API for advanced usage |

### 9.2 WebSocket Message Format

**Server → Client:**

```typescript
// Full snapshot
{
    type: "snapshot",
    data: Array<RowData>,
    validation: ValidationConfig,
    timestamp: string  // ISO format
}

// Delta update
{
    type: "delta",
    data: Array<{
        id: string,
        changes: Record<string, any>
    }>,
    timestamp: string
}

// Notification
{
    type: "notification",
    data: {
        id: string,
        message: string,
        row_id?: string,
        type: "info" | "warning" | "error" | "success",
        timestamp: string
    }
}
```

### 9.3 Column Definition Extended Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | 'str', 'int', 'float', 'bool', 'enum', 'date' |
| `enumValues` | string[] | Allowed values for enum type |
| `validation` | object | { min, max, pattern, required } |
| `rowGroup` | boolean | Enable grouping by this column |
| `aggFunc` | string | Aggregation: 'sum', 'avg', 'count', 'min', 'max' |

---

## 10. Usage Examples

### 10.1 Basic Grid

```python
import reflex as rx
from components.ag_grid import ag_grid
from components.ag_grid_state import AGGridBaseState

class BasicState(AGGridBaseState):
    column_defs = [
        {"field": "id", "headerName": "ID"},
        {"field": "name", "headerName": "Name", "editable": True},
        {"field": "value", "headerName": "Value", "type": "int", "editable": True}
    ]
    initial_data = []

def index():
    return ag_grid(
        column_defs=BasicState.column_defs,
        row_data=BasicState.initial_data,
        websocket_url="ws://localhost:8000/ws/ticks",
        on_cell_edit=BasicState.handle_cell_edit
    )
```

### 10.2 Grouped Grid with Aggregation

```python
class GroupedState(AGGridBaseState):
    column_defs = [
        {
            "field": "category",
            "headerName": "Category",
            "rowGroup": True,
            "hide": True
        },
        {
            "field": "product",
            "headerName": "Product"
        },
        {
            "field": "sales",
            "headerName": "Sales",
            "type": "int",
            "aggFunc": "sum"  # Sum in group rows
        },
        {
            "field": "price",
            "headerName": "Avg Price",
            "type": "float",
            "aggFunc": "avg"  # Average in group rows
        }
    ]
```

### 10.3 Publishing Notifications

```python
from services.tick_publisher import NotificationPublisher

notification_publisher = NotificationPublisher(tick_publisher=tick_publisher)

# Publish notification with row link
await notification_publisher.publish(
    message="Price alert: AAPL exceeded $200",
    row_id="row_42",
    notification_type="warning"
)
```

---

## 11. Performance Guidelines

### 11.1 Critical Optimizations

1. **Never route tick data through Reflex state** - Use dedicated WebSocket directly to AG Grid JS API

2. **Batch updates** - Collect all changes within a tick window and apply via `applyTransactionAsync`

3. **Delta only** - Only send changed fields, not full rows

4. **Skip edited cells** - Track cells being edited and exclude from updates

5. **Debounce state saves** - Don't save localStorage on every micro-change

### 11.2 AG Grid Performance Settings

```javascript
// In grid options
{
    animateRows: false,              // Disable row animations
    suppressRowVirtualisation: false, // Keep virtualisation on
    rowBuffer: 20,                   // Rows to render outside viewport
    debounceVerticalScrollbar: true, // Smooth scrolling
}
```

### 11.3 Data Volume Guidelines

| Rows | Update Frequency | Recommended Approach |
|------|------------------|---------------------|
| <1000 | Any | Standard delta updates |
| 1000-5000 | <500ms | Delta + batch transactions |
| 5000-10000 | <1s | Delta + viewport-only updates |
| >10000 | Any | Server-side row model |

---

## 12. Testing Requirements

### 12.1 Unit Tests

```python
# tests/test_validation.py
from services.validation_loader import load_validation_config, FieldValidation

def test_load_validation_config():
    config = load_validation_config("config/validation.ini")
    assert "price" in config
    assert config["price"].field_type == "int"
    assert config["price"].min_value == 0

def test_field_validation():
    field = FieldValidation(
        field_name="price",
        field_type="int",
        min_value=0,
        max_value=100
    )
    assert field.validate(50) == (True, None)
    assert field.validate(-1)[0] == False
    assert field.validate(101)[0] == False
```

### 12.2 Integration Tests

```python
# tests/test_websocket.py
import pytest
from fastapi.testclient import TestClient

def test_websocket_connection(client):
    with client.websocket_connect("/ws/ticks") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "snapshot"
        assert "data" in data
```

### 12.3 E2E Test Cases

1. **Grid loads with initial data**
2. **WebSocket updates flash cells**
3. **Cell edit pauses updates for that cell**
4. **Right-click shows context menu**
5. **Copy cell copies to clipboard**
6. **Export to Excel downloads file**
7. **Column resize persists after refresh**
8. **Notification click jumps to row**
9. **Grouping shows aggregated values**
10. **Validation prevents invalid input**

---

## Appendix A: Dependencies

### Python
```
reflex>=0.4.0
fastapi>=0.100.0
websockets>=11.0
configparser>=5.0
```

### JavaScript (package.json)
```json
{
  "dependencies": {
    "ag-grid-react": "^31.0.0",
    "ag-grid-enterprise": "^31.0.0",
    "ag-grid-community": "^31.0.0",
    "react": "^18.2.0"
  }
}
```

---

## Appendix B: AG Grid Enterprise Features Used

| Feature | License Required | Alternative |
|---------|------------------|-------------|
| Row Grouping | Enterprise | Manual grouping UI |
| Aggregation | Enterprise | Compute in backend |
| Excel Export | Enterprise | CSV export (Community) |
| Context Menu | Enterprise | Custom right-click handler |
| Range Selection | Enterprise | Single cell selection |
| Clipboard | Enterprise | Manual copy implementation |

Note: AG Grid Enterprise shows a watermark without license but is fully functional.

---

## Implementation Checklist

- [ ] Set up project structure
- [ ] Implement AG Grid JS wrapper
- [ ] Create Reflex custom component
- [ ] Implement TickPublisher service
- [ ] Implement validation loader
- [ ] Implement scheduled refresh
- [ ] Create FastAPI WebSocket endpoint
- [ ] Integrate with Reflex app
- [ ] Add notification panel UI
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Performance testing with 1000 rows @ 200ms
- [ ] Documentation

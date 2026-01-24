"""
AG Grid Custom Component for Reflex

This module defines the Reflex wrapper around AG Grid Enterprise.
Uses NoSSRComponent since AG Grid requires browser APIs.

ARCHITECTURAL PATTERNS:
- Function Registry: Formatters/renderers are string keys, not Python functions
- Event Sanitization: All events received are pre-sanitized by JS wrapper
- Pydantic Models: Column definitions use ColumnDef Pydantic models
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import reflex as rx
from reflex.components.component import NoSSRComponent
from reflex.vars import Var

from reflex_ag_grid.models.column_def import ColumnDef, column_defs_to_ag_grid
from reflex_ag_grid.models.validation import ValidationSchema


class AGGrid(NoSSRComponent):
    """
    Custom AG Grid Enterprise wrapper component for Reflex.

    This component renders AG Grid with Enterprise features including:
    - Context menu with copy/export
    - Range selection
    - Row grouping and aggregation
    - Excel export
    - Column state persistence

    IMPORTANT: Event handlers receive sanitized data dicts, not raw AG Grid events.

    Props:
        column_defs: List of column definitions (ColumnDef models or dicts)
        row_data: List of row data dictionaries
        row_id_field: Field name to use as unique row identifier (default: "id")
        validation_config: ValidationSchema for field validation
        grid_options: Additional AG Grid options to merge
        theme: AG Grid theme class (default: "ag-theme-balham-dark")
        height: Grid height (default: "100%")
        width: Grid width (default: "100%")
        grid_id: Unique identifier for this grid instance
        license_key: AG Grid Enterprise license key

    Events:
        on_cell_edit: Fired with {rowId, field, oldValue, newValue, rowData}
        on_row_click: Fired with {rowId, rowData}
        on_row_double_click: Fired with {rowId, rowData}
        on_row_right_click: Fired with {rowId, rowData, clientX, clientY}
        on_selection_change: Fired with {selectedRows, selectedCount}
        on_grid_ready: Fired with {gridId}

    Example:
        AGGrid.create(
            column_defs=[
                ColumnDef(field="name", header_name="Name"),
                ColumnDef(field="price", type="number", formatter="currency"),
            ],
            row_data=State.data,
            on_cell_edit=State.handle_edit,
        )
    """

    # Library path - relative to static folder
    library = "../../reflex_ag_grid/static/ag_grid_wrapper.js"
    tag = "AGGridWrapper"  # Must match the exported component name

    # Disable SSR - AG Grid requires browser APIs
    is_default = True

    # CRITICAL: Define dependencies here. Reflex handles the install.
    # This replaces manual package.json editing.
    lib_dependencies: list[str] = [
        "ag-grid-react@31.3.0",
        "ag-grid-community@31.3.0",
        "ag-grid-enterprise@31.3.0",
    ]

    # ===== Props =====

    column_defs: Var[List[Dict[str, Any]]]
    """
    Column definitions in AG Grid format.
    Use ColumnDef.to_ag_grid_def() or column_defs_to_ag_grid() to convert.
    
    Registry keys (resolved in JS):
    - _formatter: string key for valueFormatter
    - _renderer: string key for cellRenderer
    - _cellClassRules: string key for cellClassRules
    - _type: column type for editor selection
    - _validation: inline validation rules
    """

    row_data: Var[List[Dict[str, Any]]]
    """Row data. Each row MUST have a unique identifier field."""

    row_id_field: Var[str] = "id"  # type: ignore
    """Field name to use as unique row identifier."""

    validation_config: Var[Dict[str, Dict[str, Any]]] = {}  # type: ignore
    """
    Validation rules per field from ValidationSchema.to_js_config().
    Format: { field_name: { type, min, max, pattern, required, ... } }
    """

    grid_options: Var[Dict[str, Any]] = {}  # type: ignore
    """Additional AG Grid options to merge with defaults."""

    theme: Var[str] = "ag-theme-balham-dark"  # type: ignore
    """AG Grid theme class name."""

    height: Var[str] = "100%"  # type: ignore
    """Grid container height."""

    width: Var[str] = "100%"  # type: ignore
    """Grid container width."""

    grid_id: Var[str] = "default"  # type: ignore
    """Unique identifier for this grid (used for state persistence)."""

    license_key: Var[Optional[str]] = None  # type: ignore
    """AG Grid Enterprise license key. Can also be set via window.AG_GRID_LICENSE_KEY."""

    context_menu_items: Var[List[str]] = []  # type: ignore
    """Custom context menu item keys (resolved via registry)."""

    # ===== Event Handlers =====
    # All events receive SANITIZED data - no circular references

    on_cell_edit: rx.EventHandler[lambda data: [data]]
    """
    Fired when cell edit is completed with value change.
    Payload: { rowId: str, field: str, oldValue: Any, newValue: Any, rowData: dict }
    """

    on_row_click: rx.EventHandler[lambda data: [data]]
    """
    Fired when row is clicked.
    Payload: { rowId: str, rowData: dict }
    """

    on_row_double_click: rx.EventHandler[lambda data: [data]]
    """
    Fired when row is double-clicked.
    Payload: { rowId: str, rowData: dict }
    """

    on_row_right_click: rx.EventHandler[lambda data: [data]]
    """
    Fired on row right-click (before context menu appears).
    Payload: { rowId: str, rowData: dict, clientX: int, clientY: int }
    """

    on_selection_change: rx.EventHandler[lambda data: [data]]
    """
    Fired when row selection changes.
    Payload: { selectedRows: list[dict], selectedCount: int }
    """

    on_grid_ready: rx.EventHandler[lambda data: [data]]
    """
    Fired when grid is fully initialized.
    Payload: { gridId: str }
    """

    @classmethod
    def create(
        cls,
        column_defs: Union[List[ColumnDef], List[Dict[str, Any]], Var],
        row_data: Union[List[Dict[str, Any]], Var],
        validation_schema: Optional[ValidationSchema] = None,
        **props,
    ) -> "AGGrid":
        """
        Create an AGGrid component instance.

        Args:
            column_defs: Column definitions (ColumnDef list, dict list, or Var)
            row_data: Row data (list of dicts or Var)
            validation_schema: Optional Pydantic validation schema
            **props: Additional component props

        Returns:
            AGGrid component instance
        """
        # Convert ColumnDef models to AG Grid format if needed
        if isinstance(column_defs, list) and len(column_defs) > 0:
            if isinstance(column_defs[0], ColumnDef):
                column_defs = column_defs_to_ag_grid(column_defs)  # type: ignore

        # Convert ValidationSchema to JS config if provided
        if validation_schema:
            props["validation_config"] = validation_schema.to_js_config()

        # Set column_defs
        props["column_defs"] = column_defs
        props["row_data"] = row_data

        return super().create(**props)

    def _get_imports(self) -> dict:
        """Get the JS imports for this component."""
        return {}

    def _get_custom_code(self) -> Optional[str]:
        """Custom code to inject."""
        return None


def ag_grid(
    column_defs: Union[List[ColumnDef], List[Dict[str, Any]], Var],
    row_data: Union[List[Dict[str, Any]], Var],
    validation_schema: Optional[ValidationSchema] = None,
    **props,
) -> AGGrid:
    """
    Convenience function to create an AG Grid component.

    Args:
        column_defs: Column definitions
        row_data: Row data
        validation_schema: Optional validation schema
        **props: Additional props

    Returns:
        AGGrid component

    Example:
        ag_grid(
            column_defs=[
                ColumnDef(field="id", header_name="ID"),
                ColumnDef(field="price", type="number", editable=True),
            ],
            row_data=State.items,
            on_cell_edit=State.handle_edit,
            height="600px",
        )
    """
    return AGGrid.create(
        column_defs=column_defs,
        row_data=row_data,
        validation_schema=validation_schema,
        **props,
    )

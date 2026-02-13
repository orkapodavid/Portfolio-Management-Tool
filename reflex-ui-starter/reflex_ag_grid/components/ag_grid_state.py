"""
AG Grid State Mixin for Reflex

Provides a mixin class with common AG Grid functionality that can be
combined with any Reflex State class.

Usage:
    class MyState(rx.State, AGGridStateMixin):
        data: list[dict] = []

        def on_cell_edit(self, data: dict):
            row_id = data.get("rowId")
            field = data.get("field")
            new_value = data.get("newValue")
            # Update your data...
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import reflex as rx


class AGGridStateMixin:
    """
    Mixin class providing common AG Grid state and functionality.

    Combine with rx.State to get AG Grid helpers:

        class MyGridState(rx.State, AGGridStateMixin):
            items: list[dict] = []

    Provides:
    - Grid control methods via rx.call_script
    - Common event handlers you can override
    - Utility methods for row data management

    All grid control methods use the gridId to target specific grids
    when multiple grids are on the same page.
    """

    # -------------------------------------------------------------------------
    # State Variables
    # -------------------------------------------------------------------------

    selected_rows: List[Dict[str, Any]] = []
    """Currently selected rows (updated via on_selection_change)."""

    # -------------------------------------------------------------------------
    # Grid Control Methods
    # These use rx.call_script to call the JavaScript gridController
    # -------------------------------------------------------------------------

    def jump_to_row(self, row_id: str, grid_id: str = "default") -> rx.event.EventSpec:
        """
        Scroll to and highlight a specific row.

        Args:
            row_id: The row ID to jump to
            grid_id: Grid identifier (for multi-grid pages)

        Returns:
            EventSpec to execute the JavaScript call

        Example:
            def on_notification_click(self, notification: dict):
                return self.jump_to_row(notification["row_id"], "my_grid")
        """
        return rx.call_script(
            f"window.gridControllers?.['{grid_id}']?.jumpToRow('{row_id}')"
        )

    def refresh_grid(self, grid_id: str = "default") -> rx.event.EventSpec:
        """
        Force refresh all cells in the grid.

        Example:
            def on_data_updated(self):
                return self.refresh_grid("my_grid")
        """
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.refresh()")

    def export_to_excel(self, grid_id: str = "default") -> rx.event.EventSpec:
        """
        Trigger Excel export (Enterprise feature).

        Example:
            rx.button("Export Excel", on_click=State.export_to_excel("my_grid"))
        """
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.exportExcel()")

    def export_to_csv(self, grid_id: str = "default") -> rx.event.EventSpec:
        """
        Trigger CSV export.

        Example:
            rx.button("Export CSV", on_click=State.export_to_csv("my_grid"))
        """
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.exportCsv()")

    def clear_filters(self, grid_id: str = "default") -> rx.event.EventSpec:
        """Clear all column filters."""
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.clearFilters()")

    def reset_column_state(self, grid_id: str = "default") -> rx.event.EventSpec:
        """Reset columns to default state (width, order, visibility)."""
        return rx.call_script(
            f"window.gridControllers?.['{grid_id}']?.resetColumnState()"
        )

    def select_rows(
        self, row_ids: List[str], grid_id: str = "default"
    ) -> rx.event.EventSpec:
        """
        Programmatically select specific rows by ID.

        Args:
            row_ids: List of row IDs to select
            grid_id: Grid identifier
        """
        ids_json = str(row_ids)
        return rx.call_script(
            f"window.gridControllers?.['{grid_id}']?.selectRows({ids_json})"
        )

    # -------------------------------------------------------------------------
    # Event Handlers
    # Override these in your State class for custom behavior
    # -------------------------------------------------------------------------

    def handle_cell_edit(self, data: Dict[str, Any]) -> None:
        """
        Handle cell edit event.

        Override in your State to implement save logic.

        Args:
            data: Sanitized event data:
                - rowId: str
                - field: str
                - oldValue: Any
                - newValue: Any
                - rowData: dict

        Example:
            def handle_cell_edit(self, data: dict):
                row_id = data.get("rowId")
                field = data.get("field")
                new_value = data.get("newValue")
                self.update_row_data("items", row_id, {field: new_value})
        """
        row_id = data.get("rowId", "")
        field = data.get("field", "")
        old_value = data.get("oldValue")
        new_value = data.get("newValue")
        print(f"[AGGrid] Cell edited: {row_id}.{field} = {old_value} → {new_value}")

    def handle_selection_change(self, data: Dict[str, Any]) -> None:
        """
        Handle row selection change.

        Args:
            data: Sanitized event data:
                - selectedRows: list[dict]
                - selectedCount: int
        """
        self.selected_rows = data.get("selectedRows", [])

    def handle_row_click(self, data: Dict[str, Any]) -> None:
        """
        Handle row click event.

        Args:
            data: Sanitized event data:
                - rowId: str
                - rowData: dict
        """
        pass  # Override in subclass

    def handle_row_double_click(self, data: Dict[str, Any]) -> None:
        """
        Handle row double-click event.

        Args:
            data: Sanitized event data:
                - rowId: str
                - rowData: dict
        """
        pass  # Override in subclass

    def handle_row_right_click(self, data: Dict[str, Any]) -> None:
        """
        Handle row right-click (before context menu).

        Args:
            data: Sanitized event data:
                - rowId: str
                - rowData: dict
                - clientX: int
                - clientY: int
        """
        pass  # Override in subclass

    def handle_grid_ready(self, data: Dict[str, Any]) -> None:
        """
        Handle grid initialization complete.

        Args:
            data: Event data:
                - gridId: str
        """
        grid_id = data.get("gridId", "default")
        print(f"[AGGrid] Grid ready: {grid_id}")

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def update_row_data(
        self,
        data_attr: str,
        row_id: str,
        updates: Dict[str, Any],
        id_field: str = "id",
    ) -> None:
        """
        Update a specific row in a data list by ID.

        This is a helper for updating state after cell edits.

        Args:
            data_attr: Name of the state attribute containing the data list
            row_id: The row ID to update
            updates: Dict of field -> new value
            id_field: Name of the ID field in row data (default: "id")

        Example:
            # Update price for row "row_123"
            self.update_row_data("items", "row_123", {"price": 99.99})

            # Using a different ID field
            self.update_row_data("orders", "ORD001", {"status": "shipped"}, id_field="order_id")
        """
        data_list = getattr(self, data_attr, [])
        updated = False

        for i, row in enumerate(data_list):
            if str(row.get(id_field)) == str(row_id):
                data_list[i] = {**row, **updates}
                updated = True
                break

        if updated:
            # Trigger Reflex reactivity by creating a new list
            setattr(self, data_attr, data_list.copy())

    def get_row_by_id(
        self,
        data_attr: str,
        row_id: str,
        id_field: str = "id",
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific row from a data list by ID.

        Args:
            data_attr: Name of the state attribute containing the data list
            row_id: The row ID to find
            id_field: Name of the ID field in row data (default: "id")

        Returns:
            The row dict if found, None otherwise

        Example:
            row = self.get_row_by_id("items", "row_123")
            if row:
                print(f"Found: {row['name']}")
        """
        data_list = getattr(self, data_attr, [])

        for row in data_list:
            if str(row.get(id_field)) == str(row_id):
                return row

        return None

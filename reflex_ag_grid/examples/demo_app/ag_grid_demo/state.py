"""
Demo App State - Manages application state for all demo pages.

Contains DemoState class with:
- Row selection tracking
- Streaming data updates
- Notification management
- Cross-page navigation support
"""

import random

import reflex as rx

from .data import SAMPLE_DATA


class DemoState(rx.State):
    """Demo application state.

    Manages:
    - Grid data and selection
    - Streaming updates with pause-on-edit
    - Notification list with jump-to-row
    - Cross-page navigation highlighting
    """

    # Core data
    data: list[dict] = SAMPLE_DATA
    selected_rows: list[dict] = []
    last_event: str = "None"

    # Notifications
    notifications: list[dict] = []

    # Streaming control
    is_streaming: bool = False
    pause_on_edit: bool = False
    is_editing: bool = False

    # Search
    search_text: str = ""

    # Cross-page navigation support
    pending_highlight: dict = {}  # {grid_id, row_id, field?, style?}

    # =========================================================================
    # Event Handlers - Selection
    # =========================================================================

    def on_selection_change(self, rows: list, source: str, event_type: str):
        """Handle row selection changes."""
        self.selected_rows = rows if isinstance(rows, list) else []
        self.last_event = f"Selection: {len(self.selected_rows)} rows ({source})"

    def on_cell_click(self, event: dict):
        """Handle cell clicks."""
        row_index = event.get("rowIndex", "?")
        field = event.get("colDef", {}).get("field", "?")
        self.last_event = f"Cell click: row {row_index}, field {field}"

    # =========================================================================
    # Event Handlers - Editing
    # =========================================================================

    def on_cell_edit(self, row_index: int, field: str, new_value: str):
        """Handle cell value changes (Req 7 - validation feedback)."""
        if field == "price":
            try:
                val = float(new_value)
                if val < 0:
                    self.last_event = "❌ Validation error: Price cannot be negative"
                    return
            except ValueError:
                self.last_event = "❌ Validation error: Invalid price value"
                return

        self.last_event = f"✅ Cell edit: row {row_index}, {field} = {new_value}"
        if 0 <= row_index < len(self.data):
            self.data[row_index][field] = new_value

    def on_editing_started(self, row_index: int, field: str):
        """Track when editing starts (Req 12) - automatically pauses updates."""
        self.is_editing = True
        self.pause_on_edit = True
        self.last_event = f"✏️ Editing row {row_index}, field: {field}"

    def on_editing_stopped(self, row_index: int, field: str):
        """Track when editing stops - keeps updates paused until manual resume."""
        self.is_editing = False
        # DON'T auto-resume: pause_on_edit stays True until user clicks Resume
        self.last_event = (
            f"✅ Finished editing row {row_index}. Click Resume to continue updates."
        )

    def resume_updates(self):
        """Manually resume updates after editing (Req 12)."""
        self.pause_on_edit = False
        self.last_event = "▶️ Updates resumed"

    # =========================================================================
    # Notifications
    # =========================================================================

    def add_notification(self, message: str, row_id: str, level: str = "info"):
        """Add a notification (Req 6)."""
        self.notifications = [
            {
                "id": len(self.notifications),
                "message": message,
                "row_id": row_id,
                "level": level,
            }
        ] + self.notifications[:4]  # Keep last 5

    def clear_notifications(self):
        """Clear all notifications."""
        self.notifications = []

    # =========================================================================
    # Streaming
    # =========================================================================

    def simulate_price_update(self):
        """Simulate streaming price update (Req 10, 14)."""
        if self.pause_on_edit:
            return  # Skip update while paused (Req 12 - manual resume)

        idx = random.randint(0, len(self.data) - 1)
        old_price = self.data[idx]["price"]
        change = random.uniform(-5, 5)
        new_price = round(old_price + change, 2)

        self.data[idx]["price"] = new_price
        self.data[idx]["change"] = round(change, 2)

        if abs(change) > 3:
            level = "warning" if change < 0 else "success"
            self.add_notification(
                f"{self.data[idx]['symbol']}: ${old_price:.2f} → ${new_price:.2f}",
                self.data[idx]["id"],
                level,
            )

    def toggle_streaming(self):
        """Toggle streaming updates."""
        self.is_streaming = not self.is_streaming

    def toggle_pause_on_edit(self):
        """Toggle pause on edit mode."""
        self.pause_on_edit = not self.pause_on_edit

    # =========================================================================
    # Row Manipulation (Req 13 - Transaction API)
    # =========================================================================

    def add_row(self):
        """Add a new row to the grid (Req 13)."""
        new_id = f"row_{len(self.data) + 1}"
        new_row = {
            "id": new_id,
            "symbol": "NEW",
            "company": "New Company",
            "sector": "Technology",
            "price": 100.0,
            "qty": 0,
            "change": 0.0,
            "active": True,
        }
        self.data = self.data + [new_row]
        self.last_event = f"➕ Added new row: {new_id}"

    def remove_last_row(self):
        """Remove the last row from the grid (Req 13)."""
        if len(self.data) > 0:
            removed = self.data[-1]
            self.data = self.data[:-1]
            self.last_event = f"➖ Removed row: {removed.get('id', 'unknown')}"
        else:
            self.last_event = "⚠️ No rows to remove"

    # =========================================================================
    # Jump to Row / Cross-Page Navigation
    # =========================================================================

    def jump_to_row(self, row_id: str):
        """Jump to a row and flash it. Tries multiple grids."""
        script = f"""
        (() => {{
            // Try multiple possible grid refs
            const gridIds = ['notifications_grid', 'streaming_grid', 'flash_grid'];
            for (const gridId of gridIds) {{
                const gridRef = refs['ref_' + gridId];
                if (gridRef && gridRef.current && gridRef.current.api) {{
                    const api = gridRef.current.api;
                    const node = api.getRowNode('{row_id}');
                    if (node) {{
                        api.ensureNodeVisible(node, 'middle');
                        api.flashCells({{rowNodes: [node]}});
                        console.log('Jumped to row:', '{row_id}', 'in grid:', gridId);
                        return;
                    }}
                }}
            }}
            console.warn('Row not found in any grid:', '{row_id}');
        }})()
        """
        return rx.call_script(script)

    def navigate_and_highlight(self, route: str, grid_id: str, row_id: str):
        """Navigate to a page and highlight a specific row."""
        self.pending_highlight = {
            "grid_id": grid_id,
            "row_id": row_id,
        }
        return rx.redirect(route)

    def execute_pending_highlight(self, grid_id: str):
        """Execute pending highlight for a grid (called on grid ready)."""
        if not self.pending_highlight:
            return
        if self.pending_highlight.get("grid_id") != grid_id:
            return
        row_id = self.pending_highlight.get("row_id", "")
        self.pending_highlight = {}
        script = f"""
        (() => {{
            const gridRef = refs['ref_{grid_id}'];
            if (gridRef && gridRef.current && gridRef.current.api) {{
                const api = gridRef.current.api;
                const node = api.getRowNode('{row_id}');
                if (node) {{
                    api.ensureNodeVisible(node, 'middle');
                    api.flashCells({{rowNodes: [node]}});
                    console.log('Cross-page jump to row:', '{row_id}');
                }} else {{
                    console.warn('Row not found:', '{row_id}');
                }}
            }} else {{
                console.warn('Grid API not available for:', '{grid_id}');
            }}
        }})()
        """
        return rx.call_script(script)

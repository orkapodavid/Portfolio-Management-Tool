"""
21 - CRUD Data Source Page - Demonstrates Pandas-backed CRUD operations.

Requirement 21: CRUD Data Source with Mock API
AG Grid Feature: Data source pattern with add/update/delete
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..components import nav_bar


# Mock database as Pandas-like list
INITIAL_DATA = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "department": "Engineering",
        "salary": 95000,
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "department": "Marketing",
        "salary": 75000,
    },
    {
        "id": 3,
        "name": "Carol White",
        "email": "carol@example.com",
        "department": "Engineering",
        "salary": 105000,
    },
    {
        "id": 4,
        "name": "David Brown",
        "email": "david@example.com",
        "department": "Sales",
        "salary": 85000,
    },
    {
        "id": 5,
        "name": "Eve Davis",
        "email": "eve@example.com",
        "department": "HR",
        "salary": 70000,
    },
]


class CrudState(rx.State):
    """State for CRUD demo."""

    data: list[dict] = INITIAL_DATA
    next_id: int = 6
    last_action: str = "Ready"

    def add_row(self):
        """Create a new row."""
        new_row = {
            "id": self.next_id,
            "name": "New Employee",
            "email": f"new{self.next_id}@example.com",
            "department": "Unassigned",
            "salary": 50000,
        }
        self.data = self.data + [new_row]
        self.last_action = f"✅ Created row {self.next_id}"
        self.next_id += 1

    def on_cell_edit(self, row_id: str, field: str, value):
        """Update a cell value (triggered by inline editing)."""
        row_id_int = int(row_id)
        for i, row in enumerate(self.data):
            if row.get("id") == row_id_int:
                self.data[i][field] = value
                self.last_action = f"✏️ Updated row {row_id}: {field} = {value}"
                break

    def delete_last(self):
        """Delete the last row."""
        if len(self.data) > 0:
            deleted = self.data[-1]
            self.data = self.data[:-1]
            self.last_action = f"🗑️ Deleted: {deleted.get('name', 'Unknown')}"
        else:
            self.last_action = "⚠️ No rows to delete"

    def reset_data(self):
        """Reset to initial data."""
        self.data = INITIAL_DATA.copy()
        self.next_id = 6
        self.last_action = "🔄 Reset to initial data"


def crud_data_source_page() -> rx.Component:
    """CRUD Data Source demo page.

    Features:
    - Create new rows
    - Read data with inline editing
    - Update cells via double-click edit
    - Delete rows
    - Reset to initial state
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("21 - CRUD Data Source", size="6"),
        rx.text("Complete Create, Read, Update, Delete operations"),
        rx.callout(
            "Full CRUD operations: Click 'Add Row' to create, double-click cells to edit, "
            "and 'Delete Last' to remove. All changes update the in-memory data store.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "➕ Add Row",
                on_click=CrudState.add_row,
                color_scheme="green",
            ),
            rx.button(
                "🗑️ Delete Last",
                on_click=CrudState.delete_last,
                color_scheme="red",
            ),
            rx.button(
                "🔄 Reset",
                on_click=CrudState.reset_data,
                color_scheme="gray",
            ),
            rx.badge(CrudState.last_action, color_scheme="blue"),
            spacing="3",
        ),
        ag_grid(
            id="crud_grid",
            row_data=CrudState.data,
            column_defs=[
                {"field": "id", "headerName": "ID", "width": 70, "editable": False},
                {"field": "name", "headerName": "Name", "editable": True, "flex": 1},
                {"field": "email", "headerName": "Email", "editable": True, "flex": 1},
                {
                    "field": "department",
                    "headerName": "Dept",
                    "editable": True,
                    "cellEditor": "agSelectCellEditor",
                    "cellEditorParams": {
                        "values": [
                            "Engineering",
                            "Marketing",
                            "Sales",
                            "HR",
                            "Finance",
                            "Unassigned",
                        ]
                    },
                    "width": 130,
                },
                {
                    "field": "salary",
                    "headerName": "Salary",
                    "editable": True,
                    "width": 100,
                },
            ],
            row_id_key="id",
            on_cell_value_changed=CrudState.on_cell_edit,
            enable_cell_change_flash=True,
            theme="quartz",
            width="90vw",
            height="50vh",
        ),
        rx.box(
            rx.heading("CRUD Pattern:", size="4"),
            rx.code_block(
                """# Create
def add_row(self):
    self.data = self.data + [new_row]

# Update (triggered by on_cell_edit)
def on_cell_edit(self, row_id, field, value):
    self.data[idx][field] = value

# Delete
def delete_last(self):
    self.data = self.data[:-1]""",
                language="python",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )

"""
17 - Tree Data Page - Demonstrates hierarchical data structure.

Requirement 17: Tree Data / Hierarchical Structure
AG Grid Feature: treeData + getDataPath
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..components import nav_bar, status_badge


# Sample hierarchical folder/file data
TREE_DATA = [
    {
        "id": "1",
        "path": ["Documents"],
        "name": "Documents",
        "size": None,
        "type": "folder",
    },
    {
        "id": "2",
        "path": ["Documents", "Reports"],
        "name": "Reports",
        "size": None,
        "type": "folder",
    },
    {
        "id": "3",
        "path": ["Documents", "Reports", "Q1_2024.xlsx"],
        "name": "Q1_2024.xlsx",
        "size": 1024,
        "type": "file",
    },
    {
        "id": "4",
        "path": ["Documents", "Reports", "Q2_2024.xlsx"],
        "name": "Q2_2024.xlsx",
        "size": 2048,
        "type": "file",
    },
    {
        "id": "5",
        "path": ["Documents", "Reports", "Q3_2024.xlsx"],
        "name": "Q3_2024.xlsx",
        "size": 1536,
        "type": "file",
    },
    {
        "id": "6",
        "path": ["Documents", "Images"],
        "name": "Images",
        "size": None,
        "type": "folder",
    },
    {
        "id": "7",
        "path": ["Documents", "Images", "logo.png"],
        "name": "logo.png",
        "size": 512,
        "type": "file",
    },
    {
        "id": "8",
        "path": ["Downloads"],
        "name": "Downloads",
        "size": None,
        "type": "folder",
    },
    {
        "id": "9",
        "path": ["Downloads", "installer.exe"],
        "name": "installer.exe",
        "size": 52428800,
        "type": "file",
    },
]


class TreeDataState(rx.State):
    """State for tree data demo."""

    data: list[dict] = TREE_DATA
    last_event: str = "None"

    def on_row_click(self, event: dict):
        """Handle row clicks."""
        row_data = event.get("data", {})
        self.last_event = (
            f"Clicked: {row_data.get('name', '?')} ({row_data.get('type', '?')})"
        )


def format_size(size) -> str:
    """Format file size for display."""
    if size is None:
        return "—"
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size // 1024} KB"
    else:
        return f"{size // (1024 * 1024)} MB"


def tree_data_page() -> rx.Component:
    """Tree Data demo page.

    Features:
    - Hierarchical file/folder structure
    - Expand/collapse nodes
    - Path-based grouping
    - Custom icons for folders vs files
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("17 - Tree Data", size="6"),
        rx.text("Hierarchical data structure with expand/collapse"),
        rx.callout(
            "Tree Data displays hierarchical relationships. Click the expand arrows "
            "to navigate the folder structure. AG Grid uses getDataPath to build the tree.",
            icon="info",
        ),
        status_badge(),
        rx.text(f"Last Event: {TreeDataState.last_event}", size="2"),
        ag_grid(
            id="tree_data_grid",
            row_data=TreeDataState.data,
            column_defs=[
                {"field": "name", "headerName": "Name", "flex": 2},
                {"field": "type", "headerName": "Type", "width": 100},
                {"field": "size", "headerName": "Size", "width": 120},
            ],
            row_id_key="id",
            tree_data=True,
            get_data_path=rx.Var("(data) => data.path"),
            auto_group_column_def={
                "headerName": "File Explorer",
                "minWidth": 300,
                "cellRendererParams": {
                    "suppressCount": True,
                },
            },
            group_default_expanded=-1,  # Expand all by default
            on_row_clicked=TreeDataState.on_row_click,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.box(
            rx.heading("Data Structure:", size="4"),
            rx.code_block(
                """# Each row has a 'path' array defining its location in the tree
TREE_DATA = [
    {"id": "1", "path": ["Documents"], "name": "Documents", "type": "folder"},
    {"id": "2", "path": ["Documents", "Reports"], "name": "Reports", "type": "folder"},
    {"id": "3", "path": ["Documents", "Reports", "Q1.xlsx"], "name": "Q1.xlsx", "type": "file"},
]

# AG Grid config
ag_grid(
    tree_data=True,
    get_data_path=rx.Var("(data) => data.path"),
)""",
                language="python",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )

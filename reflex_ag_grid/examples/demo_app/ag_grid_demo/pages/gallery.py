"""
Example Gallery Page - Visual index of AG Grid features.
"""

import reflex as rx
from ..components import nav_bar


def feature_card(
    title: str, description: str, route: str, icon: str, color: str
) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon(tag=icon, size=24, color=color),
                    rx.heading(title, size="3"),
                    align="center",
                    spacing="2",
                ),
                rx.text(description, size="1", color="gray"),
                align_items="start",
                spacing="2",
                height="100%",
            ),
            _hover={"transform": "translateY(-2px)", "box_shadow": "lg"},
            transition="all 0.2s",
            height="120px",
        ),
        href=route,
        text_decoration="none",
        width="100%",
    )


def gallery_page() -> rx.Component:
    return rx.vstack(
        nav_bar(),
        rx.heading("Example Gallery", size="7", margin_bottom="2"),
        rx.text(
            "Comprehensive showcase of Reflex AG Grid Enterprise features.",
            margin_bottom="6",
            color="gray",
        ),
        rx.grid(
            # Req 1: Context Menu
            feature_card(
                "01 - Context Menu",
                "Custom right-click menu actions.",
                "/01-context-menu",
                "mouse-pointer-2",
                "blue",
            ),
            # Req 2: Range Selection
            feature_card(
                "02 - Range Selection",
                "Select and aggregate cell ranges.",
                "/02-range-selection",
                "box-select",
                "indigo",
            ),
            # Req 3: Cell Flash
            feature_card(
                "03 - Cell Flash",
                "Visual feedback for value changes.",
                "/03-cell-flash",
                "zap",
                "amber",
            ),
            # Req 4: Jump & Highlight
            feature_card(
                "04 - Jump & Highlight",
                "Cross-component navigation.",
                "/04-jump-highlight",
                "arrow-right-circle",
                "orange",
            ),
            # Req 5: Grouping
            feature_card(
                "05 - Grouping",
                "Row grouping and aggregation.",
                "/05-grouping",
                "layers",
                "purple",
            ),
            # Req 6: Notifications
            feature_card(
                "06 - Notifications",
                "Event-driven notification system.",
                "/06-notifications",
                "bell",
                "red",
            ),
            # Req 7: Validation
            feature_card(
                "07 - Validation",
                "Schema-based input validation.",
                "/07-validation",
                "shield-check",
                "green",
            ),
            # Req 8: Clipboard
            feature_card(
                "08 - Clipboard",
                "Copy/paste with Excel compatibility.",
                "/08-clipboard",
                "clipboard",
                "cyan",
            ),
            # Req 9: Excel Export
            feature_card(
                "09 - Excel Export",
                "Native Excel export with styles.",
                "/09-excel-export",
                "file-spreadsheet",
                "teal",
            ),
            # Req 10: WebSocket
            feature_card(
                "10 - WebSocket",
                "Real-time streaming updates.",
                "/10-websocket",
                "radio",
                "pink",
            ),
            # Req 11: Cell Editors
            feature_card(
                "11 - Cell Editors",
                "Rich editors (select, date, etc).",
                "/11-cell-editors",
                "pen-tool",
                "violet",
            ),
            # Req 12: Edit Pause
            feature_card(
                "12 - Edit Pause",
                "Pause updates while editing.",
                "/12-edit-pause",
                "pause-circle",
                "slate",
            ),
            # Req 13: Transaction API
            feature_card(
                "13 - Transaction API",
                "Fast delta updates for large data.",
                "/13-transaction-api",
                "arrow-left-right",
                "emerald",
            ),
            # Req 14: Background Tasks
            feature_card(
                "14 - Background Tasks",
                "Running tasks affecting grid state.",
                "/14-background-tasks",
                "activity",
                "rose",
            ),
            # Req 15: Column State
            feature_card(
                "15 - Column State",
                "Save/restore column layout.",
                "/15-column-state",
                "layout-grid",
                "blue",
            ),
            # Req 16: Cell Renderers
            feature_card(
                "16 - Cell Renderers",
                "Custom cell styling & formatting.",
                "/16-cell-renderers",
                "palette",
                "fuchsia",
            ),
            # Req 17: Tree Data
            feature_card(
                "17 - Tree Data",
                "Hierarchical data with expand/collapse.",
                "/17-tree-data",
                "folder-tree",
                "teal",
            ),
            # Req 18: Performance Testing
            feature_card(
                "18 - Performance",
                "1000+ row stress test with virtual scroll.",
                "/18-perf-test",
                "gauge",
                "orange",
            ),
            # Req 19: Status Bar
            feature_card(
                "19 - Status Bar",
                "Row counts and aggregations.",
                "/19-status-bar",
                "bar-chart-2",
                "cyan",
            ),
            # Req 20: Overlays
            feature_card(
                "20 - Overlays",
                "Loading and no-rows overlays.",
                "/20-overlays",
                "loader-2",
                "pink",
            ),
            # Req 21: CRUD Data Source
            feature_card(
                "21 - CRUD",
                "Create, Read, Update, Delete operations.",
                "/21-crud",
                "database",
                "lime",
            ),
            # Phase 3 Features (v35)
            feature_card(
                "22 - Advanced Filter",
                "Enterprise filter builder UI.",
                "/22-advanced-filter",
                "filter",
                "violet",
            ),
            feature_card(
                "23 - Set Filter",
                "Multi-select checkbox filtering.",
                "/23-set-filter",
                "check-square",
                "emerald",
            ),
            feature_card(
                "24 - Multi Filter",
                "Combined filter types.",
                "/24-multi-filter",
                "list-filter",
                "amber",
            ),
            feature_card(
                "25 - Row Numbers",
                "Automatic row numbering column.",
                "/25-row-numbers",
                "hash",
                "slate",
            ),
            columns="3",  # 3 columns layout
            spacing="4",
            width="100%",
        ),
        padding="6",
        max_width="1200px",
        margin="0 auto",
    )

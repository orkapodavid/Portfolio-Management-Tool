"""
Navigation Bar Component - Top navigation for all 25 demo pages.
"""

import reflex as rx


def nav_bar() -> rx.Component:
    """Navigation bar for demo pages.

    Links to all 25 demo pages (one per requirement).
    """
    return rx.box(
        rx.hstack(
            rx.text("AG Grid Demo", weight="bold", size="3"),
            rx.divider(orientation="vertical", size="2"),
            rx.scroll_area(
                rx.hstack(
                    rx.link("Gallery", href="/", size="1", weight="bold"),
                    rx.link("01-Menu", href="/01-context-menu", size="1"),
                    rx.link("02-Range", href="/02-range-selection", size="1"),
                    rx.link("03-Flash", href="/03-cell-flash", size="1"),
                    rx.link("04-Jump", href="/04-jump-highlight", size="1"),
                    rx.link("05-Group", href="/05-grouping", size="1"),
                    rx.link("06-Notify", href="/06-notifications", size="1"),
                    rx.link("07-Valid", href="/07-validation", size="1"),
                    rx.link("08-Copy", href="/08-clipboard", size="1"),
                    rx.link("09-Export", href="/09-excel-export", size="1"),
                    rx.link("10-WS", href="/10-websocket", size="1"),
                    rx.link("11-Edit", href="/11-cell-editors", size="1"),
                    rx.link("12-Pause", href="/12-edit-pause", size="1"),
                    rx.link("13-Trans", href="/13-transaction-api", size="1"),
                    rx.link("14-Tasks", href="/14-background-tasks", size="1"),
                    rx.link("15-State", href="/15-column-state", size="1"),
                    rx.link("16-Render", href="/16-cell-renderers", size="1"),
                    rx.link("17-Tree", href="/17-tree-data", size="1"),
                    rx.link("18-Perf", href="/18-perf-test", size="1"),
                    rx.link("19-Status", href="/19-status-bar", size="1"),
                    rx.link("20-Overlay", href="/20-overlays", size="1"),
                    rx.link("21-CRUD", href="/21-crud", size="1"),
                    # Phase 3 (v35)
                    rx.link("22-Filter", href="/22-advanced-filter", size="1"),
                    rx.link("23-Set", href="/23-set-filter", size="1"),
                    rx.link("24-Multi", href="/24-multi-filter", size="1"),
                    rx.link("25-RowNum", href="/25-row-numbers", size="1"),
                    rx.link("26-Search", href="/26-quick-filter", size="1"),
                    spacing="3",
                ),
                type="scroll",
                scrollbars="horizontal",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        padding="2",
        background="var(--gray-2)",
        width="100%",
    )

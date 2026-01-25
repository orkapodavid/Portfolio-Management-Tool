"""
AG Grid Demo App - Multi-page demo showcasing all AG Grid features.

This is the main app file that imports from modular components:
- state.py: DemoState class
- data.py: Sample data and validation schema
- columns.py: Column definitions
- components/: Shared UI components
- pages/: All demo pages

Demonstrates all 15 requirements from the AG Grid Traceability Matrix.
"""

import reflex as rx

from .pages import (
    index,
    editable_page,
    grouped_page,
    streaming_page,
    range_page,
    column_state_page,
    search_page,
    validation_page,
    jump_demo_page,
)


# =============================================================================
# APP
# =============================================================================

app = rx.App()
app.add_page(index, route="/", title="Basic Grid")
app.add_page(editable_page, route="/editable", title="Editable Grid")
app.add_page(grouped_page, route="/grouped", title="Grouped Grid")
app.add_page(streaming_page, route="/streaming", title="Streaming Data")
app.add_page(range_page, route="/range", title="Range Selection")
app.add_page(column_state_page, route="/column-state", title="Column State")
app.add_page(search_page, route="/search", title="Global Search")
app.add_page(validation_page, route="/validation", title="Validation Demo")
app.add_page(jump_demo_page, route="/jump-demo", title="Cross-Page Jump")

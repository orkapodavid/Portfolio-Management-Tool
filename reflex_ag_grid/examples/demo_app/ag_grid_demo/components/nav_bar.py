"""
Navigation Bar Component - Top navigation for all demo pages.
"""

import reflex as rx


def nav_bar() -> rx.Component:
    """Navigation bar for demo pages.

    Links to all demo pages:
    - Basic, Editable, Validation, Grouped
    - Streaming, Range Select, Column State
    - Search, Jump Demo
    """
    return rx.hstack(
        rx.link("Basic", href="/"),
        rx.link("Editable", href="/editable"),
        rx.link("Validation", href="/validation"),
        rx.link("Grouped", href="/grouped"),
        rx.link("Streaming", href="/streaming"),
        rx.link("Range Select", href="/range"),
        rx.link("Column State", href="/column-state"),
        rx.link("Search", href="/search"),
        rx.link("Jump Demo", href="/jump-demo"),
        spacing="4",
        padding="3",
        background="var(--gray-2)",
        width="100%",
    )

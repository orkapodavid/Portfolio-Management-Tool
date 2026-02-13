"""
Demo App Column Definitions - Column configurations for all grid types.

Contains:
- get_basic_columns(): Basic sortable/filterable columns
- get_editable_columns(): Columns with various cell editors
- get_grouped_columns(): Columns with grouping and aggregation
"""

from reflex_ag_grid import ag_grid

from .data import SECTORS


def get_basic_columns():
    """Basic column definitions with sorting and filtering."""
    return [
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol",
            sortable=True,
            filter="agTextColumnFilter",
        ),
        ag_grid.column_def(field="company", header_name="Company", flex=1),
        ag_grid.column_def(
            field="sector", header_name="Sector", filter="agSetColumnFilter"
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            sortable=True,
            filter="agNumberColumnFilter",
        ),
        ag_grid.column_def(field="qty", header_name="Quantity", sortable=True),
        ag_grid.column_def(field="change", header_name="Change %", sortable=True),
    ]


def get_editable_columns():
    """Columns with different cell editors (Req 11).

    Demonstrates:
    - Text editing (company)
    - Select dropdown (sector)
    - Number editor (price)
    - Checkbox editor (active)
    """
    return [
        ag_grid.column_def(field="symbol", header_name="Symbol", editable=False),
        ag_grid.column_def(field="company", header_name="Company", editable=True),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            editable=True,
            cell_editor="agSelectCellEditor",
            cell_editor_params={"values": SECTORS},
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            editable=True,
            cell_editor="agNumberCellEditor",
        ),
        ag_grid.column_def(field="qty", header_name="Quantity", editable=True),
        ag_grid.column_def(
            field="active",
            header_name="Active",
            editable=True,
            cell_editor="agCheckboxCellEditor",
            cell_renderer="agCheckboxCellRenderer",
        ),
    ]


def get_grouped_columns():
    """Columns with grouping support (Req 5).

    Demonstrates:
    - Row grouping by sector
    - Aggregation functions (avg, sum)
    """
    return [
        ag_grid.column_def(
            field="sector", header_name="Sector", row_group=True, hide=True
        ),
        ag_grid.column_def(field="symbol", header_name="Symbol", sortable=True),
        ag_grid.column_def(field="company", header_name="Company", flex=1),
        ag_grid.column_def(field="price", header_name="Price", agg_func="avg"),
        ag_grid.column_def(field="qty", header_name="Quantity", agg_func="sum"),
        ag_grid.column_def(field="change", header_name="Change %", agg_func="avg"),
    ]

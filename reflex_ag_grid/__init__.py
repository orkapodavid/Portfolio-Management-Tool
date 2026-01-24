"""
Reflex AG Grid Enterprise Wrapper

A generic, reusable AG Grid Enterprise wrapper for Reflex Python applications.
Designed to be copyable between repositories as a local package.

Usage:
    from reflex_ag_grid import AGGrid, AGGridStateMixin
    from reflex_ag_grid.models import ColumnDef, ValidationSchema

Example:
    class MyState(rx.State, AGGridStateMixin):
        data: list[dict] = []

    def my_grid():
        return AGGrid.create(
            column_defs=[
                ColumnDef(field="name", header_name="Name"),
                ColumnDef(field="price", header_name="Price", type="number"),
            ],
            row_data=MyState.data,
            on_cell_edit=MyState.handle_cell_edit,
        )
"""

from reflex_ag_grid.components.ag_grid import AGGrid, ag_grid
from reflex_ag_grid.components.ag_grid_state import AGGridStateMixin
from reflex_ag_grid.models import ColumnDef, ValidationSchema, FieldValidation

__all__ = [
    "AGGrid",
    "ag_grid",
    "AGGridStateMixin",
    "ColumnDef",
    "ValidationSchema",
    "FieldValidation",
]

__version__ = "0.1.0"

"""
AG Grid Component for Reflex

This module provides a comprehensive AG Grid Enterprise wrapper for Reflex Python.

Main exports:
- ag_grid: Namespace providing clean API (ag_grid(...), ag_grid.column_def(...))
- AgGrid: Core component class
- ColumnDef: Column definition model
- AGFilters, AGEditors: Constants for filter/editor types

Usage:
    from reflex_ag_grid import ag_grid

    ag_grid(
        id="my_grid",
        row_data=State.data,
        column_defs=[
            ag_grid.column_def(field="name", header_name="Name"),
            ag_grid.column_def(field="price", editable=True),
        ],
        theme="quartz",
    )
"""

from types import SimpleNamespace
from typing import Any, Literal

import reflex as rx
from pydantic import BaseModel
from reflex.components.el import Div
from reflex.components.props import PropsBase


# =============================================================================
# EVENT SANITIZATION HELPERS
# =============================================================================


def callback_content(iterable: list[str]) -> str:
    """Join JS expressions with semicolons for arrow callback body."""
    return "; ".join(iterable)


def arrow_callback(js_expr: str | list[str]) -> rx.Var:
    """
    Create an arrow callback that executes JS expressions.

    Args:
        js_expr: Single JS expression or list of expressions

    Returns:
        rx.Var containing the IIFE callback
    """
    if isinstance(js_expr, list):
        js_expr = callback_content(js_expr)
    return rx.Var(f"(() => {{{js_expr}}})()")


def exclude_non_serializable_keys(
    event: rx.Var,
    exclude_keys: list[str],
) -> list[str]:
    """
    Create JS expressions to exclude non-serializable keys from an event object.

    AG Grid event objects contain circular references (api, node, etc.) that
    cannot be serialized to JSON. This function creates JS that destructures
    the event and returns only the serializable properties.

    Args:
        event: The event variable to destructure
        exclude_keys: List of property names to exclude

    Returns:
        JS expressions for destructuring and returning clean object
    """
    exclude_keys_str = ", ".join(exclude_keys)
    return [
        f"let {{{exclude_keys_str}, ...rest}} = {event}",
        "return rest",
    ]


# =============================================================================
# EVENT SPEC FUNCTIONS
# These define how AG Grid events are transformed before being sent to Python
# =============================================================================

# Keys that contain circular references and cannot be serialized
_CELL_EVENT_EXCLUDE_KEYS = [
    "context",
    "api",
    "columnApi",
    "column",
    "node",
    "event",
    "eventPath",
]
_ROW_EVENT_EXCLUDE_KEYS = ["context", "api", "source", "node", "event", "eventPath"]


def _on_cell_event_spec(event: rx.Var) -> list[rx.Var]:
    """Event spec for cell events - removes non-serializable AG Grid objects."""
    return [
        arrow_callback(exclude_non_serializable_keys(event, _CELL_EVENT_EXCLUDE_KEYS))
    ]


def _on_row_event_spec(event: rx.Var) -> list[rx.Var]:
    """Event spec for row events - removes non-serializable AG Grid objects."""
    return [
        arrow_callback(exclude_non_serializable_keys(event, _ROW_EVENT_EXCLUDE_KEYS))
    ]


def _on_cell_value_changed(event: rx.Var) -> list[rx.Var]:
    """
    Event spec for cell value changes.

    Returns: [rowIndex, field, newValue]
    """
    return [
        rx.Var(f"(() => {{let {{rowIndex, ...rest}} = {event}; return rowIndex}})()"),
        rx.Var(f"(() => {{let {{colDef, ...rest}} = {event}; return colDef.field}})()"),
        rx.Var(f"(() => {{let {{newValue, ...rest}} = {event}; return newValue}})()"),
    ]


def _on_selection_change_signature(event: rx.Var) -> list[rx.Var]:
    """
    Event spec for selection changes.

    Returns: [selectedRows, source, type]
    """
    return [
        rx.Var(f"{event}.api.getSelectedRows()"),
        rx.Var(f"{event}.source"),
        rx.Var(f"{event}.type"),
    ]


def _on_cell_editing_spec(event: rx.Var) -> list[rx.Var]:
    """
    Event spec for cell editing started/stopped.

    Returns: [rowIndex, field]
    """
    return [
        rx.Var(f"(() => {{let {{rowIndex, ...rest}} = {event}; return rowIndex}})()"),
        rx.Var(
            f"(() => {{let {{colDef, ...rest}} = {event}; return colDef?.field || null}})()"
        ),
    ]


# =============================================================================
# AG GRID CONSTANTS
# =============================================================================


class AGFilters(SimpleNamespace):
    """
    Available AG Grid filter types.

    Usage:
        ag_grid.column_def(field="name", filter=AGFilters.text)
    """

    text = "agTextColumnFilter"
    number = "agNumberColumnFilter"
    date = "agDateColumnFilter"
    set = "agSetColumnFilter"  # Enterprise
    multi = "agMultiColumnFilter"  # Enterprise


class AGEditors(SimpleNamespace):
    """
    Available AG Grid cell editor types.

    Usage:
        ag_grid.column_def(field="status", cell_editor=AGEditors.select,
                          cell_editor_params={"values": ["A", "B", "C"]})
    """

    text = "agTextCellEditor"
    large_text = "agLargeTextCellEditor"
    select = "agSelectCellEditor"
    rich_select = "agRichSelectCellEditor"  # Enterprise
    number = "agNumberCellEditor"
    date = "agDateCellEditor"
    checkbox = "agCheckboxCellEditor"


# =============================================================================
# COLUMN DEFINITION MODELS
# =============================================================================


class ColumnDef(PropsBase):
    """
    AG Grid column definition with automatic camelCase conversion.

    Usage:
        ag_grid.column_def(
            field="price",
            header_name="Price",
            editable=True,
            filter=AGFilters.number,
        )
    """

    # Required
    field: str | rx.Var[str]

    # Identity
    col_id: str | rx.Var[str] | None = None
    type: str | rx.Var[str] | None = None

    # Display
    header_name: str | rx.Var[str] | None = None
    header_tooltip: str | rx.Var[str] | None = None
    hide: bool | rx.Var[bool] = False

    # Editing
    editable: bool | rx.Var[bool] = False
    cell_editor: str | rx.Var[str] | None = None
    cell_editor_params: dict[str, list[Any]] | rx.Var[dict[str, list[Any]]] | None = (
        None
    )

    # Filtering
    filter: str | rx.Var[str] | None = None
    floating_filter: bool | rx.Var[bool] = False

    # Rendering
    value_formatter: rx.Var | None = None
    cell_renderer: rx.Var | None = None
    checkbox_selection: bool | rx.Var[bool] = False

    # Styling (conditional cell styling)
    # cell_style: JS function returning CSS style object, e.g., (params) => ({ color: 'red' })
    cell_style: rx.Var | None = None
    # cell_class: JS function returning CSS class name(s), e.g., (params) => 'my-class'
    cell_class: rx.Var | None = None
    # cell_class_rules: Object mapping class names to conditions
    # e.g., {'positive': 'params.value >= 0', 'negative': 'params.value < 0'}
    cell_class_rules: dict[str, str] | rx.Var | None = None

    # Sizing
    width: int | rx.Var[int] | None = None
    min_width: int | rx.Var[int] | None = None
    max_width: int | rx.Var[int] | None = None
    flex: int | rx.Var[int] | None = None
    resizable: bool | None = None

    # Text handling
    wrap_text: bool | None = None
    auto_height: bool | None = None

    # Behavior
    sortable: bool | rx.Var[bool] = True
    enable_cell_change_flash: bool | None = None

    # Grouping (Enterprise)
    row_group: bool | rx.Var[bool] = False
    enable_row_group: bool | rx.Var[bool] = False
    agg_func: str | rx.Var[str] | None = None


class ColumnGroup(PropsBase):
    """
    AG Grid column group definition for grouping related columns.

    Usage:
        ag_grid.column_group(
            group_id="address",
            header_name="Address",
            children=[
                ag_grid.column_def(field="city"),
                ag_grid.column_def(field="country"),
            ],
        )
    """

    children: list["ColumnDef | ColumnGroup"] | rx.Var[list["ColumnDef | ColumnGroup"]]
    group_id: str | rx.Var[str]
    header_name: str | rx.Var[str]
    header_tooltip: str | rx.Var[str] | None = None
    marry_children: bool | rx.Var[bool] = False
    open_by_default: bool | rx.Var[bool] = False
    column_group_show: Literal["open", "closed"] | rx.Var[str] = "open"


# =============================================================================
# AG GRID API HELPER
# =============================================================================


class AgGridAPI(BaseModel):
    """
    Helper for calling AG Grid API methods from Python.

    Usage:
        api = ag_grid.api("my_grid")
        api.selectAll()
        api.exportDataAsCsv()
    """

    model_config = {"arbitrary_types_allowed": True}
    ref: str

    @classmethod
    def create(cls, id: str) -> "AgGridAPI":
        """Create an API instance from a grid ID."""
        return cls(ref=rx.utils.format.format_ref(id))

    @property
    def _api(self) -> str:
        """Get the JS expression for accessing the grid API."""
        return f"refs['{self.ref}']?.current?.api"

    def __getattr__(self, name: str):
        """Dynamically create API method calls."""

        def _call_api(*args, **kwargs):
            var_args = [str(rx.Var.create(arg)) for arg in args]
            camel_name = rx.utils.format.to_camel_case(name)
            return rx.call_script(
                f"{self._api}.{camel_name}({', '.join(var_args)})",
                **kwargs,
            )

        return _call_api


# =============================================================================
# THEME HELPER
# =============================================================================

# Mapping of theme names to their CSS classes (light/dark variants)
_THEME_CLASSES = {
    "quartz": ("ag-theme-quartz", "ag-theme-quartz-dark"),
    "balham": ("ag-theme-balham", "ag-theme-balham-dark"),
    "alpine": ("ag-theme-alpine", "ag-theme-alpine-dark"),
    "material": ("ag-theme-material", "ag-theme-material-dark"),
}


def _get_theme_class_name(theme_name: str) -> rx.Var:
    """
    Get the CSS class name for a theme, respecting color mode.

    Args:
        theme_name: One of "quartz", "balham", "alpine", "material"

    Returns:
        rx.Var that resolves to the correct class based on light/dark mode
    """
    return rx.match(
        theme_name,
        *[
            (name, rx.color_mode_cond(light, dark))
            for name, (light, dark) in _THEME_CLASSES.items()
        ],
        "",  # default
    )


# =============================================================================
# EVENT HELPER FOR GRID READY
# =============================================================================

size_columns_to_fit = rx.Var(
    "(event) => event.api.sizeColumnsToFit()", _var_type=rx.EventChain
)


# =============================================================================
# MAIN AG GRID COMPONENT
# =============================================================================


class AgGrid(rx.Component):
    """
    Reflex AG Grid component wrapping ag-grid-react with Enterprise support.

    Features:
    - CSS imports via add_imports()
    - License key injection via add_custom_code()
    - Event sanitization to remove non-serializable AG Grid objects
    - Dark mode support via theme prop

    Note: ResizeObserver errors may appear briefly during initialization
    but do not affect grid functionality.
    """

    # Library configuration
    library: str = "ag-grid-react@32.3.0"
    tag: str = "AgGridReact"
    lib_dependencies: list[str] = [
        "ag-grid-community@32.3.0",
        "ag-grid-enterprise@32.3.0",
    ]

    # -------------------------------------------------------------------------
    # Core Props
    # -------------------------------------------------------------------------
    column_defs: rx.Var[list[dict[str, Any] | ColumnDef | ColumnGroup]]
    row_data: rx.Var[list[dict[str, Any]]]

    # -------------------------------------------------------------------------
    # Selection
    # -------------------------------------------------------------------------
    row_selection: rx.Var[str] = "single"  # "single" | "multiple"
    cell_selection: bool | rx.Var[bool] = False
    suppress_row_click_selection: rx.Var[bool] = rx.Var.create(False)
    enable_range_selection: rx.Var[bool] = rx.Var.create(False)  # Enterprise

    # -------------------------------------------------------------------------
    # Cell Flash (highlight changes)
    # -------------------------------------------------------------------------
    enable_cell_change_flash: rx.Var[bool] = rx.Var.create(False)

    # -------------------------------------------------------------------------
    # Pagination
    # -------------------------------------------------------------------------
    pagination: rx.Var[bool] = False
    pagination_page_size: rx.Var[int] = rx.Var.create(10)
    pagination_page_size_selector: rx.Var[list[int]] = rx.Var.create([10, 25, 50])

    # -------------------------------------------------------------------------
    # Quick Filter (global search)
    # -------------------------------------------------------------------------
    quick_filter_text: rx.Var[str] = rx.Var.create("")

    # -------------------------------------------------------------------------
    # Styling
    # -------------------------------------------------------------------------
    animate_rows: rx.Var[bool] = False
    theme: rx.Var[Literal["quartz", "balham", "alpine", "material"]]

    # -------------------------------------------------------------------------
    # Column Defaults
    # -------------------------------------------------------------------------
    default_col_def: rx.Var[dict[str, Any]] = rx.Var.create({})
    auto_size_strategy: rx.Var[dict] = rx.Var.create({})

    # -------------------------------------------------------------------------
    # Grouping (Enterprise)
    # -------------------------------------------------------------------------
    group_default_expanded: rx.Var[int] | None = rx.Var.create(-1)  # -1 = all expanded
    group_selects_children: rx.Var[bool] = rx.Var.create(False)
    auto_group_column_def: rx.Var[Any] = rx.Var.create({})
    row_group_panel_show: rx.Var[Literal["always", "onlyWhenGrouping", "never"]] = (
        "never"
    )

    # -------------------------------------------------------------------------
    # Pinned Rows
    # -------------------------------------------------------------------------
    pinned_top_row_data: rx.Var[list[dict[str, Any]]] = rx.Var.create([])
    pinned_bottom_row_data: rx.Var[list[dict[str, Any]]] = rx.Var.create([])

    # -------------------------------------------------------------------------
    # Sidebar (Enterprise)
    # -------------------------------------------------------------------------
    side_bar: rx.Var[str | dict[str, Any] | bool | list[str]] = rx.Var.create("")

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    validation_schema: rx.Var[dict[str, Any]] = rx.Var.create({})

    # -------------------------------------------------------------------------
    # Row ID
    # -------------------------------------------------------------------------
    get_row_id: rx.EventHandler[lambda e0: [e0]]

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------
    on_cell_clicked: rx.EventHandler[_on_cell_event_spec]
    on_cell_double_clicked: rx.EventHandler[_on_cell_event_spec]
    on_cell_value_changed: rx.EventHandler[_on_cell_value_changed]
    on_row_clicked: rx.EventHandler[_on_row_event_spec]
    on_row_double_clicked: rx.EventHandler[_on_row_event_spec]
    on_selection_changed: rx.EventHandler[_on_selection_change_signature]
    on_grid_ready: rx.EventHandler[lambda e0: [e0]]
    on_first_data_rendered: rx.EventHandler[_on_cell_event_spec]
    on_cell_editing_started: rx.EventHandler[_on_cell_editing_spec]
    on_cell_editing_stopped: rx.EventHandler[_on_cell_editing_spec]

    # -------------------------------------------------------------------------
    # Component Creation
    # -------------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *children,
        id: str,
        row_id_key: str | None = None,
        **props,
    ) -> rx.Component:
        """
        Create an AG Grid component.

        Args:
            id: Unique grid identifier (required)
            row_id_key: Field name to use as row ID (e.g., "id")
            **props: Additional AG Grid props

        Returns:
            Configured AG Grid component
        """
        props.setdefault("id", id)

        # Configure row ID getter from row_id_key
        if row_id_key is not None:
            props["get_row_id"] = rx.Var(f"(params) => params.data.{row_id_key}").to(
                rx.EventChain
            )

        # Set theme class based on color mode
        theme_name = props.pop("theme", "quartz")
        props["class_name"] = _get_theme_class_name(theme_name)

        # Auto-size columns on grid ready if auto_size_strategy is set
        if "auto_size_strategy" in props:
            props["on_grid_ready"] = size_columns_to_fit

        # Set default for row group panel
        props.setdefault("row_group_panel_show", "never")

        return super().create(*children, **props)

    def add_imports(self) -> dict:
        """Import AG Grid CSS and Enterprise modules."""
        return {
            "": [
                "ag-grid-community/styles/ag-grid.css",
                "ag-grid-community/styles/ag-theme-quartz.css",
                "ag-grid-community/styles/ag-theme-balham.css",
                "ag-grid-community/styles/ag-theme-material.css",
                "ag-grid-community/styles/ag-theme-alpine.css",
                "ag-grid-enterprise",
            ],
            "ag-grid-enterprise": ["LicenseManager"],
        }

    def add_custom_code(self) -> list[str]:
        """Inject license key from environment variable."""
        import os

        ag_grid_license_key = os.getenv("AG_GRID_LICENSE_KEY")
        if ag_grid_license_key is not None:
            return [f"LicenseManager.setLicenseKey('{ag_grid_license_key}');"]
        return ["LicenseManager.setLicenseKey(null);"]

    # -------------------------------------------------------------------------
    # API Access
    # -------------------------------------------------------------------------

    @property
    def api(self) -> AgGridAPI:
        """Access the AG Grid API for imperative operations."""
        return AgGridAPI(ref=self.get_ref())

    def get_selected_rows(self, callback: rx.EventHandler):
        """Get selected rows and pass to callback."""
        return self.api.getSelectedRows(callback=callback)

    def select_all(self):
        """Select all rows."""
        return self.api.selectAll()

    def deselect_all(self):
        """Deselect all rows."""
        return self.api.deselectAll()

    def export_data_as_csv(self):
        """Export grid data as CSV file."""
        return self.api.exportDataAsCsv()

    def export_data_as_excel(self):
        """Export grid data as Excel file (Enterprise)."""
        return self.api.exportDataAsExcel()


# =============================================================================
# WRAPPED AG GRID (with dimensions)
# =============================================================================


class WrappedAgGrid(AgGrid):
    """
    AG Grid wrapped in a div with configurable width/height.

    This is the default when calling ag_grid(...).
    """

    @classmethod
    def create(cls, *children, **props):
        width = props.pop("width", None)
        height = props.pop("height", None)
        return Div.create(
            super().create(*children, **props),
            width=width or "100%",
            height=height or "400px",
        )


# =============================================================================
# NAMESPACE FOR CLEAN API
# =============================================================================


class AgGridNamespace(rx.ComponentNamespace):
    """
    Namespace providing clean API for AG Grid.

    Usage:
        ag_grid(id="my_grid", ...)       # Creates WrappedAgGrid
        ag_grid.column_def(field="x")    # Creates ColumnDef
        ag_grid.api("my_grid")           # Creates AgGridAPI
    """

    api = AgGridAPI.create
    column_def = ColumnDef
    column_group = ColumnGroup
    filters = AGFilters
    editors = AGEditors
    size_columns_to_fit = size_columns_to_fit
    root = AgGrid.create
    __call__ = WrappedAgGrid.create


# Main export
ag_grid = AgGridNamespace()

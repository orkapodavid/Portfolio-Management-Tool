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
    # NOTE: checkbox_selection removed - use rowSelection.checkboxes in GridOptions (v35)

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
# THEME HELPER (v35 Theming API)
# =============================================================================

# Mapping of theme names to their v35 theme objects.
# In v35, themes are JS objects imported from ag-grid-community.
_THEME_OBJECTS = {
    "quartz": "themeQuartz",
    "balham": "themeBalham",
    "alpine": "themeAlpine",
    "material": "themeMaterial",
}


def _get_theme_object(theme_name: str) -> rx.Var:
    """
    Get the v35 theme object for a theme.

    Args:
        theme_name: One of "quartz", "balham", "alpine", "material"

    Returns:
        rx.Var that references the JavaScript theme object

    Note:
        AG Grid v35 uses the Theming API where themes are JS objects.
        The theme object (e.g., themeQuartz) is passed directly to the theme prop.
    """
    theme_obj = _THEME_OBJECTS.get(theme_name, "themeQuartz")
    # rx.Var(name) creates a Var with _js_expr=name, which renders as-is in JS (unquoted)
    return rx.Var(theme_obj)


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
    library: str = "ag-grid-react@35.0.1"
    tag: str = "AgGridReact"
    lib_dependencies: list[str] = [
        "ag-grid-community@35.0.1",
        "ag-grid-enterprise@35.0.1",
    ]

    # -------------------------------------------------------------------------
    # Core Props
    # -------------------------------------------------------------------------
    column_defs: rx.Var[list[dict[str, Any] | ColumnDef | ColumnGroup]]
    row_data: rx.Var[list[dict[str, Any]]]

    # -------------------------------------------------------------------------
    # Selection (v35 API - object-based config)
    # -------------------------------------------------------------------------
    # row_selection accepts: "single", "multiple", or v35 object config
    # The create() method transforms deprecated string values to v35 object format
    row_selection: rx.Var[str | dict[str, Any]] = "single"
    # cell_selection: v35 API for range selection (replaces deprecated enableRangeSelection)
    cell_selection: bool | rx.Var[bool] = False
    # NOTE: suppress_row_click_selection and group_selects_children are handled
    # in create() and merged into rowSelection object for v35 compatibility

    # NOTE: enable_cell_change_flash removed - use column-level enableCellChangeFlash
    # in columnDefs instead of grid-level option

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
    # Styling (v35 Theming API)
    # -------------------------------------------------------------------------
    animate_rows: rx.Var[bool] = False
    # Note: theme is passed as a JS theme object (themeQuartz, themeBalham, etc.)
    # The wrapper automatically maps these based on the css class name
    theme: rx.Var[Any] = "quartz"  # "quartz" | "balham" | "alpine" | "material"

    # -------------------------------------------------------------------------
    # Column Defaults
    # -------------------------------------------------------------------------
    default_col_def: rx.Var[dict[str, Any]] = rx.Var.create({})
    # NOTE: auto_size_strategy should NOT have a default value - only pass when explicitly set
    auto_size_strategy: rx.Var[dict] | None = None

    # -------------------------------------------------------------------------
    # Grouping (Enterprise)
    # -------------------------------------------------------------------------
    group_default_expanded: rx.Var[int] | None = rx.Var.create(-1)  # -1 = all expanded
    # NOTE: group_selects_children moved to Selection section for v35 migration
    auto_group_column_def: rx.Var[Any] = rx.Var.create({})
    row_group_panel_show: rx.Var[Literal["always", "onlyWhenGrouping", "never"]] = (
        "never"
    )

    # -------------------------------------------------------------------------
    # Tree Data (Enterprise)
    # -------------------------------------------------------------------------
    # IMPORTANT: Using rx.Var.create() for defaults ensures Reflex properly
    # registers these as component props instead of misplacing them in css:{}
    tree_data: rx.Var[bool] = rx.Var.create(False)
    get_data_path: rx.Var | None = None  # JS function: (data) => data.path

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
    # Status Bar (Enterprise)
    # Displays row counts, aggregations, and selection info at grid bottom
    # -------------------------------------------------------------------------
    # status_bar config: {"statusPanels": [...]}
    # Built-in panels: agTotalRowCountComponent, agFilteredRowCountComponent,
    #                  agSelectedRowCountComponent, agAggregationComponent,
    #                  agTotalAndFilteredRowCountComponent
    status_bar: rx.Var[dict[str, Any]] | None = None

    # NOTE: validation_schema removed - not a valid AG Grid option

    # -------------------------------------------------------------------------
    # Advanced Filter (Enterprise) - v35
    # -------------------------------------------------------------------------
    enable_advanced_filter: rx.Var[bool] = False
    # NOTE: advanced_filter_model should NOT have a default value - only pass when explicitly set
    advanced_filter_model: rx.Var[dict[str, Any]] | None = None
    advanced_filter_params: rx.Var[dict[str, Any]] | None = None
    include_hidden_columns_in_advanced_filter: rx.Var[bool] = False

    # -------------------------------------------------------------------------
    # Row Numbers (v33.1+)
    # -------------------------------------------------------------------------
    row_numbers: rx.Var[bool] = False

    # -------------------------------------------------------------------------
    # Grand Total Pinning (v33.3+)
    # -------------------------------------------------------------------------
    grand_total_row: rx.Var[str] = ""
    group_total_row: rx.Var[str] = ""

    # -------------------------------------------------------------------------
    # Undo/Redo Cell Editing
    # -------------------------------------------------------------------------
    undo_redo_cell_editing: rx.Var[bool] = False
    undo_redo_cell_editing_limit: rx.Var[int] = 10

    # -------------------------------------------------------------------------
    # Suppress Events (fine-grained control)
    # -------------------------------------------------------------------------
    suppress_click_edit: rx.Var[bool] = rx.Var.create(False)
    suppress_cell_focus: rx.Var[bool] = rx.Var.create(False)
    suppress_header_focus: rx.Var[bool] = rx.Var.create(False)
    suppress_scroll_on_new_data: rx.Var[bool] = rx.Var.create(False)
    suppress_maintain_unsorted_order: rx.Var[bool] = rx.Var.create(False)
    suppress_row_hover_highlight: rx.Var[bool] = rx.Var.create(False)

    # -------------------------------------------------------------------------
    # Overlays
    # -------------------------------------------------------------------------
    loading: rx.Var[bool] = False
    overlay_loading_template: rx.Var[str] | None = None
    overlay_no_rows_template: rx.Var[str] | None = None
    suppress_no_rows_overlay: rx.Var[bool] = False

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
        # IMPORTANT: AG Grid v35 requires getRowId to return a STRING
        if row_id_key is not None:
            props["get_row_id"] = rx.Var(
                f"(params) => String(params.data.{row_id_key})"
            ).to(rx.EventChain)

        # Set theme using v35 Theming API (theme object, not CSS class)
        theme_name = props.pop("theme", "quartz")
        props["theme"] = _get_theme_object(theme_name)

        # =====================================================================
        # v35 Deprecated Props Migration
        # Transform/remove deprecated props to prevent AG Grid warnings
        # =====================================================================

        # Pop deprecated props to prevent them from being passed to gridOptions
        suppress_row_click = props.pop("suppress_row_click_selection", False)
        group_selects = props.pop("group_selects_children", False)

        # enable_cell_change_flash: in v35, this should be set at column level
        # We move it to defaultColDef to maintain functionality
        enable_cell_flash = props.pop("enable_cell_change_flash", False)
        if enable_cell_flash:
            # Merge into defaultColDef
            default_col_def = props.get("default_col_def", {})
            if isinstance(default_col_def, dict):
                default_col_def["enableCellChangeFlash"] = True
                props["default_col_def"] = default_col_def

        # Transform deprecated row_selection string format to v35 object format
        row_selection = props.get("row_selection", "single")
        if isinstance(row_selection, str) and row_selection in ("single", "multiple"):
            row_selection_config = {
                "mode": "singleRow" if row_selection == "single" else "multiRow",
            }
            # For multiRow, enable checkboxes (v35 replacement for colDef.checkboxSelection)
            if row_selection == "multiple":
                row_selection_config["checkboxes"] = True
            # Merge suppress_row_click_selection into enableClickSelection
            if suppress_row_click:
                row_selection_config["enableClickSelection"] = False
            # Merge group_selects_children into groupSelects
            if group_selects:
                row_selection_config["groupSelects"] = "descendants"
            # Pass as JS object using rx.Var
            props["row_selection"] = rx.Var.create(row_selection_config)

        # Auto-size columns on grid ready if auto_size_strategy is set
        if props.get("auto_size_strategy") is not None:
            props["on_grid_ready"] = size_columns_to_fit

        # Set default for row group panel
        props.setdefault("row_group_panel_show", "never")

        # =================================================================
        # Tree Data Props - Explicit conversion to ensure proper serialization
        # These props are incorrectly placed in css:{} by Reflex if not
        # explicitly converted to rx.Var. This forces them to be recognized
        # as component props rather than styling props.
        # =================================================================
        if "tree_data" in props and props["tree_data"] is True:
            # Convert to rx.Var to ensure it's serialized as a component prop
            props["tree_data"] = rx.Var.create(True)
        
        if "get_data_path" in props and props["get_data_path"] is not None:
            # Ensure the callback is properly wrapped
            get_data_path_val = props["get_data_path"]
            if isinstance(get_data_path_val, rx.Var):
                # Already a Var, ensure it's typed correctly
                props["get_data_path"] = get_data_path_val
            elif isinstance(get_data_path_val, str):
                # Convert string JS function to Var
                props["get_data_path"] = rx.Var(get_data_path_val)

        # =================================================================
        # Remove invalid gridOptions properties
        # These are consumed by the wrapper but not valid AG Grid options
        # =================================================================
        props.pop("id", None)  # 'id' is for container element, not grid

        # Remove None valued props to avoid passing "undefined" to AG Grid
        # (class attributes with None default should not be passed if not set)
        props = {k: v for k, v in props.items() if v is not None}

        return super().create(*children, **props)

    def add_imports(self) -> dict:
        """Import AG Grid v35 theme objects and Enterprise modules.

        AG Grid v35 uses the Theming API which requires importing theme objects
        from ag-grid-community instead of CSS files. The theme object is passed
        to the `theme` grid option.
        """
        return {
            "": [
                "ag-grid-enterprise",
            ],
            "ag-grid-community": [
                "ModuleRegistry",
                "themeQuartz",
                "themeBalham",
                "themeAlpine",
                "themeMaterial",
            ],
            "ag-grid-enterprise": ["LicenseManager", "AllEnterpriseModule"],
        }

    def add_custom_code(self) -> list[str]:
        """Register AG Grid modules and inject license key.

        AG Grid v35 requires explicit module registration via ModuleRegistry.
        AllEnterpriseModule includes all Enterprise features: RowNumbersModule,
        RowGroupingModule, UndoRedoEditModule, etc.
        """
        import os

        # Module registration MUST happen before any grid is created
        code = [
            "ModuleRegistry.registerModules([AllEnterpriseModule]);",
        ]

        ag_grid_license_key = os.getenv("AG_GRID_LICENSE_KEY")
        if ag_grid_license_key is not None:
            code.append(f"LicenseManager.setLicenseKey('{ag_grid_license_key}');")
        else:
            code.append("LicenseManager.setLicenseKey(null);")

        return code

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

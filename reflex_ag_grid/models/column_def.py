"""
Column Definition Pydantic Models

Defines type-safe column configurations that serialize to AG Grid ColDef format.
Uses string keys for formatters/renderers via the Registry Pattern.
"""

from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ColumnType(str, Enum):
    """Supported column data types mapped to AG Grid cell editors."""

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    ENUM = "enum"
    TEXT = "text"  # Large text / multiline


class ColumnDef(BaseModel):
    """
    Pydantic model for AG Grid column definition.

    Uses the Registry Pattern: formatters, renderers, and validators
    are specified as string keys that map to JavaScript functions
    registered in the ag_grid_wrapper.js registry.

    Example:
        ColumnDef(
            field="price",
            header_name="Price",
            type=ColumnType.NUMBER,
            editable=True,
            formatter="currency",  # Maps to JS registry
            cell_class_rules="traffic_light",  # Maps to JS registry
        )
    """

    # Core properties
    field: str = Field(..., description="The field name in the row data")
    header_name: Optional[str] = Field(
        None, description="Display name for column header"
    )

    # Type and editing
    type: ColumnType = Field(
        ColumnType.STRING, description="Data type for editor selection"
    )
    editable: bool = Field(False, description="Whether cells can be edited")

    # Enum values (for ColumnType.ENUM)
    enum_values: Optional[list[str]] = Field(
        None, description="Allowed values for enum type"
    )

    # Sizing
    width: Optional[int] = Field(None, description="Fixed width in pixels")
    min_width: Optional[int] = Field(None, description="Minimum width in pixels")
    max_width: Optional[int] = Field(None, description="Maximum width in pixels")
    flex: Optional[int] = Field(None, description="Flex grow factor")

    # Visibility and pinning
    hide: bool = Field(False, description="Whether column is hidden")
    pinned: Optional[Literal["left", "right"]] = Field(
        None, description="Pin to left or right"
    )
    lock_pinned: bool = Field(False, description="Prevent unpinning")
    lock_position: bool = Field(False, description="Prevent moving")

    # Sorting and filtering
    sortable: bool = Field(True, description="Enable sorting")
    filter: bool = Field(True, description="Enable filtering")
    filter_type: Optional[str] = Field(None, description="Filter type override")

    # Grouping and aggregation
    row_group: bool = Field(False, description="Enable grouping by this column")
    agg_func: Optional[
        Literal["sum", "avg", "count", "min", "max", "first", "last"]
    ] = Field(None, description="Aggregation function for grouped rows")

    # Registry Pattern: String keys for JS functions
    formatter: Optional[str] = Field(
        None,
        description="Registry key for valueFormatter (e.g., 'currency', 'percentage')",
    )
    renderer: Optional[str] = Field(
        None,
        description="Registry key for cellRenderer (e.g., 'status_badge', 'progress_bar')",
    )
    cell_class_rules: Optional[str] = Field(
        None,
        description="Registry key for cellClassRules (e.g., 'traffic_light', 'threshold')",
    )
    value_parser: Optional[str] = Field(
        None, description="Registry key for valueParser for custom parsing"
    )

    # Validation (references ValidationSchema by field name)
    validation: Optional[dict[str, Any]] = Field(
        None, description="Inline validation rules: {min, max, pattern, required}"
    )

    # Cell styling
    cell_style: Optional[dict[str, str]] = Field(None, description="Static cell styles")
    header_class: Optional[str] = Field(None, description="CSS class for header")
    cell_class: Optional[str] = Field(None, description="CSS class for cells")

    # Tooltip
    tooltip_field: Optional[str] = Field(None, description="Field to use for tooltip")

    # Extra AG Grid options (passthrough)
    extra: Optional[dict[str, Any]] = Field(
        None, description="Additional AG Grid ColDef options to merge"
    )

    def to_ag_grid_def(self) -> dict[str, Any]:
        """
        Convert to AG Grid ColDef format.

        Maps Pydantic field names to AG Grid property names and
        includes registry keys for JS-side resolution.
        """
        col_def: dict[str, Any] = {
            "field": self.field,
            "headerName": self.header_name or self.field.replace("_", " ").title(),
        }

        # Type and editor
        col_def["_type"] = self.type.value  # Custom prop for registry lookup
        col_def["editable"] = self.editable

        if self.enum_values:
            col_def["_enumValues"] = self.enum_values

        # Sizing
        if self.width is not None:
            col_def["width"] = self.width
        if self.min_width is not None:
            col_def["minWidth"] = self.min_width
        if self.max_width is not None:
            col_def["maxWidth"] = self.max_width
        if self.flex is not None:
            col_def["flex"] = self.flex

        # Visibility and pinning
        if self.hide:
            col_def["hide"] = True
        if self.pinned:
            col_def["pinned"] = self.pinned
        if self.lock_pinned:
            col_def["lockPinned"] = True
        if self.lock_position:
            col_def["lockPosition"] = True

        # Sorting and filtering
        col_def["sortable"] = self.sortable
        col_def["filter"] = self.filter
        if self.filter_type:
            col_def["filter"] = self.filter_type

        # Grouping
        if self.row_group:
            col_def["rowGroup"] = True
        if self.agg_func:
            col_def["aggFunc"] = self.agg_func

        # Registry keys (prefixed with _ for JS to detect)
        if self.formatter:
            col_def["_formatter"] = self.formatter
        if self.renderer:
            col_def["_renderer"] = self.renderer
        if self.cell_class_rules:
            col_def["_cellClassRules"] = self.cell_class_rules
        if self.value_parser:
            col_def["_valueParser"] = self.value_parser

        # Validation
        if self.validation:
            col_def["_validation"] = self.validation

        # Styling
        if self.cell_style:
            col_def["cellStyle"] = self.cell_style
        if self.header_class:
            col_def["headerClass"] = self.header_class
        if self.cell_class:
            col_def["cellClass"] = self.cell_class

        # Tooltip
        if self.tooltip_field:
            col_def["tooltipField"] = self.tooltip_field

        # Merge extra options
        if self.extra:
            col_def.update(self.extra)

        return col_def

    class Config:
        """Pydantic configuration."""

        use_enum_values = True


def column_defs_to_ag_grid(columns: list[ColumnDef]) -> list[dict[str, Any]]:
    """Convert a list of ColumnDef to AG Grid format."""
    return [col.to_ag_grid_def() for col in columns]

"""
Column Definition Pydantic Models

Defines type-safe column configurations that serialize to AG Grid ColDef format.
Uses string keys for formatters/renderers via the Registry Pattern.

CRITICAL: Uses Pydantic aliases (serialization_alias) to output camelCase
for JavaScript consumption, since Reflex's NoSSRComponent doesn't
rename keys inside data lists like column_defs.
"""

from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


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

    IMPORTANT: Use model_dump(by_alias=True, exclude_none=True) to get
    proper camelCase keys for JavaScript. The `to_ag_grid_def()` method
    does this automatically.

    Example:
        col = ColumnDef(
            field="price",
            header_name="Price",
            type=ColumnType.NUMBER,
            editable=True,
            formatter="currency",
        )
        js_def = col.model_dump(by_alias=True, exclude_none=True)
        # Result: {"field": "price", "headerName": "Price", ...}
    """

    model_config = ConfigDict(
        populate_by_name=True,  # Allow both field name and alias for input
        use_enum_values=True,  # Serialize enums as their values
    )

    # Core properties
    field: str = Field(..., description="The field name in the row data")
    header_name: Optional[str] = Field(
        None,
        serialization_alias="headerName",
        description="Display name for column header",
    )

    # Type and editing (prefixed with _ for JS registry lookup)
    type: ColumnType = Field(
        ColumnType.STRING,
        serialization_alias="_type",
        description="Data type for editor selection",
    )
    editable: bool = Field(False, description="Whether cells can be edited")

    # Enum values (for ColumnType.ENUM)
    enum_values: Optional[list[str]] = Field(
        None,
        serialization_alias="_enumValues",
        description="Allowed values for enum type",
    )

    # Sizing
    width: Optional[int] = Field(None, description="Fixed width in pixels")
    min_width: Optional[int] = Field(
        None,
        serialization_alias="minWidth",
        description="Minimum width in pixels",
    )
    max_width: Optional[int] = Field(
        None,
        serialization_alias="maxWidth",
        description="Maximum width in pixels",
    )
    flex: Optional[int] = Field(None, description="Flex grow factor")

    # Visibility and pinning
    hide: bool = Field(False, description="Whether column is hidden")
    pinned: Optional[Literal["left", "right"]] = Field(
        None,
        description="Pin to left or right",
    )
    lock_pinned: bool = Field(
        False,
        serialization_alias="lockPinned",
        description="Prevent unpinning",
    )
    lock_position: bool = Field(
        False,
        serialization_alias="lockPosition",
        description="Prevent moving",
    )

    # Sorting and filtering
    sortable: bool = Field(True, description="Enable sorting")
    filter: bool = Field(True, description="Enable filtering")
    filter_type: Optional[str] = Field(None, description="Filter type override")

    # Grouping and aggregation
    row_group: bool = Field(
        False,
        serialization_alias="rowGroup",
        description="Enable grouping by this column",
    )
    agg_func: Optional[
        Literal["sum", "avg", "count", "min", "max", "first", "last"]
    ] = Field(
        None,
        serialization_alias="aggFunc",
        description="Aggregation function for grouped rows",
    )

    # Registry Pattern: String keys for JS functions (prefixed with _)
    formatter: Optional[str] = Field(
        None,
        serialization_alias="_formatter",
        description="Registry key for valueFormatter (e.g., 'currency', 'percentage')",
    )
    renderer: Optional[str] = Field(
        None,
        serialization_alias="_renderer",
        description="Registry key for cellRenderer (e.g., 'status_badge', 'progress_bar')",
    )
    cell_class_rules: Optional[str] = Field(
        None,
        serialization_alias="_cellClassRules",
        description="Registry key for cellClassRules (e.g., 'traffic_light', 'threshold')",
    )
    value_parser: Optional[str] = Field(
        None,
        serialization_alias="_valueParser",
        description="Registry key for valueParser for custom parsing",
    )

    # Validation (references ValidationSchema by field name)
    validation: Optional[dict[str, Any]] = Field(
        None,
        serialization_alias="_validation",
        description="Inline validation rules: {min, max, pattern, required}",
    )

    # Cell styling
    cell_style: Optional[dict[str, str]] = Field(
        None,
        serialization_alias="cellStyle",
        description="Static cell styles",
    )
    header_class: Optional[str] = Field(
        None,
        serialization_alias="headerClass",
        description="CSS class for header",
    )
    cell_class: Optional[str] = Field(
        None,
        serialization_alias="cellClass",
        description="CSS class for cells",
    )

    # Tooltip
    tooltip_field: Optional[str] = Field(
        None,
        serialization_alias="tooltipField",
        description="Field to use for tooltip",
    )

    # Extra AG Grid options (passthrough)
    extra: Optional[dict[str, Any]] = Field(
        None,
        description="Additional AG Grid ColDef options to merge",
    )

    def to_ag_grid_def(self) -> dict[str, Any]:
        """
        Convert to AG Grid ColDef format.

        Uses Pydantic's model_dump with aliases to produce camelCase keys.
        Automatically generates headerName from field if not provided.
        """
        # Dump with aliases, excluding None values
        col_def = self.model_dump(by_alias=True, exclude_none=True)

        # Generate headerName from field if not provided
        if "headerName" not in col_def:
            col_def["headerName"] = self.field.replace("_", " ").title()

        # Handle filter_type override (not aliased, needs manual handling)
        if self.filter_type:
            col_def["filter"] = self.filter_type
            col_def.pop("filter_type", None)

        # Merge extra options
        if self.extra:
            extra = col_def.pop("extra", {})
            col_def.update(extra)

        # Remove hide if False (default)
        if not self.hide:
            col_def.pop("hide", None)

        return col_def


def column_defs_to_ag_grid(columns: list[ColumnDef]) -> list[dict[str, Any]]:
    """Convert a list of ColumnDef to AG Grid format."""
    return [col.to_ag_grid_def() for col in columns]

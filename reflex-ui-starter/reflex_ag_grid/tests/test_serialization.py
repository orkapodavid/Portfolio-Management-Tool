"""
Serialization Tests for AG Grid Models

CRITICAL: These tests verify that Pydantic models serialize with correct
camelCase keys for JavaScript consumption. Reflex's NoSSRComponent does NOT
rename keys inside data lists, so we must handle aliasing in Pydantic.

Run: pytest reflex_ag_grid/tests/test_serialization.py -v
"""

import pytest
from reflex_ag_grid.models.column_def import (
    ColumnDef,
    ColumnType,
    column_defs_to_ag_grid,
)
from reflex_ag_grid.models.validation import FieldValidation, ValidationSchema


class TestColumnDefSerialization:
    """Test ColumnDef serialization produces correct camelCase keys."""

    def test_header_name_to_camel_case(self):
        """Verify header_name serializes to headerName."""
        col = ColumnDef(field="price", header_name="Price")

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "headerName" in dump, "Expected 'headerName' (camelCase)"
        assert "header_name" not in dump, "Should NOT contain snake_case 'header_name'"
        assert dump["headerName"] == "Price"

    def test_min_width_to_camel_case(self):
        """Verify min_width serializes to minWidth."""
        col = ColumnDef(field="name", min_width=100, max_width=300)

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "minWidth" in dump
        assert "maxWidth" in dump
        assert "min_width" not in dump
        assert "max_width" not in dump
        assert dump["minWidth"] == 100
        assert dump["maxWidth"] == 300

    def test_lock_pinned_to_camel_case(self):
        """Verify lock_pinned serializes to lockPinned."""
        col = ColumnDef(field="id", lock_pinned=True, lock_position=True)

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "lockPinned" in dump
        assert "lockPosition" in dump
        assert dump["lockPinned"] is True
        assert dump["lockPosition"] is True

    def test_row_group_and_agg_func(self):
        """Verify grouping props serialize correctly."""
        col = ColumnDef(field="category", row_group=True, agg_func="sum")

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "rowGroup" in dump
        assert "aggFunc" in dump
        assert dump["rowGroup"] is True
        assert dump["aggFunc"] == "sum"

    def test_registry_keys_use_underscore_prefix(self):
        """Verify registry keys use _ prefix for JS detection."""
        col = ColumnDef(
            field="value",
            type=ColumnType.NUMBER,
            formatter="currency",
            renderer="progress_bar",
            cell_class_rules="traffic_light",
            value_parser="float",
        )

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "_type" in dump
        assert "_formatter" in dump
        assert "_renderer" in dump
        assert "_cellClassRules" in dump
        assert "_valueParser" in dump
        assert dump["_type"] == "number"
        assert dump["_formatter"] == "currency"

    def test_enum_values_serialization(self):
        """Verify enum_values serializes to _enumValues."""
        col = ColumnDef(
            field="status",
            type=ColumnType.ENUM,
            enum_values=["Active", "Pending", "Cancelled"],
        )

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "_enumValues" in dump
        assert "enum_values" not in dump
        assert dump["_enumValues"] == ["Active", "Pending", "Cancelled"]

    def test_cell_style_serialization(self):
        """Verify cell styling props serialize correctly."""
        col = ColumnDef(
            field="name",
            cell_style={"fontWeight": "bold"},
            header_class="custom-header",
            cell_class="custom-cell",
        )

        dump = col.model_dump(by_alias=True, exclude_none=True)

        assert "cellStyle" in dump
        assert "headerClass" in dump
        assert "cellClass" in dump
        assert dump["cellStyle"] == {"fontWeight": "bold"}

    def test_to_ag_grid_def_generates_header_name(self):
        """Verify to_ag_grid_def auto-generates headerName from field."""
        col = ColumnDef(field="first_name")

        result = col.to_ag_grid_def()

        assert result["headerName"] == "First Name"

    def test_to_ag_grid_def_uses_explicit_header_name(self):
        """Verify explicit header_name is preserved."""
        col = ColumnDef(field="first_name", header_name="Given Name")

        result = col.to_ag_grid_def()

        assert result["headerName"] == "Given Name"

    def test_none_values_excluded(self):
        """Verify None values are excluded from output."""
        col = ColumnDef(field="simple")

        dump = col.model_dump(by_alias=True, exclude_none=True)

        # These should NOT be in the output
        assert "headerName" not in dump  # None -> excluded
        assert "_formatter" not in dump  # None -> excluded
        assert "minWidth" not in dump  # None -> excluded

        # These SHOULD be in the output (have defaults)
        assert "field" in dump
        assert "editable" in dump
        assert "sortable" in dump


class TestColumnDefsToAgGrid:
    """Test the column_defs_to_ag_grid helper function."""

    def test_converts_list_of_column_defs(self):
        """Verify list conversion works."""
        columns = [
            ColumnDef(field="id", header_name="ID"),
            ColumnDef(field="price", type=ColumnType.NUMBER, formatter="currency"),
        ]

        result = column_defs_to_ag_grid(columns)

        assert len(result) == 2
        assert result[0]["headerName"] == "ID"
        assert result[1]["_formatter"] == "currency"


class TestValidationSerialization:
    """Test ValidationSchema and FieldValidation serialization."""

    def test_field_validation_to_js(self):
        """Verify FieldValidation converts to JS format."""
        validation = FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=10000,
            required=True,
        )

        js_config = validation.to_js_validation()

        assert js_config["type"] == "number"
        assert js_config["min"] == 0
        assert js_config["max"] == 10000
        assert js_config["required"] is True

    def test_validation_schema_to_js_config(self):
        """Verify ValidationSchema converts to dict format."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(field_name="price", field_type="number", min_value=0),
                FieldValidation(field_name="name", required=True),
            ]
        )

        config = schema.to_js_config()

        assert "price" in config
        assert "name" in config
        assert config["price"]["min"] == 0
        assert config["name"]["required"] is True

    def test_field_validation_validate_value(self):
        """Verify validation logic works."""
        validation = FieldValidation(
            field_name="quantity",
            field_type="integer",
            min_value=1,
            max_value=100,
        )

        # Valid values
        is_valid, error = validation.validate_value(50)
        assert is_valid is True
        assert error is None

        # Below minimum
        is_valid, error = validation.validate_value(0)
        assert is_valid is False
        assert "quantity" in error.lower() or ">=" in error

        # Above maximum
        is_valid, error = validation.validate_value(200)
        assert is_valid is False

    def test_validation_schema_validate_row(self):
        """Verify row validation works."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(field_name="price", field_type="number", min_value=0),
                FieldValidation(field_name="name", required=True),
            ]
        )

        # Valid row
        is_valid, errors = schema.validate_row({"price": 10, "name": "Widget"})
        assert is_valid is True
        assert len(errors) == 0

        # Invalid row (negative price, missing name)
        is_valid, errors = schema.validate_row({"price": -5, "name": ""})
        assert is_valid is False
        assert "price" in errors or "name" in errors


class TestInputAliasing:
    """Test that input can use either snake_case or camelCase."""

    def test_can_create_with_snake_case(self):
        """Verify snake_case input works."""
        col = ColumnDef(
            field="test",
            header_name="Test Header",
            min_width=100,
        )

        assert col.header_name == "Test Header"
        assert col.min_width == 100

    def test_populate_by_name_allows_both(self):
        """Verify populate_by_name config works."""
        # This should work because of populate_by_name=True
        col = ColumnDef(
            field="test",
            header_name="From Python",  # snake_case input
        )

        dump = col.model_dump(by_alias=True, exclude_none=True)
        assert dump["headerName"] == "From Python"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

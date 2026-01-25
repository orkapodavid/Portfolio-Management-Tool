"""
Unit tests for validation models.

Tests FieldValidation and ValidationSchema classes.
"""

import pytest

from reflex_ag_grid.models.validation import FieldValidation, ValidationSchema


class TestFieldValidation:
    """Tests for FieldValidation model."""

    def test_validate_required_empty(self):
        """Required field with empty value should fail."""
        fv = FieldValidation(field_name="name", required=True)
        is_valid, error = fv.validate_value("")
        assert not is_valid
        assert "required" in error.lower()

    def test_validate_required_none(self):
        """Required field with None value should fail."""
        fv = FieldValidation(field_name="name", required=True)
        is_valid, error = fv.validate_value(None)
        assert not is_valid
        assert "required" in error.lower()

    def test_validate_optional_empty(self):
        """Optional field with empty value should pass."""
        fv = FieldValidation(field_name="name", required=False)
        is_valid, error = fv.validate_value("")
        assert is_valid
        assert error is None

    def test_validate_number_in_range(self):
        """Number within range should pass."""
        fv = FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=100,
        )
        is_valid, error = fv.validate_value(50)
        assert is_valid
        assert error is None

    def test_validate_number_below_min(self):
        """Number below min should fail."""
        fv = FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=100,
        )
        is_valid, error = fv.validate_value(-10)
        assert not is_valid
        assert ">=" in error

    def test_validate_number_above_max(self):
        """Number above max should fail."""
        fv = FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=100,
        )
        is_valid, error = fv.validate_value(150)
        assert not is_valid
        assert "<=" in error

    def test_validate_integer_from_string(self):
        """Integer coercion from string should work."""
        fv = FieldValidation(field_name="qty", field_type="integer")
        is_valid, error = fv.validate_value("42")
        assert is_valid

    def test_validate_integer_invalid_string(self):
        """Invalid integer string should fail."""
        fv = FieldValidation(field_name="qty", field_type="integer")
        is_valid, error = fv.validate_value("not a number")
        assert not is_valid
        assert "type" in error.lower()

    def test_validate_pattern_match(self):
        """Value matching pattern should pass."""
        fv = FieldValidation(
            field_name="symbol",
            pattern="^[A-Z]{1,5}$",
        )
        is_valid, error = fv.validate_value("AAPL")
        assert is_valid
        assert error is None

    def test_validate_pattern_no_match(self):
        """Value not matching pattern should fail."""
        fv = FieldValidation(
            field_name="symbol",
            pattern="^[A-Z]{1,5}$",
        )
        is_valid, error = fv.validate_value("aapl123")
        assert not is_valid
        assert "format" in error.lower()

    def test_validate_enum_valid(self):
        """Valid enum value should pass."""
        fv = FieldValidation(
            field_name="sector",
            enum_values=["Technology", "Finance", "Healthcare"],
        )
        is_valid, error = fv.validate_value("Technology")
        assert is_valid
        assert error is None

    def test_validate_enum_invalid(self):
        """Invalid enum value should fail."""
        fv = FieldValidation(
            field_name="sector",
            enum_values=["Technology", "Finance", "Healthcare"],
        )
        is_valid, error = fv.validate_value("Unknown")
        assert not is_valid
        assert "one of" in error.lower()

    def test_validate_string_min_length(self):
        """String below min length should fail."""
        fv = FieldValidation(
            field_name="name",
            min_length=3,
        )
        is_valid, error = fv.validate_value("AB")
        assert not is_valid
        assert "at least" in error.lower()

    def test_validate_string_max_length(self):
        """String above max length should fail."""
        fv = FieldValidation(
            field_name="name",
            max_length=5,
        )
        is_valid, error = fv.validate_value("TOOLONG")
        assert not is_valid
        assert "at most" in error.lower()

    def test_to_js_validation(self):
        """to_js_validation should return correct dict."""
        fv = FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=1000,
            required=True,
            error_message="Invalid price",
        )
        js = fv.to_js_validation()
        assert js["type"] == "number"
        assert js["min"] == 0
        assert js["max"] == 1000
        assert js["required"] is True
        assert js["errorMessage"] == "Invalid price"


class TestValidationSchema:
    """Tests for ValidationSchema model."""

    def test_get_field_found(self):
        """get_field should return field if found."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(field_name="price", field_type="number"),
                FieldValidation(field_name="qty", field_type="integer"),
            ]
        )
        field = schema.get_field("price")
        assert field is not None
        assert field.field_name == "price"

    def test_get_field_not_found(self):
        """get_field should return None if not found."""
        schema = ValidationSchema(fields=[])
        field = schema.get_field("missing")
        assert field is None

    def test_validate_row_all_valid(self):
        """validate_row should pass with valid data."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(
                    field_name="price",
                    field_type="number",
                    min_value=0,
                ),
                FieldValidation(
                    field_name="qty",
                    field_type="integer",
                    min_value=1,
                ),
            ]
        )
        row = {"price": 100, "qty": 10}
        is_valid, errors = schema.validate_row(row)
        assert is_valid
        assert len(errors) == 0

    def test_validate_row_with_errors(self):
        """validate_row should return errors for invalid data."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(
                    field_name="price",
                    field_type="number",
                    min_value=0,
                ),
                FieldValidation(
                    field_name="qty",
                    field_type="integer",
                    min_value=1,
                ),
            ]
        )
        row = {"price": -10, "qty": 0}
        is_valid, errors = schema.validate_row(row)
        assert not is_valid
        assert "price" in errors
        assert "qty" in errors

    def test_to_js_config(self):
        """to_js_config should return field-keyed dict."""
        schema = ValidationSchema(
            fields=[
                FieldValidation(field_name="price", field_type="number"),
                FieldValidation(field_name="qty", field_type="integer"),
            ]
        )
        config = schema.to_js_config()
        assert "price" in config
        assert "qty" in config
        assert config["price"]["type"] == "number"
        assert config["qty"]["type"] == "integer"

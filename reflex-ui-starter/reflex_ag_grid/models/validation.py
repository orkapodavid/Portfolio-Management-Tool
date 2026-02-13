"""
Validation Schema Pydantic Models

Replaces .ini-based validation with type-safe Pydantic models.
Can be shared between backend state and frontend validators.
"""

from typing import Any, Optional
import re

from pydantic import BaseModel, Field, field_validator


class FieldValidation(BaseModel):
    """
    Validation rules for a single field.

    These rules are serialized to JSON and passed to the AG Grid wrapper
    for client-side validation in the valueParser.

    Example:
        FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=1_000_000,
            required=True,
            error_message="Price must be between 0 and 1,000,000"
        )
    """

    field_name: str = Field(..., description="Name of the field to validate")
    field_type: str = Field(
        "string", description="Data type: string, number, integer, boolean, enum"
    )

    # Numeric constraints
    min_value: Optional[float] = Field(None, description="Minimum allowed value")
    max_value: Optional[float] = Field(None, description="Maximum allowed value")

    # String constraints
    min_length: Optional[int] = Field(None, description="Minimum string length")
    max_length: Optional[int] = Field(None, description="Maximum string length")
    pattern: Optional[str] = Field(None, description="Regex pattern for validation")

    # Enum constraints
    enum_values: Optional[list[str]] = Field(
        None, description="Allowed values for enum type"
    )

    # General
    required: bool = Field(False, description="Whether field is required")
    error_message: Optional[str] = Field(None, description="Custom error message")

    @field_validator("pattern")
    @classmethod
    def validate_pattern(cls, v: Optional[str]) -> Optional[str]:
        """Validate that pattern is a valid regex."""
        if v is not None:
            try:
                re.compile(v)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")
        return v

    def validate_value(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a value against this field's rules.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required check
        if self.required and (value is None or value == ""):
            return False, self.error_message or f"{self.field_name} is required"

        if value is None or value == "":
            return True, None

        # Type coercion and validation
        try:
            if self.field_type in ("integer", "int"):
                value = int(value)
            elif self.field_type in ("number", "float"):
                value = float(value)
            elif self.field_type == "boolean":
                if isinstance(value, str):
                    value = value.lower() in ("true", "1", "yes")
                else:
                    value = bool(value)
        except (ValueError, TypeError):
            return (
                False,
                self.error_message
                or f"{self.field_name} must be type {self.field_type}",
            )

        # Numeric range validation
        if self.min_value is not None and isinstance(value, (int, float)):
            if value < self.min_value:
                return (
                    False,
                    self.error_message
                    or f"{self.field_name} must be >= {self.min_value}",
                )

        if self.max_value is not None and isinstance(value, (int, float)):
            if value > self.max_value:
                return (
                    False,
                    self.error_message
                    or f"{self.field_name} must be <= {self.max_value}",
                )

        # String length validation
        if isinstance(value, str):
            if self.min_length is not None and len(value) < self.min_length:
                return (
                    False,
                    self.error_message
                    or f"{self.field_name} must be at least {self.min_length} characters",
                )

            if self.max_length is not None and len(value) > self.max_length:
                return (
                    False,
                    self.error_message
                    or f"{self.field_name} must be at most {self.max_length} characters",
                )

        # Pattern validation
        if self.pattern and isinstance(value, str):
            if not re.match(self.pattern, value):
                return (
                    False,
                    self.error_message
                    or f"{self.field_name} doesn't match required format",
                )

        # Enum validation
        if self.enum_values and value not in self.enum_values:
            return (
                False,
                self.error_message
                or f"{self.field_name} must be one of: {', '.join(self.enum_values)}",
            )

        return True, None

    def to_js_validation(self) -> dict[str, Any]:
        """Convert to JS-compatible validation object."""
        result: dict[str, Any] = {
            "type": self.field_type,
            "required": self.required,
        }

        if self.min_value is not None:
            result["min"] = self.min_value
        if self.max_value is not None:
            result["max"] = self.max_value
        if self.min_length is not None:
            result["minLength"] = self.min_length
        if self.max_length is not None:
            result["maxLength"] = self.max_length
        if self.pattern:
            result["pattern"] = self.pattern
        if self.enum_values:
            result["enumValues"] = self.enum_values
        if self.error_message:
            result["errorMessage"] = self.error_message

        return result


class ValidationSchema(BaseModel):
    """
    Complete validation schema for a grid.

    Maps field names to their validation rules.

    Example:
        schema = ValidationSchema(
            fields=[
                FieldValidation(field_name="price", field_type="number", min_value=0),
                FieldValidation(field_name="symbol", pattern="^[A-Z]{1,5}$"),
            ]
        )
    """

    fields: list[FieldValidation] = Field(default_factory=list)

    def get_field(self, field_name: str) -> Optional[FieldValidation]:
        """Get validation rules for a specific field."""
        for field in self.fields:
            if field.field_name == field_name:
                return field
        return None

    def validate_row(self, row: dict[str, Any]) -> tuple[bool, dict[str, str]]:
        """
        Validate an entire row against the schema.

        Returns:
            Tuple of (all_valid, errors_dict)
            errors_dict maps field names to error messages
        """
        errors: dict[str, str] = {}

        for field_validation in self.fields:
            value = row.get(field_validation.field_name)
            is_valid, error = field_validation.validate_value(value)
            if not is_valid and error:
                errors[field_validation.field_name] = error

        return len(errors) == 0, errors

    def to_js_config(self) -> dict[str, dict[str, Any]]:
        """Convert to JS-compatible validation config."""
        return {field.field_name: field.to_js_validation() for field in self.fields}

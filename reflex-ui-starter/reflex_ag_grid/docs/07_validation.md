# 07 - Validation

**Requirement**: Data validation for cell editing  
**AG Grid Feature**: `valueParser`, `valueValidator`, and visual feedback  
**Demo Route**: `/07-validation`

## Overview

Data validation ensures that user-entered values meet defined criteria before being accepted. Invalid values can be rejected or shown with visual feedback.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `valueParser` | Parse user input before setting value |
| `cellClassRules` | Apply CSS classes based on value |
| `valueSetter` | Custom logic when setting value |

## Code Example

```python
from reflex_ag_grid import ag_grid
from reflex_ag_grid.models import ValidationSchema, FieldValidation

# Define validation rules
schema = ValidationSchema(fields=[
    FieldValidation(
        field="price",
        type="number",
        min_value=0,
        max_value=10000,
        required=True,
    ),
    FieldValidation(
        field="symbol",
        type="string",
        pattern=r"^[A-Z]{1,5}$",
        required=True,
    ),
    FieldValidation(
        field="sector",
        type="enum",
        enum_values=["Technology", "Finance", "Healthcare"],
    ),
])
```

## Validation Types

| Type | Validation |
|------|------------|
| `number` | min/max value, integer check |
| `string` | min/max length, pattern regex |
| `enum` | Value must be in list |

## Visual Feedback

Use `cellClassRules` for visual validation:

```javascript
cellClassRules: {
    'invalid-cell': params => params.value < 0,
    'warning-cell': params => params.value > 1000,
}
```

## How to Implement

1. Define `ValidationSchema` with field rules
2. Pass to grid component
3. Invalid cells show visual feedback
4. Values can be rejected or corrected

## Related Documentation

- [AG Grid Value Parsers](https://www.ag-grid.com/javascript-data-grid/value-parsers/)

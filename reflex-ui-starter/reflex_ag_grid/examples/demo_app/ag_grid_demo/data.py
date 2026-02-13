"""
Demo App Data - Sample data and constants for all demo pages.

Contains:
- SAMPLE_DATA: 8 sample stock records
- SECTORS: Available sector values
- EDITABLE_VALIDATION: Validation schema for editable grids
"""

from reflex_ag_grid import FieldValidation, ValidationSchema


# =============================================================================
# VALIDATION SCHEMA
# =============================================================================

EDITABLE_VALIDATION = ValidationSchema(
    fields=[
        FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=1_000_000,
            required=True,
            error_message="Price must be between 0 and 1,000,000",
        ),
        FieldValidation(
            field_name="qty",
            field_type="integer",
            min_value=1,
            max_value=10_000,
            required=True,
            error_message="Quantity must be between 1 and 10,000",
        ),
        FieldValidation(
            field_name="change",
            field_type="number",
            min_value=-100,
            max_value=100,
            error_message="Change must be between -100% and 100%",
        ),
        FieldValidation(
            field_name="symbol",
            field_type="string",
            pattern="^[A-Z]{1,5}$",
            required=True,
            error_message="Symbol must be 1-5 uppercase letters",
        ),
        FieldValidation(
            field_name="sector",
            field_type="enum",
            enum_values=["Technology", "Finance", "Healthcare", "Energy"],
            required=True,
            error_message="Invalid sector",
        ),
    ]
)


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_DATA = [
    {
        "id": "0",
        "symbol": "AAPL",
        "company": "Apple Inc.",
        "sector": "Technology",
        "price": 175.50,
        "qty": 100,
        "change": 2.5,
        "active": True,
        "status": "Active",
    },
    {
        "id": "1",
        "symbol": "GOOGL",
        "company": "Alphabet Inc.",
        "sector": "Technology",
        "price": 140.25,
        "qty": 50,
        "change": -1.2,
        "active": True,
        "status": "Pending",
    },
    {
        "id": "2",
        "symbol": "MSFT",
        "company": "Microsoft Corp.",
        "sector": "Technology",
        "price": 378.90,
        "qty": 75,
        "change": 0.8,
        "active": True,
        "status": "Active",
    },
    {
        "id": "3",
        "symbol": "JPM",
        "company": "JPMorgan Chase",
        "sector": "Finance",
        "price": 195.00,
        "qty": 200,
        "change": 1.5,
        "active": False,
        "status": "Inactive",
    },
    {
        "id": "4",
        "symbol": "GS",
        "company": "Goldman Sachs",
        "sector": "Finance",
        "price": 385.75,
        "qty": 30,
        "change": -0.5,
        "active": True,
        "status": "Active",
    },
    {
        "id": "5",
        "symbol": "JNJ",
        "company": "Johnson & Johnson",
        "sector": "Healthcare",
        "price": 155.30,
        "qty": 120,
        "change": 0.3,
        "active": True,
        "status": "Pending",
    },
    {
        "id": "6",
        "symbol": "PFE",
        "company": "Pfizer Inc.",
        "sector": "Healthcare",
        "price": 28.50,
        "qty": 500,
        "change": -2.1,
        "active": False,
        "status": "Inactive",
    },
    {
        "id": "7",
        "symbol": "XOM",
        "company": "Exxon Mobil",
        "sector": "Energy",
        "price": 105.20,
        "qty": 150,
        "change": 3.2,
        "active": True,
        "status": "Active",
    },
]

SECTORS = ["Technology", "Finance", "Healthcare", "Energy"]

# 26 - Quick Filter

> Demo Route: `/26-quick-filter`

## Requirement

Provide a text search box that filters all data in the grid instantly.

## AG Grid Feature

- **quickFilterText** - The search text to filter the grid
- **quickFilterParser** - Optional custom parser for search terms

## How It Works

1. User types in the search input box
2. The search text is passed to AG Grid's `quickFilterText` prop
3. AG Grid searches across all visible columns for matches
4. Rows are filtered to show only matching results

## Code Example

```python
from reflex_ag_grid import ag_grid
import reflex as rx


class SearchState(rx.State):
    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value


def page():
    return rx.vstack(
        rx.input(
            placeholder="Search...",
            value=SearchState.search_text,
            on_change=SearchState.set_search,
        ),
        ag_grid(
            row_data=State.data,
            column_defs=columns,
            quick_filter_text=SearchState.search_text,
        ),
    )
```

## Key Props

| Prop | Type | Description |
|------|------|-------------|
| `quick_filter_text` | `str` | The text to filter by across all columns |

## Notes

- Quick Filter is a **Community** feature (no Enterprise license required)
- Searches all visible column values
- Case-insensitive by default
- Splits search text by spaces and matches all words

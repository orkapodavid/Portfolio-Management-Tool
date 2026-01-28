# 21 - CRUD Data Source

**Requirement**: Create, Read, Update, Delete operations  
**AG Grid Feature**: Data manipulation + inline editing  
**Demo Route**: `/21-crud`

## Overview

Complete CRUD operations with in-memory data store and inline cell editing.

## CRUD Pattern

```python
class CrudState(rx.State):
    data: list[dict] = INITIAL_DATA
    next_id: int = 1
    
    # CREATE
    def add_row(self):
        new_row = {"id": self.next_id, "name": "New Item"}
        self.data = self.data + [new_row]
        self.next_id += 1
    
    # UPDATE (via on_cell_value_changed)
    def on_cell_edit(self, row_id: str, field: str, value):
        for i, row in enumerate(self.data):
            if str(row.get("id")) == row_id:
                self.data[i][field] = value
                break
    
    # DELETE
    def delete_row(self, row_id: int):
        self.data = [r for r in self.data if r.get("id") != row_id]
```

## Grid Configuration

```python
ag_grid(
    row_data=CrudState.data,
    column_defs=[
        {"field": "id", "editable": False},
        {"field": "name", "editable": True},
        {"field": "email", "editable": True},
    ],
    row_id_key="id",
    on_cell_value_changed=CrudState.on_cell_edit,
    enable_cell_change_flash=True,
)
```

## Related Documentation

- [AG Grid Cell Editing](https://www.ag-grid.com/javascript-data-grid/cell-editing/)

# 17 - Tree Data

**Requirement**: Hierarchical data display  
**AG Grid Feature**: Tree Data + getDataPath  
**Demo Route**: `/17-tree-data`

## Overview

Tree Data displays hierarchical relationships like file/folder structures. AG Grid uses `getDataPath` to build the tree from flat data with path arrays.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `treeData=True` | Enable tree data mode |
| `getDataPath` | JS function to extract path from row |
| `autoGroupColumnDef` | Configure the tree column |
| `groupDefaultExpanded` | Control initial expand state |

## Data Structure

```python
# Each row needs a 'path' array defining its tree location
TREE_DATA = [
    {"id": "1", "path": ["Documents"], "name": "Documents", "type": "folder"},
    {"id": "2", "path": ["Documents", "Reports"], "name": "Reports", "type": "folder"},
    {"id": "3", "path": ["Documents", "Reports", "Q1.xlsx"], "name": "Q1.xlsx", "type": "file"},
]
```

## Python Usage

```python
ag_grid(
    row_data=State.data,
    column_defs=[...],
    tree_data=True,
    get_data_path=rx.Var("(data) => data.path"),
    auto_group_column_def={
        "headerName": "File Explorer",
        "minWidth": 300,
    },
    group_default_expanded=-1,  # -1 = expand all
)
```

## Related Documentation

- [AG Grid Tree Data](https://www.ag-grid.com/javascript-data-grid/tree-data/)

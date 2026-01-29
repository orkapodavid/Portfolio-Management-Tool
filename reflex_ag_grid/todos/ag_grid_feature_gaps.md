# AG Grid Feature Gap Analysis

This document identifies AG Grid features (Community & Enterprise) that are **NOT yet implemented** in the `reflex_ag_grid` wrapper or demonstrated in the demo app.

## Summary

| Category | Implemented | Not Implemented |
|----------|-------------|-----------------|
| Enterprise Features | 10 | 14 |
| Community Features | 8 | 12 |
| Row Models | 1 | 3 |

---

## Enterprise Features NOT Implemented

### 🔴 High Priority (Common Use Cases)

| Feature | Description | Props/API Required |
|---------|-------------|-------------------|
| **Master/Detail** | Nested grids within rows for hierarchical data | `masterDetail`, `detailCellRenderer`, `detailRowHeight`, `keepDetailRows` |
| **Pivoting** | Cross-tab pivot tables with row/column pivoting | `pivotMode`, `pivot` (on colDef), `pivotPanelShow` |
| **Integrated Charts** | Build charts directly from grid data | `enableCharts`, AG Charts module dependency |
| **Sparklines** | Mini inline charts in cells | `cellRenderer: 'agSparklineCellRenderer'`, `cellRendererParams` |
| **Server-Side Row Model** | Lazy-loading with server-side operations | `rowModelType: 'serverSide'`, `serverSideDatasource` |
| **Advanced Filter** | Builder UI for complex filter expressions | `enableAdvancedFilter`, `advancedFilterModel` |

### 🟡 Medium Priority

| Feature | Description | Props/API Required |
|---------|-------------|-------------------|
| **Row Spanning** | Cells spanning multiple rows | `spanRows` (on colDef) - new in v33.1 |
| **Column Spanning** | Cells spanning multiple columns | `colSpan` (on colDef) |
| **Set Filter** | Multi-select checkbox filter (partial - prop exists) | `filter: 'agSetColumnFilter'` + full params |
| **Multi Filter** | Combined filter with multiple filter types | `filter: 'agMultiColumnFilter'` |
| **Row Numbers** | Automatic row numbering column | `enableRowNumbers` - new in v33.1 |
| **Grand Total Pinning** | Pinned totals at top/bottom of groups | New in v33.3 |
| **Batch Editing** | Edit multiple cells before committing | `batchEditMode` - new in v34.0 |
| **Cell Editor Validation** | Built-in editor validation | `cellEditorParams.validation` - new in v34.0 |

---

## Community Features NOT Implemented

### Grid Props NOT Exposed

| Feature | Description | Props Required |
|---------|-------------|---------------|
| **Infinite Row Model** | Infinite scrolling for large datasets | `rowModelType: 'infinite'`, `datasource`, `cacheBlockSize` |
| **Viewport Row Model** | Viewport-based rendering | `rowModelType: 'viewport'`, `viewportDatasource` |
| **Full Width Rows** | Rows spanning all columns | `fullWidthCellRenderer`, `isFullWidthRow` |
| **Row Height** | Dynamic row height | `rowHeight`, `getRowHeight`, `rowHeightResizing` (v33.3) |
| **Header Height** | Custom header heights | `headerHeight`, `groupHeaderHeight`, `floatingFiltersHeight` |
| **Row Dragging** | Drag rows to reorder | `rowDrag`, `rowDragManaged`, `rowDragEntireRow` |
| **Row Pinning API** | Pin rows dynamically via API | `api.setRowPinned()` |
| **Loading Overlays** (partial) | Custom loading component | `loadingOverlayComponent` - only overlay template exposed |
| **Tooltip** | Custom cell tooltips | `tooltipField`, `tooltipValueGetter`, `tooltipComponent` |
| **Immutable Data** | Optimized updates for immutable data | `immutableData`, `deltaRowDataMode` |
| **Suppress Events** | Fine-grained event control | `suppressClickEdit`, `suppressCellFocus`, etc. |
| **Undo/Redo** | Edit history with undo/redo | `undoRedoCellEditing`, `undoRedoCellEditingLimit` |

---

## Column Definition Fields NOT Exposed

The current `ColumnDef` class exposes 25+ fields. The following are **missing**:

| Field | Description |
|-------|-------------|
| `pinned` | Pin column left/right (`'left'`, `'right'`) |
| `lockPosition` | Lock column position |
| `lockVisible` | Lock column visibility |
| `lockPinned` | Lock column pinned state |
| `suppressMenu` | Hide column menu |
| `suppressMovable` | Prevent column moving |
| `suppressSizeToFit` | Exclude from auto-size |
| `pivot` | Use column for pivoting |
| `pivotIndex` | Pivot order |
| `toolPanelClass` | Custom class in tool panel |
| `colSpan` | Column spanning callback |
| `spanRows` | Row spanning callback |
| `tooltipField` | Tooltip source field |
| `tooltipValueGetter` | Custom tooltip getter |
| `maxNumConditions` | Max filter conditions |

---

## Event Handlers NOT Exposed

| Event | Description |
|-------|-------------|
| `onColumnVisible` | Column visibility changed |
| `onColumnPinned` | Column pinned/unpinned |
| `onColumnResized` | Column width changed |
| `onColumnMoved` | Column position changed |
| `onColumnGroupOpened` | Column group expanded/collapsed |
| `onRowGroupOpened` | Row group expanded/collapsed |
| `onExpandOrCollapseAll` | Expand/collapse all triggered |
| `onCellFocused` | Cell focus changed |
| `onPaginationChanged` | Pagination state changed |
| `onSortChanged` | Sort model changed |
| `onFilterChanged` | Filter model changed |
| `onRowDragEnter/Move/End` | Row drag events |
| `onChartCreated/Updated/Destroyed` | Chart lifecycle (Enterprise) |
| `onToolPanelVisibleChanged` | Tool panel opened/closed |

---

## API Methods NOT Exposed

The current `AgGridAPI` class supports dynamic method calls, but these are commonly needed:

| Method | Description |
|--------|-------------|
| `setFilterModel()` | Set all column filters programmatically |
| `getFilterModel()` | Get current filter state |
| `setSortModel()` | Set column sorting |
| `getSortModel()` | Get current sort state |
| `expandAll()` / `collapseAll()` | Group expansion |
| `forEachNode()` | Iterate all nodes |
| `refreshCells()` | Refresh specific cells |
| `flashCells()` | Flash specific cells |
| `ensureIndexVisible()` | Scroll to row by index |
| `ensureNodeVisible()` | Scroll to node |
| `getPinnedTopRowCount()` / `getPinnedBottomRowCount()` | Pinned row counts |
| `createRangeChart()` | Create chart from selection (Enterprise) |

---

## Components NOT Demonstrated in Demo App

The demo app has 21 pages but does **not** demonstrate:

| Feature | Demo Priority |
|---------|---------------|
| Master/Detail grids | 🔴 High |
| Pivoting tables | 🔴 High |
| Integrated Charts | 🔴 High |
| Sparklines in cells | 🟡 Medium |
| Row Spanning | 🟡 Medium |
| Column Spanning | 🟡 Medium |
| Row Drag & Drop | 🟡 Medium |
| Full Width Rows | 🟢 Low |
| Custom Tooltips | 🟢 Low |
| Undo/Redo editing | 🟢 Low |

---

## Currently Implemented Features

For reference, these features ARE implemented in `ag_grid.py`:

### Component Props
- `column_defs`, `row_data`
- `row_selection` (single/multiple), `cell_selection`
- `enable_range_selection` (Enterprise)
- `enable_cell_change_flash`
- `pagination`, `pagination_page_size`, `pagination_page_size_selector`
- `quick_filter_text`
- `animate_rows`, `theme` (with dark mode)
- `default_col_def`, `auto_size_strategy`
- `group_default_expanded`, `group_selects_children`, `auto_group_column_def`
- `pinned_top_row_data`, `pinned_bottom_row_data`
- `side_bar` (Enterprise)
- `validation_schema`

### Column Definition Fields
- `field`, `col_id`, `type`
- `header_name`, `header_tooltip`, `hide`
- `editable`, `cell_editor`, `cell_editor_params`
- `filter`, `floating_filter`
- `value_formatter`, `cell_renderer`, `checkbox_selection`
- `cell_style`, `cell_class`, `cell_class_rules`
- `width`, `min_width`, `max_width`, `flex`, `resizable`
- `wrap_text`, `auto_height`
- `sortable`, `enable_cell_change_flash`
- `row_group`, `enable_row_group`, `agg_func` (Enterprise)

### Events
- `on_cell_clicked`, `on_cell_double_clicked`
- `on_cell_value_changed`
- `on_row_clicked`, `on_row_double_clicked`
- `on_selection_changed`
- `on_grid_ready`, `on_first_data_rendered`
- `on_cell_editing_started`, `on_cell_editing_stopped`

### Demo App Pages (21 total)
1. Context Menu
2. Range Selection
3. Cell Flash
4. Jump & Highlight
5. Grouping & Aggregation
6. Notifications
7. Validation
8. Clipboard
9. Excel Export
10. WebSocket Updates
11. Cell Editors
12. Edit Pause
13. Transaction API
14. Background Tasks
15. Column State
16. Cell Renderers
17. Tree Data
18. Performance Testing
19. Status Bar
20. Overlays
21. CRUD Data Source

---

## Recommendations

### Phase 1: High-Impact Enterprise Features
1. **Master/Detail** - Common for complex data relationships
2. **Pivoting** - Essential for analytics dashboards
3. **Integrated Charts** - High-value visualization capability

### Phase 2: Community Core Features
1. **Row/Column Spanning** - Important for report-style grids
2. **Row Dragging** - User-requested for reordering
3. **Undo/Redo** - Improves editing experience
4. **Tooltips** - Better data visibility

### Phase 3: Advanced Row Models
1. **Server-Side Row Model** - For truly large datasets
2. **Infinite Scrolling** - Simpler lazy-loading option

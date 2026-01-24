/**
 * AG Grid Wrapper for Reflex Python
 * 
 * ARCHITECTURAL PATTERNS IMPLEMENTED:
 * 
 * 1. FUNCTION REGISTRY PATTERN
 *    Python cannot pass functions to JavaScript. Instead, Python passes
 *    string keys (e.g., "currency_formatter") that map to functions
 *    registered in the REGISTRIES below.
 * 
 * 2. EVENT SANITIZATION
 *    AG Grid events contain circular references (gridApi). We extract
 *    only safe, serializable data before sending to Python.
 * 
 * 3. LICENSE KEY INJECTION
 *    Enterprise license is applied before grid instantiation via
 *    the licenseKey prop or window.AG_GRID_LICENSE_KEY.
 * 
 * @module ag_grid_wrapper
 */

import React, { useRef, useEffect, useCallback, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { LicenseManager } from 'ag-grid-enterprise';

// Styles
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-balham.css';
import 'ag-grid-enterprise';

// ============================================================================
// LICENSE KEY INJECTION (Constraint #4)
// ============================================================================

/**
 * Apply AG Grid Enterprise license key.
 * Priority: prop > window.AG_GRID_LICENSE_KEY > window.ENV.AG_GRID_LICENSE_KEY
 */
function applyLicenseKey(licenseKey) {
    const key = licenseKey
        || window.AG_GRID_LICENSE_KEY
        || window.ENV?.AG_GRID_LICENSE_KEY;

    if (key) {
        LicenseManager.setLicenseKey(key);
        console.log('[AGGrid] License key applied');
    } else {
        console.warn('[AGGrid] No license key found - watermark will appear');
    }
}

// ============================================================================
// FUNCTION REGISTRY (Constraint #1)
// ============================================================================

/**
 * Registry of value formatters.
 * Python passes string keys that map to these functions.
 * 
 * Add custom formatters here:
 *   FORMATTER_REGISTRY['my_formatter'] = (params) => { ... }
 */
const FORMATTER_REGISTRY = {
    // Currency formatter: $1,234.56
    currency: (params) => {
        if (params.value == null) return '';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        }).format(params.value);
    },

    // Currency (JPY): ¥1,234
    currency_jpy: (params) => {
        if (params.value == null) return '';
        return new Intl.NumberFormat('ja-JP', {
            style: 'currency',
            currency: 'JPY',
        }).format(params.value);
    },

    // Percentage: 12.34%
    percentage: (params) => {
        if (params.value == null) return '';
        return `${(params.value * 100).toFixed(2)}%`;
    },

    // Percentage (already multiplied): 12.34%
    percentage_value: (params) => {
        if (params.value == null) return '';
        return `${params.value.toFixed(2)}%`;
    },

    // Number with commas: 1,234,567
    number: (params) => {
        if (params.value == null) return '';
        return new Intl.NumberFormat('en-US').format(params.value);
    },

    // Decimal: 1,234.56
    decimal: (params) => {
        if (params.value == null) return '';
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(params.value);
    },

    // Date: 2024-01-15
    date: (params) => {
        if (params.value == null) return '';
        const date = new Date(params.value);
        return date.toISOString().split('T')[0];
    },

    // DateTime: 2024-01-15 14:30
    datetime: (params) => {
        if (params.value == null) return '';
        const date = new Date(params.value);
        return date.toLocaleString();
    },

    // Boolean: Yes/No
    boolean: (params) => {
        if (params.value == null) return '';
        return params.value ? 'Yes' : 'No';
    },

    // Uppercase
    uppercase: (params) => {
        if (params.value == null) return '';
        return String(params.value).toUpperCase();
    },
};

/**
 * Registry of cell renderers.
 * For more complex rendering (React components), add here.
 */
const RENDERER_REGISTRY = {
    // Status badge with colors
    status_badge: (params) => {
        if (params.value == null) return '';
        const colors = {
            'Active': 'bg-green-100 text-green-800',
            'Pending': 'bg-yellow-100 text-yellow-800',
            'Cancelled': 'bg-red-100 text-red-800',
            'Completed': 'bg-blue-100 text-blue-800',
        };
        const colorClass = colors[params.value] || 'bg-gray-100 text-gray-800';
        return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass}">${params.value}</span>`;
    },

    // Progress bar (value 0-100)
    progress_bar: (params) => {
        if (params.value == null) return '';
        const percent = Math.min(100, Math.max(0, params.value));
        const color = percent >= 75 ? 'bg-green-500' : percent >= 50 ? 'bg-yellow-500' : 'bg-red-500';
        return `<div class="w-full bg-gray-200 rounded-full h-2">
            <div class="${color} h-2 rounded-full" style="width: ${percent}%"></div>
        </div>`;
    },
};

/**
 * Registry of cell class rules.
 * Returns object mapping class names to condition functions.
 */
const CELL_CLASS_RULES_REGISTRY = {
    // Traffic light: green for positive, red for negative
    traffic_light: {
        'bg-green-50 text-green-700': (params) => params.value > 0,
        'bg-red-50 text-red-700': (params) => params.value < 0,
    },

    // Threshold-based: green >= 100, yellow >= 50, red < 50
    threshold: {
        'bg-green-50 text-green-700': (params) => params.value >= 100,
        'bg-yellow-50 text-yellow-700': (params) => params.value >= 50 && params.value < 100,
        'bg-red-50 text-red-700': (params) => params.value < 50,
    },

    // Bold for non-zero
    bold_nonzero: {
        'font-bold': (params) => params.value !== 0 && params.value != null,
    },
};

/**
 * Registry of value parsers for editing.
 */
const VALUE_PARSER_REGISTRY = {
    // Parse as integer
    integer: (params) => {
        const parsed = parseInt(params.newValue, 10);
        return isNaN(parsed) ? params.oldValue : parsed;
    },

    // Parse as float
    float: (params) => {
        const parsed = parseFloat(params.newValue);
        return isNaN(parsed) ? params.oldValue : parsed;
    },

    // Parse as uppercase
    uppercase: (params) => {
        return String(params.newValue || '').toUpperCase();
    },
};

// ============================================================================
// CELL EDITOR MAPPING
// ============================================================================

/**
 * Map column type to AG Grid cell editor.
 */
function getCellEditor(type) {
    const editors = {
        'string': 'agTextCellEditor',
        'number': 'agNumberCellEditor',
        'integer': 'agNumberCellEditor',
        'float': 'agNumberCellEditor',
        'boolean': 'agCheckboxCellEditor',
        'date': 'agDateCellEditor',
        'datetime': 'agDateCellEditor',
        'enum': 'agSelectCellEditor',
        'text': 'agLargeTextCellEditor',
    };
    return editors[type] || 'agTextCellEditor';
}

/**
 * Get cell editor params based on column config.
 */
function getCellEditorParams(colDef) {
    const type = colDef._type || 'string';

    switch (type) {
        case 'enum':
            return {
                values: colDef._enumValues || [],
            };
        case 'integer':
            return {
                precision: 0,
                min: colDef._validation?.min,
                max: colDef._validation?.max,
                step: 1,
            };
        case 'number':
        case 'float':
            return {
                precision: colDef._precision ?? 2,
                min: colDef._validation?.min,
                max: colDef._validation?.max,
                step: colDef._step ?? 0.01,
            };
        case 'text':
            return {
                maxLength: colDef._maxLength ?? 1000,
                rows: 5,
                cols: 50,
            };
        default:
            return {};
    }
}

// ============================================================================
// VALIDATION WITH REGISTRY
// ============================================================================

/**
 * Create value parser with validation.
 */
function createValueParser(colDef, validationConfig) {
    const fieldValidation = validationConfig?.[colDef.field] || colDef._validation || {};
    const type = colDef._type || fieldValidation.type || 'string';
    const customParser = colDef._valueParser;

    return (params) => {
        let value = params.newValue;

        // Apply custom parser first if specified
        if (customParser && VALUE_PARSER_REGISTRY[customParser]) {
            value = VALUE_PARSER_REGISTRY[customParser](params);
            params = { ...params, newValue: value };
        }

        // Type coercion
        if (type === 'integer') {
            value = parseInt(value, 10);
            if (isNaN(value)) return params.oldValue;
        } else if (type === 'number' || type === 'float') {
            value = parseFloat(value);
            if (isNaN(value)) return params.oldValue;
        } else if (type === 'boolean') {
            value = Boolean(value);
        }

        // Range validation
        if (fieldValidation.min !== undefined && value < fieldValidation.min) {
            console.warn(`Validation: ${colDef.field} below min ${fieldValidation.min}`);
            return params.oldValue;
        }
        if (fieldValidation.max !== undefined && value > fieldValidation.max) {
            console.warn(`Validation: ${colDef.field} above max ${fieldValidation.max}`);
            return params.oldValue;
        }

        // Pattern validation
        if (fieldValidation.pattern) {
            const regex = new RegExp(fieldValidation.pattern);
            if (!regex.test(String(value))) {
                console.warn(`Validation: ${colDef.field} doesn't match pattern`);
                return params.oldValue;
            }
        }

        // Enum validation
        if (fieldValidation.enumValues && !fieldValidation.enumValues.includes(value)) {
            console.warn(`Validation: ${colDef.field} not in allowed values`);
            return params.oldValue;
        }

        return value;
    };
}

// ============================================================================
// EVENT SANITIZATION (Constraint #2)
// ============================================================================

/**
 * Sanitize AG Grid event for safe transmission to Python.
 * Extracts only serializable data, avoiding circular references.
 */
function sanitizeEvent(event, rowIdField = 'id') {
    if (!event) return null;

    const sanitized = {};

    // Row identification
    if (event.node?.data) {
        sanitized.rowId = String(event.node.data[rowIdField] ?? event.node.id);
        sanitized.rowData = { ...event.node.data };  // Shallow copy
    } else if (event.data) {
        sanitized.rowId = String(event.data[rowIdField] ?? '');
        sanitized.rowData = { ...event.data };
    }

    // Column identification
    if (event.colDef) {
        sanitized.colId = event.colDef.field;
        sanitized.field = event.colDef.field;
    } else if (event.column) {
        sanitized.colId = event.column.getColId();
        sanitized.field = event.column.getColId();
    }

    // Value changes
    if ('oldValue' in event) sanitized.oldValue = event.oldValue;
    if ('newValue' in event) sanitized.newValue = event.newValue;
    if ('value' in event) sanitized.value = event.value;

    // Selection
    if (event.api?.getSelectedRows) {
        try {
            sanitized.selectedRows = event.api.getSelectedRows().map(row => ({ ...row }));
        } catch (e) {
            // Ignore if not available
        }
    }

    // Mouse position (for context menu)
    if (event.event) {
        sanitized.clientX = event.event.clientX;
        sanitized.clientY = event.event.clientY;
    }

    return sanitized;
}

/**
 * Sanitize cell edit event specifically.
 */
function sanitizeCellEditEvent(event, rowIdField = 'id') {
    return {
        rowId: String(event.data?.[rowIdField] ?? event.node?.id ?? ''),
        field: event.colDef?.field ?? event.column?.getColId() ?? '',
        oldValue: event.oldValue,
        newValue: event.newValue,
        rowData: event.data ? { ...event.data } : {},
    };
}

/**
 * Sanitize selection change event.
 */
function sanitizeSelectionEvent(event) {
    const selectedRows = event.api?.getSelectedRows() || [];
    return {
        selectedRows: selectedRows.map(row => ({ ...row })),
        selectedCount: selectedRows.length,
    };
}

// ============================================================================
// CONTEXT MENU
// ============================================================================

/**
 * Build context menu items (Enterprise feature).
 */
function buildContextMenuItems(params, customItems = []) {
    const defaultItems = [
        {
            name: 'Copy Cell',
            shortcut: 'Ctrl+C',
            icon: '<span class="ag-icon ag-icon-copy"></span>',
            action: () => copyToClipboard(params.value),
        },
        {
            name: 'Copy Cell with Header',
            action: () => {
                const header = params.colDef.headerName || params.colDef.field;
                copyToClipboard(`${header}\n${params.value}`);
            },
        },
        {
            name: 'Copy Row',
            action: () => {
                const columns = params.api.getAllDisplayedColumns();
                const headers = columns.map(c => c.getColDef().headerName || c.getColId());
                const values = columns.map(c => params.node.data[c.getColId()]);
                copyToClipboard(`${headers.join('\t')}\n${values.join('\t')}`);
            },
        },
        'separator',
        {
            name: 'Copy Selected Rows',
            disabled: !params.api.getSelectedRows().length,
            action: () => {
                const columns = params.api.getAllDisplayedColumns();
                const headers = columns.map(c => c.getColDef().headerName || c.getColId());
                const rows = params.api.getSelectedRows().map(row =>
                    columns.map(c => row[c.getColId()]).join('\t')
                );
                copyToClipboard(`${headers.join('\t')}\n${rows.join('\n')}`);
            },
        },
        'separator',
        {
            name: 'Export to Excel',
            icon: '<span class="ag-icon ag-icon-excel"></span>',
            action: () => {
                params.api.exportDataAsExcel({
                    fileName: `export_${new Date().toISOString().slice(0, 10)}.xlsx`,
                });
            },
        },
        {
            name: 'Export to CSV',
            icon: '<span class="ag-icon ag-icon-csv"></span>',
            action: () => {
                params.api.exportDataAsCsv({
                    fileName: `export_${new Date().toISOString().slice(0, 10)}.csv`,
                });
            },
        },
        'separator',
        {
            name: 'Reset Columns',
            action: () => {
                params.api.resetColumnState();
                localStorage.removeItem(`ag_grid_state_${params.context?.gridId || 'default'}`);
            },
        },
    ];

    if (customItems.length > 0) {
        return [...customItems, 'separator', ...defaultItems];
    }

    return defaultItems;
}

/**
 * Copy text to clipboard.
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(String(text ?? ''));
    } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = String(text ?? '');
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
}

// ============================================================================
// LOCAL STORAGE PERSISTENCE
// ============================================================================

function saveColumnState(api, gridId) {
    try {
        const state = {
            columns: api.getColumnState(),
            filters: api.getFilterModel(),
        };
        localStorage.setItem(`ag_grid_state_${gridId}`, JSON.stringify(state));
    } catch (err) {
        console.warn('Failed to save column state:', err);
    }
}

function restoreColumnState(api, gridId) {
    try {
        const stateJson = localStorage.getItem(`ag_grid_state_${gridId}`);
        if (!stateJson) return;

        const state = JSON.parse(stateJson);
        if (state.columns) {
            api.applyColumnState({ state: state.columns, applyOrder: true });
        }
        if (state.filters) {
            api.setFilterModel(state.filters);
        }
    } catch (err) {
        console.warn('Failed to restore column state:', err);
    }
}

// ============================================================================
// GLOBAL CONTROLLER (for rx.call_script)
// ============================================================================

/**
 * Global controller exposed for Reflex to call via rx.call_script().
 * Set per grid instance.
 */
window.gridControllers = window.gridControllers || {};

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const AGGridWrapper = ({
    // Data props
    columnDefs = [],
    rowData = [],
    rowIdField = 'id',

    // Configuration
    validationConfig = {},
    gridOptions = {},
    theme = 'ag-theme-balham-dark',
    height = '100%',
    width = '100%',
    gridId = 'default',

    // License
    licenseKey = null,

    // Event handlers (Reflex callbacks) - receive sanitized data
    onCellEdit,
    onRowClick,
    onRowDoubleClick,
    onRowRightClick,
    onSelectionChange,
    onGridReady,

    // Custom context menu items (as registry keys)
    contextMenuItems = [],
}) => {
    // Refs
    const gridRef = useRef(null);
    const editingCellsRef = useRef(new Set());

    // Apply license key on mount
    useEffect(() => {
        applyLicenseKey(licenseKey);
    }, [licenseKey]);

    // =========================================================================
    // COLUMN DEFINITIONS PROCESSING
    // Apply registry patterns to column definitions
    // =========================================================================

    const processedColumnDefs = useMemo(() => {
        return columnDefs.map(col => {
            const processed = { ...col };

            // Cell editor based on type
            if (col._type) {
                processed.cellEditor = getCellEditor(col._type);
                processed.cellEditorParams = getCellEditorParams(col);
            }

            // Apply formatter from registry
            if (col._formatter && FORMATTER_REGISTRY[col._formatter]) {
                processed.valueFormatter = FORMATTER_REGISTRY[col._formatter];
            }

            // Apply renderer from registry
            if (col._renderer && RENDERER_REGISTRY[col._renderer]) {
                processed.cellRenderer = RENDERER_REGISTRY[col._renderer];
            }

            // Apply cell class rules from registry
            if (col._cellClassRules && CELL_CLASS_RULES_REGISTRY[col._cellClassRules]) {
                processed.cellClassRules = CELL_CLASS_RULES_REGISTRY[col._cellClassRules];
            }

            // Apply value parser with validation
            processed.valueParser = createValueParser(col, validationConfig);

            // Clean up internal props
            delete processed._type;
            delete processed._enumValues;
            delete processed._formatter;
            delete processed._renderer;
            delete processed._cellClassRules;
            delete processed._valueParser;
            delete processed._validation;

            return processed;
        });
    }, [columnDefs, validationConfig]);

    // =========================================================================
    // EVENT HANDLERS WITH SANITIZATION
    // =========================================================================

    const handleCellEditingStarted = useCallback((event) => {
        const cellKey = `${event.data?.[rowIdField]}:${event.colDef?.field}`;
        editingCellsRef.current.add(cellKey);
    }, [rowIdField]);

    const handleCellEditingStopped = useCallback((event) => {
        const cellKey = `${event.data?.[rowIdField]}:${event.colDef?.field}`;
        editingCellsRef.current.delete(cellKey);

        // Only fire if value actually changed
        if (event.valueChanged && onCellEdit) {
            const sanitized = sanitizeCellEditEvent(event, rowIdField);
            onCellEdit(sanitized);
        }
    }, [rowIdField, onCellEdit]);

    const handleRowClicked = useCallback((event) => {
        if (onRowClick) {
            const sanitized = sanitizeEvent(event, rowIdField);
            onRowClick(sanitized);
        }
    }, [rowIdField, onRowClick]);

    const handleRowDoubleClicked = useCallback((event) => {
        if (onRowDoubleClick) {
            const sanitized = sanitizeEvent(event, rowIdField);
            onRowDoubleClick(sanitized);
        }
    }, [rowIdField, onRowDoubleClick]);

    const handleSelectionChanged = useCallback((event) => {
        if (onSelectionChange) {
            const sanitized = sanitizeSelectionEvent(event);
            onSelectionChange(sanitized);
        }
    }, [onSelectionChange]);

    // =========================================================================
    // CONTEXT MENU WITH RIGHT-CLICK CALLBACK
    // =========================================================================

    const getContextMenuItems = useCallback((params) => {
        // Notify Python of right-click (sanitized)
        if (onRowRightClick && params.node) {
            const sanitized = sanitizeEvent(params, rowIdField);
            onRowRightClick(sanitized);
        }

        return buildContextMenuItems(params, contextMenuItems);
    }, [rowIdField, onRowRightClick, contextMenuItems]);

    // =========================================================================
    // COLUMN STATE PERSISTENCE
    // =========================================================================

    const handleColumnStateChanged = useCallback(() => {
        const api = gridRef.current?.api;
        if (!api) return;

        // Debounce saves
        if (handleColumnStateChanged.timeout) {
            clearTimeout(handleColumnStateChanged.timeout);
        }
        handleColumnStateChanged.timeout = setTimeout(() => {
            saveColumnState(api, gridId);
        }, 500);
    }, [gridId]);

    // =========================================================================
    // GRID READY
    // =========================================================================

    const handleGridReady = useCallback((params) => {
        // Restore column state
        restoreColumnState(params.api, gridId);

        // Register global controller for this grid
        window.gridControllers[gridId] = {
            jumpToRow: (rowId) => {
                const rowNode = params.api.getRowNode(String(rowId));
                if (rowNode) {
                    params.api.ensureNodeVisible(rowNode, 'middle');
                    params.api.flashCells({
                        rowNodes: [rowNode],
                        flashDuration: 500,
                        fadeDuration: 1000,
                    });
                }
            },
            refresh: () => params.api.refreshCells({ force: true }),
            exportExcel: () => params.api.exportDataAsExcel(),
            exportCsv: () => params.api.exportDataAsCsv(),
            clearFilters: () => params.api.setFilterModel(null),
            resetColumnState: () => {
                params.api.resetColumnState();
                localStorage.removeItem(`ag_grid_state_${gridId}`);
            },
            getSelectedRows: () => params.api.getSelectedRows(),
            selectRows: (rowIds) => {
                params.api.deselectAll();
                rowIds.forEach(id => {
                    const node = params.api.getRowNode(String(id));
                    if (node) node.setSelected(true);
                });
            },
            getApi: () => params.api,
        };

        // Notify Python
        if (onGridReady) {
            onGridReady({ gridId });
        }
    }, [gridId, onGridReady]);

    // Cleanup controller on unmount
    useEffect(() => {
        return () => {
            delete window.gridControllers[gridId];
        };
    }, [gridId]);

    // =========================================================================
    // DEFAULT GRID OPTIONS
    // =========================================================================

    const defaultGridOptions = {
        // Row identification
        getRowId: (params) => String(params.data[rowIdField]),

        // Context for callbacks
        context: { gridId },

        // Selection
        rowSelection: 'multiple',
        suppressRowClickSelection: false,

        // Grouping (Enterprise)
        groupDefaultExpanded: 1,
        autoGroupColumnDef: {
            headerName: 'Group',
            minWidth: 200,
            cellRendererParams: { suppressCount: false },
        },

        // Performance
        animateRows: false,
        suppressRowVirtualisation: false,
        rowBuffer: 20,
        debounceVerticalScrollbar: true,

        // Enterprise features
        enableRangeSelection: true,
        enableRangeHandle: true,
        enableFillHandle: true,
        rowGroupPanelShow: 'onlyWhenGrouping',

        // Clipboard
        enableCellTextSelection: true,
        ensureDomOrder: true,

        // Status bar
        statusBar: {
            statusPanels: [
                { statusPanel: 'agTotalRowCountComponent', align: 'left' },
                { statusPanel: 'agFilteredRowCountComponent', align: 'left' },
                { statusPanel: 'agSelectedRowCountComponent', align: 'center' },
                { statusPanel: 'agAggregationComponent', align: 'right' },
            ],
        },
    };

    const mergedGridOptions = { ...defaultGridOptions, ...gridOptions };

    // =========================================================================
    // RENDER
    // =========================================================================

    return (
        <div className={theme} style={{ height, width }}>
            <AgGridReact
                ref={gridRef}
                columnDefs={processedColumnDefs}
                rowData={rowData}

                {...mergedGridOptions}

                // Event handlers
                onGridReady={handleGridReady}
                onCellEditingStarted={handleCellEditingStarted}
                onCellEditingStopped={handleCellEditingStopped}
                onRowClicked={handleRowClicked}
                onRowDoubleClicked={handleRowDoubleClicked}
                onSelectionChanged={handleSelectionChanged}

                // Column state persistence
                onColumnMoved={handleColumnStateChanged}
                onColumnResized={handleColumnStateChanged}
                onColumnVisible={handleColumnStateChanged}
                onColumnPinned={handleColumnStateChanged}
                onSortChanged={handleColumnStateChanged}
                onFilterChanged={handleColumnStateChanged}

                // Context menu
                getContextMenuItems={getContextMenuItems}
            />
        </div>
    );
};

// Add custom CSS for cell states
const style = document.createElement('style');
style.textContent = `
    .ag-cell-flash {
        background-color: rgba(255, 215, 0, 0.3) !important;
        transition: background-color 0.5s ease-out;
    }
    
    .ag-cell-invalid {
        background-color: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid red !important;
    }
    
    @keyframes cellFlash {
        0% { background-color: rgba(255, 215, 0, 0.5); }
        100% { background-color: transparent; }
    }
`;
document.head.appendChild(style);

export default AGGridWrapper;

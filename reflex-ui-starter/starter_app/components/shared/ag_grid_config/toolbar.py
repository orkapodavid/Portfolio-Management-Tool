"""
Unified grid toolbar with search, generate, export, and layout controls.

This is the recommended way to add a toolbar above AG Grid components.
"""

from typing import Callable

import reflex as rx

from .constants import COMPACT_HEADER_HEIGHT, COMPACT_ROW_HEIGHT
from .export_helpers import _get_export_excel_js


def grid_toolbar(
    storage_key: str,
    page_name: str,
    *,
    # Search
    search_value: rx.Var[str] | None = None,
    on_search_change: Callable | None = None,
    on_search_clear: Callable | None = None,
    # Generate dropdown (optional)
    show_generate: bool = False,
    generate_items: list[str] | None = None,
    on_generate: Callable | None = None,
    is_generate_open: rx.Var[bool] | None = None,
    on_generate_toggle: Callable | None = None,
    # Refresh button (optional)
    show_refresh: bool = False,
    on_refresh: Callable | None = None,
    is_loading: rx.Var[bool] | None = None,
    # Date picker (optional)
    show_date_picker: bool = False,
    on_date_change: Callable | None = None,
    # Export/Layout buttons
    show_excel: bool = True,
    show_save: bool = True,
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
    grid_id: str | None = None,
    show_compact_toggle: bool = False,
    # Status bar (optional)
    last_updated: rx.Var[str] | None = None,
    auto_refresh: rx.Var[bool] | None = None,
    on_auto_refresh_toggle: Callable | None = None,
    # Extra content injected into the left controls area
    extra_left_content: rx.Component | None = None,
) -> rx.Component:
    """
    Unified grid toolbar with search, generate, export, and layout controls.

    This is the recommended way to add a toolbar above AG Grid components.
    It combines the styling of workspace_controls with grid-specific functionality.

    Color scheme:
    - Compact Toggle: Violet (view action) -> Green when active
    - Excel: Green (data export action)
    - Save Layout: Blue (layout action, matches Restore)
    - Restore: Blue (layout action)
    - Reset: Gray (destructive/neutral)

    Visual Layout:
        [Generate] [Export▾] [↻] [🔍 Search...] [📅 Date] | [Compact] | [Excel] | [Save] [Restore] [Reset]


    Args:
        storage_key: Unique localStorage key for grid state persistence
        page_name: Name prefix for export files (e.g., "pnl_full")

        search_value: State var for search text
        on_search_change: Handler for search input changes
        on_search_clear: Handler for clearing search

        show_generate: Show Generate dropdown button
        generate_items: List of menu items for Generate dropdown
        on_generate: Handler when a generate item is clicked (receives item label)
        is_generate_open: State var for dropdown open state
        on_generate_toggle: Handler to toggle dropdown

        show_refresh: Show Refresh button
        on_refresh: Handler for refresh click
        is_loading: State var for loading spinner

        show_date_picker: Show date picker input
        on_date_change: Handler for date changes

        show_excel: Show Excel export button
        show_save: Show Save Layout button
        show_restore: Show Restore button
        show_reset: Show Reset button
        button_size: Radix button size for layout and view buttons
        grid_id: Grid ID for API calls (required for compact toggle)
        show_compact_toggle: Show compact mode toggle button


    Returns:
        Complete toolbar styled with TailwindCSS

    Usage (simple - grid-only controls):
        grid_toolbar(
            storage_key="pnl_grid_state",
            page_name="pnl_full",
            search_value=State.search_text,
            on_search_change=State.set_search,
        )

    Usage (full - with Generate and Refresh):
        grid_toolbar(
            storage_key="pnl_grid_state",
            page_name="pnl_full",
            search_value=State.search_text,
            on_search_change=State.set_search,
            show_generate=True,
            generate_items=["Generate Report", "Refresh Data"],
            on_generate=State.handle_generate,
            is_generate_open=State.is_menu_open,
            on_generate_toggle=State.toggle_menu,
            show_refresh=True,
            on_refresh=State.refresh_data,
            is_loading=State.is_loading,
        )
    """
    safe_key = storage_key.replace("-", "_")

    # =========================================================================
    # LEFT SIDE CONTROLS
    # =========================================================================
    left_controls = []

    # Extra left content (e.g., streaming toggle)
    if extra_left_content is not None:
        left_controls.append(extra_left_content)

    # Generate dropdown button
    if (
        show_generate
        and generate_items
        and on_generate
        and is_generate_open is not None
    ):
        generate_btn = rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("zap", size=12),
                    rx.el.span("Generate", class_name="ml-1.5"),
                    rx.icon("chevron-down", size=10, class_name="ml-1 opacity-70"),
                    class_name="flex items-center",
                ),
                on_click=on_generate_toggle,
                class_name="px-3 h-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded hover:shadow-md transition-all flex items-center shadow-sm",
            ),
            rx.cond(
                is_generate_open,
                rx.el.div(
                    rx.el.div(
                        class_name="fixed inset-0 z-40",
                        on_click=on_generate_toggle,
                    ),
                    rx.el.div(
                        rx.foreach(
                            generate_items,
                            lambda item: rx.el.button(
                                item,
                                on_click=lambda i=item: on_generate(i),
                                class_name="block w-full text-left px-4 py-2 text-[10px] font-bold text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors",
                            ),
                        ),
                        class_name="absolute top-full left-0 mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-100 py-1 z-50",
                    ),
                ),
            ),
            class_name="relative",
        )
        left_controls.append(generate_btn)

    # Excel export button (styled like workspace_controls Export)
    if show_excel:
        excel_btn = rx.el.button(
            rx.el.div(
                rx.icon("file-spreadsheet", size=12),
                rx.el.span("Excel", class_name="ml-1.5"),
                class_name="flex items-center",
            ),
            on_click=rx.call_script(_get_export_excel_js(page_name)),
            class_name="px-3 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold uppercase tracking-widest rounded hover:bg-gray-50 hover:text-green-600 transition-colors shadow-sm flex items-center",
        )
        left_controls.append(excel_btn)

    # Refresh button
    if show_refresh and on_refresh:
        refresh_btn = rx.el.button(
            rx.icon(
                "refresh-cw",
                size=12,
                class_name=rx.cond(
                    is_loading if is_loading is not None else False,
                    "animate-spin",
                    "",
                ),
            ),
            on_click=on_refresh,
            class_name="h-6 w-6 flex items-center justify-center bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm",
        )
        left_controls.append(refresh_btn)

    # Search input
    if search_value is not None and on_search_change is not None:
        search_input = rx.el.div(
            rx.icon("search", size=12, class_name="text-gray-400 mr-1.5 shrink-0"),
            rx.el.input(
                placeholder="Search all columns...",
                value=search_value,
                on_change=on_search_change,
                class_name="bg-transparent text-[10px] font-bold outline-none w-full text-gray-700 placeholder-gray-400",
            ),
            rx.cond(
                search_value != "",
                rx.el.button(
                    rx.icon(
                        "x", size=10, class_name="text-gray-400 hover:text-gray-600"
                    ),
                    on_click=on_search_clear if on_search_clear else lambda: None,
                    class_name="p-0.5 rounded-full hover:bg-gray-100 ml-1 transition-colors",
                ),
            ),
            class_name="flex items-center bg-white border border-gray-200 rounded px-2 h-6 flex-1 max-w-[200px] shadow-sm ml-2 transition-all focus-within:border-blue-400 focus-within:ring-1 focus-within:ring-blue-100",
        )
        left_controls.append(search_input)

    # Date picker - Premium redesign with glassmorphism and micro-interactions
    if show_date_picker and on_date_change:
        date_picker = rx.el.div(
            # Gradient accent bar on hover
            rx.el.div(
                class_name="absolute inset-y-0 left-0 w-0.5 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-l opacity-0 group-hover:opacity-100 transition-opacity duration-200",
            ),
            # Calendar icon with subtle gradient background
            rx.el.div(
                rx.icon(
                    "calendar-days",
                    size=14,
                    class_name="text-blue-500 group-hover:text-blue-600 transition-colors duration-200",
                ),
                class_name="flex items-center justify-center w-7 h-full bg-gradient-to-br from-blue-50 to-indigo-50 border-r border-gray-100 group-hover:from-blue-100 group-hover:to-indigo-100 transition-all duration-200",
            ),
            # Date input with improved styling
            rx.el.input(
                type="date",
                on_change=on_date_change,
                class_name="flex-1 bg-transparent text-[11px] font-semibold text-gray-700 outline-none px-2.5 h-full cursor-pointer appearance-none [&::-webkit-calendar-picker-indicator]:opacity-0 [&::-webkit-calendar-picker-indicator]:absolute [&::-webkit-calendar-picker-indicator]:inset-0 [&::-webkit-calendar-picker-indicator]:w-full [&::-webkit-calendar-picker-indicator]:h-full [&::-webkit-calendar-picker-indicator]:cursor-pointer",
            ),
            # Dropdown chevron indicator
            rx.el.div(
                rx.icon(
                    "chevron-down",
                    size=12,
                    class_name="text-gray-400 group-hover:text-blue-500 transition-colors duration-200 group-hover:translate-y-0.5 transform",
                ),
                class_name="flex items-center justify-center pr-2",
            ),
            class_name="group relative flex items-center bg-white/90 backdrop-blur-sm border border-gray-200/80 rounded-lg h-7 min-w-[140px] shadow-sm hover:shadow-md hover:border-blue-300/60 hover:bg-white transition-all duration-200 overflow-hidden cursor-pointer",
        )
        left_controls.append(date_picker)

    # =========================================================================
    # RIGHT SIDE CONTROLS (Layout buttons)
    # =========================================================================
    layout_buttons = []

    if show_save:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("save", size=12),
                    rx.el.span("Save", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"saveGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm flex items-center",
            )
        )

    if show_restore:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("rotate-ccw", size=12),
                    rx.el.span("Restore", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"restoreGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm flex items-center",
            )
        )

    if show_reset:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("x", size=12),
                    rx.el.span("Reset", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"resetGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-500 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-red-600 transition-colors shadow-sm flex items-center",
            )
        )

    # View group (violet) - compact mode toggle
    view_buttons = []
    if show_compact_toggle and grid_id:
        # JavaScript to toggle compact mode dynamically via AG Grid API
        # Uses React Fiber traversal to reliably access the grid API
        toggle_compact_js = f"""(function() {{
    // Find the specific AG Grid root wrapper by ID (SPA-safe)
    let wrapper = document.querySelector('#{grid_id} .ag-root-wrapper');
    if (!wrapper) {{
        // Fallback to first grid on page
        wrapper = document.querySelector('.ag-root-wrapper');
    }}
    if (!wrapper) {{
        console.error('Grid not found');
        return;
    }}
    
    // Find React fiber with grid API
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) {{
        console.error('Grid API not accessible');
        return;
    }}
    
    let fiber = wrapper[key];
    while (fiber) {{
        if (fiber.stateNode && fiber.stateNode.api) {{
            const api = fiber.stateNode.api;
            
            // Get current row height to determine mode
            const firstRow = api.getDisplayedRowAtIndex(0);
            const currentHeight = firstRow ? firstRow.rowHeight : 42;
            const isCompact = currentHeight < 35;
            
            // Toggle between normal and compact
            const newRowHeight = isCompact ? 42 : {COMPACT_ROW_HEIGHT};
            const newHeaderHeight = isCompact ? 48 : {COMPACT_HEADER_HEIGHT};
            
            api.setGridOption('rowHeight', newRowHeight);
            api.setGridOption('headerHeight', newHeaderHeight);
            api.resetRowHeights();
            
            // Auto-size columns for tighter fit in compact mode
            if (!isCompact) {{
                // Switching TO compact: auto-size columns to content
                api.autoSizeAllColumns();
            }} else {{
                // Switching to normal: size columns to fit grid width
                api.sizeColumnsToFit();
            }}
            
            // Update button visual state
            const btn = document.getElementById('compact-toggle-{grid_id}');
            if (btn) {{
                const textSpan = btn.querySelector('span');
                if (!isCompact) {{
                    // Now compact - show active state (green/active)
                    btn.classList.remove('bg-white', 'text-gray-600', 'hover:bg-violet-50', 'hover:text-violet-600');
                    btn.classList.add('bg-violet-100', 'text-violet-700', 'border-violet-300');
                    if (textSpan) textSpan.textContent = 'Compact ✓';
                }} else {{
                    // Now normal - show default state
                    btn.classList.remove('bg-violet-100', 'text-violet-700', 'border-violet-300');
                    btn.classList.add('bg-white', 'text-gray-600', 'hover:bg-violet-50', 'hover:text-violet-600');
                    if (textSpan) textSpan.textContent = 'Compact';
                }}
            }}
            
            console.log('Compact mode:', !isCompact, 'Row height:', newRowHeight);
            return;
        }}
        fiber = fiber.return;
    }}
    console.error('Grid API not found in fiber tree');
}})();"""
        view_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("rows-3", size=12),
                    rx.el.span("Compact", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                id=f"compact-toggle-{grid_id}",
                on_click=rx.call_script(toggle_compact_js),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-violet-50 hover:text-violet-600 transition-colors shadow-sm flex items-center",
            )
        )

    # =========================================================================
    # ASSEMBLE TOOLBAR
    # =========================================================================
    right_side_items = []

    # View buttons (Compact toggle) - first on right side
    if view_buttons:
        right_side_items.extend(view_buttons)
        # Add divider if there are more items after
        if layout_buttons:
            right_side_items.append(rx.el.div(class_name="w-px h-4 bg-gray-300 mx-2"))

    if layout_buttons:
        right_side_items.extend(layout_buttons)

    # =========================================================================
    # STATUS BAR (optional - shows last updated time and auto-refresh toggle)
    # Premium redesign with glassmorphism, live indicator, and gradient accents
    # =========================================================================
    has_status_bar = last_updated is not None or auto_refresh is not None

    status_bar_content = None
    if has_status_bar:
        status_left = []
        status_right = []

        if last_updated is not None:
            status_left.append(
                rx.el.div(
                    # Live pulse indicator (shows when auto-refresh is active)
                    rx.cond(
                        auto_refresh if auto_refresh is not None else True,
                        rx.el.div(
                            rx.el.div(
                                class_name="absolute inset-0 bg-emerald-400 rounded-full animate-ping opacity-75",
                            ),
                            rx.el.div(
                                class_name="relative w-2 h-2 bg-emerald-500 rounded-full",
                            ),
                            class_name="relative w-2 h-2 mr-2.5",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="w-2 h-2 bg-gray-300 rounded-full",
                            ),
                            class_name="relative w-2 h-2 mr-2.5",
                        ),
                    ),
                    # Clock icon with subtle animation
                    rx.el.div(
                        rx.icon(
                            "clock",
                            size=12,
                            class_name="text-slate-400",
                        ),
                        class_name="mr-1.5",
                    ),
                    # Label and timestamp
                    rx.el.span("Last Updated", class_name="text-slate-400 mr-1.5"),
                    rx.el.span(
                        last_updated,
                        class_name="font-mono font-semibold text-slate-600 bg-gradient-to-r from-slate-100 to-gray-100 px-2 py-0.5 rounded border border-slate-200/60",
                    ),
                    class_name="flex items-center",
                )
            )

        if auto_refresh is not None and on_auto_refresh_toggle is not None:
            status_right.append(
                rx.el.div(
                    # Label with subtle styling
                    rx.el.span(
                        "Auto Refresh",
                        class_name="text-slate-500 font-medium mr-2.5 select-none",
                    ),
                    # Custom styled switch container
                    rx.el.div(
                        rx.switch(
                            checked=auto_refresh,
                            on_change=on_auto_refresh_toggle,
                            size="1",
                        ),
                        class_name="[&_button]:shadow-inner [&_button[data-state='checked']]:bg-gradient-to-r [&_button[data-state='checked']]:from-emerald-500 [&_button[data-state='checked']]:to-teal-500",
                    ),
                    class_name="flex items-center bg-white/60 backdrop-blur-sm border border-slate-200/60 rounded-lg px-2.5 py-1 shadow-sm hover:shadow hover:border-slate-300/80 transition-all duration-200",
                )
            )

        status_bar_content = rx.el.div(
            # Left section
            rx.el.div(*status_left, class_name="flex items-center gap-4"),
            # Right section
            rx.el.div(*status_right, class_name="flex items-center gap-4"),
            # Container with glassmorphism effect
            class_name="flex items-center justify-between px-4 py-1.5 bg-gradient-to-r from-slate-50/95 via-white/90 to-slate-50/95 backdrop-blur-sm border-b border-slate-200/60 text-[11px] font-medium w-full shadow-sm",
        )

    # =========================================================================
    # TOOLBAR ROW
    # =========================================================================
    toolbar_row = rx.el.div(
        rx.el.div(
            *left_controls,
            class_name="flex items-center gap-2 flex-1",
        ),
        rx.el.div(
            *right_side_items,
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between px-3 py-1.5 bg-[#F9F9F9] border-b border-gray-200 shrink-0 h-[40px] w-full",
    )

    # Return with optional status bar
    if has_status_bar:
        return rx.el.div(
            status_bar_content,
            toolbar_row,
            class_name="flex flex-col w-full",
        )

    return toolbar_row

"""
Notification Sidebar State - Enhanced with jump-to-row navigation.

Handles:
- Notification loading (demo data referencing real grids)
- Filtering and pagination
- Mark read, dismiss, simulate
- Navigate to grid + highlight row
"""

import reflex as rx
from typing import List
import random
from datetime import datetime

from starter_app.states.notifications.types import NotificationItem

# Demo notifications — each references a real grid and row
DEMO_NOTIFICATIONS: List[NotificationItem] = [
    {
        "id": "demo-001",
        "header": "Price Alert",
        "ticker": "AAPL",
        "timestamp": "2 min ago",
        "instruction": "AAPL crossed above $195.00 resistance level",
        "type": "alert",
        "read": False,
        "grid_id": "market_data_grid",
        "row_id": "AAPL",
        "route": "/dashboard/analytics",
    },
    {
        "id": "demo-002",
        "header": "FX Spike",
        "ticker": "EUR/USD",
        "timestamp": "5 min ago",
        "instruction": "EUR/USD bid-ask spread widened to 5 pips",
        "type": "warning",
        "read": False,
        "grid_id": "fx_data_grid",
        "row_id": "EUR/USD",
        "route": "/market-data/fx-data",
    },
    {
        "id": "demo-003",
        "header": "Reference Update",
        "ticker": "HSBA.L",
        "timestamp": "10 min ago",
        "instruction": "HSBA.L ISIN updated — verify reference data",
        "type": "info",
        "read": True,
        "grid_id": "reference_data_grid",
        "row_id": "HSBA.L",
        "route": "/market-data/reference-data",
    },
    {
        "id": "demo-004",
        "header": "Volume Spike",
        "ticker": "TSLA",
        "timestamp": "15 min ago",
        "instruction": "Unusual volume detected on TSLA — 3x average",
        "type": "alert",
        "read": False,
        "grid_id": "market_data_grid",
        "row_id": "TSLA",
        "route": "/dashboard/analytics",
    },
    {
        "id": "demo-005",
        "header": "FX Alert",
        "ticker": "GBP/JPY",
        "timestamp": "20 min ago",
        "instruction": "GBP/JPY crossed 190.00 — approaching resistance",
        "type": "alert",
        "read": False,
        "grid_id": "fx_data_grid",
        "row_id": "GBP/JPY",
        "route": "/market-data/fx-data",
    },
    {
        "id": "demo-006",
        "header": "New Listing",
        "ticker": "SAP.DE",
        "timestamp": "30 min ago",
        "instruction": "SAP.DE added to reference universe — verify data",
        "type": "info",
        "read": True,
        "grid_id": "reference_data_grid",
        "row_id": "SAP.DE",
        "route": "/market-data/reference-data",
    },
    {
        "id": "demo-007",
        "header": "Price Alert",
        "ticker": "NVDA",
        "timestamp": "1 hr ago",
        "instruction": "NVDA up 3.2% — new 52-week high approaching",
        "type": "warning",
        "read": False,
        "grid_id": "market_data_grid",
        "row_id": "NVDA",
        "route": "/dashboard/analytics",
    },
    {
        "id": "demo-008",
        "header": "FX Rate Change",
        "ticker": "USD/JPY",
        "timestamp": "1 hr ago",
        "instruction": "USD/JPY change +0.35% — BOJ intervention watch",
        "type": "warning",
        "read": False,
        "grid_id": "fx_data_grid",
        "row_id": "USD/JPY",
        "route": "/market-data/fx-data",
    },
]


# =============================================================================
# SHARED JS HELPERS — extracted from duplicated inline JS
# =============================================================================


def _js_clear_highlight() -> str:
    """JS to clear any existing row highlight state."""
    return """
    window.__pmtHighlightedRow = null;
    if (window.__pmtHighlightInterval) {
        clearInterval(window.__pmtHighlightInterval);
        window.__pmtHighlightInterval = null;
    }
    document.querySelectorAll('.notification-highlight').forEach(el => {
        el.classList.remove('notification-highlight');
    });
    """


def _js_get_grid_api(grid_id: str) -> str:
    """JS to locate the AG Grid API via React Fiber traversal.
    
    Sets local variables `wrapper` and `api`. If not found, early-returns.
    """
    return f"""
    const wrapper = document.querySelector('[id="{grid_id}"] .ag-root-wrapper')
                 || document.querySelector('.ag-root-wrapper');
    if (!wrapper) {{ console.warn('No AG Grid found'); return; }}

    const fiberKey = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!fiberKey) {{ console.warn('React Fiber not found'); return; }}

    let fiber = wrapper[fiberKey];
    let api = null;
    let maxDepth = 50;
    while (fiber && maxDepth-- > 0) {{
        if (fiber.stateNode && fiber.stateNode.api) {{
            api = fiber.stateNode.api;
            break;
        }}
        if (fiber.memoizedProps && fiber.memoizedProps.gridRef && fiber.memoizedProps.gridRef.current) {{
            api = fiber.memoizedProps.gridRef.current.api;
            break;
        }}
        fiber = fiber.return;
    }}
    if (!api) {{ console.warn('AG Grid API not found'); return; }}
    """


def _js_find_and_highlight_row(row_id: str, row_id_key: str) -> str:
    """JS to find a row node, scroll to it, flash, and apply persistent highlight.
    
    Requires `api` to already be set by `_js_get_grid_api()`.
    """
    return f"""
    let node = api.getRowNode('{row_id}');
    if (!node) {{
        api.forEachNode((rowNode) => {{
            if (!node && rowNode.data) {{
                const fieldValue = rowNode.data['{row_id_key}'];
                if (fieldValue !== undefined && String(fieldValue) === String('{row_id}')) {{
                    node = rowNode;
                }}
            }}
        }});
    }}

    if (node) {{
        const actualRowId = node.id || '{row_id}';
        window.__pmtHighlightedRow = {{ grid_id: '{row_id_key}', row_id: actualRowId }};

        api.ensureNodeVisible(node, 'middle');
        api.flashCells({{rowNodes: [node]}});

        const applyHighlight = () => {{
            const highlighted = window.__pmtHighlightedRow;
            if (!highlighted || highlighted.row_id !== actualRowId) return;
            document.querySelectorAll('.ag-row.notification-highlight').forEach(el => {{
                if (el.getAttribute('row-id') !== actualRowId) {{
                    el.classList.remove('notification-highlight');
                }}
            }});
            document.querySelectorAll(`[row-id='${{actualRowId}}']`).forEach(rowEl => {{
                if (!rowEl.classList.contains('notification-highlight')) {{
                    rowEl.classList.add('notification-highlight');
                }}
            }});
        }};

        applyHighlight();
        requestAnimationFrame(applyHighlight);
        setTimeout(applyHighlight, 100);
        setTimeout(applyHighlight, 300);
        setTimeout(applyHighlight, 500);

        if (window.__pmtHighlightInterval) clearInterval(window.__pmtHighlightInterval);
        window.__pmtHighlightInterval = setInterval(() => {{
            const highlighted = window.__pmtHighlightedRow;
            if (!highlighted) {{ clearInterval(window.__pmtHighlightInterval); return; }}
            document.querySelectorAll(`[row-id='${{highlighted.row_id}}']`).forEach(el => {{
                if (!el.classList.contains('notification-highlight')) el.classList.add('notification-highlight');
            }});
        }}, 200);

        console.log('SUCCESS: Jumped to row', actualRowId);
    }} else {{
        console.warn('Row not found for', '{row_id_key}', '=', '{row_id}');
    }}
    """


def _build_jump_js(grid_id: str, row_id: str, row_id_key: str) -> str:
    """Build complete JS to jump to and highlight a row in a grid."""
    return f"""
    (() => {{
        {_js_clear_highlight()}
        window.__pmtHighlightedRow = {{ grid_id: '{grid_id}', row_id: '{row_id}' }};
        {_js_get_grid_api(grid_id)}
        {_js_find_and_highlight_row(row_id, row_id_key)}
    }})()
    """


def _build_navigate_js(
    grid_id: str, row_id: str, row_id_key: str, route: str
) -> str:
    """Build JS to navigate to a row, handling same-page and cross-page cases."""
    return f"""
    (() => {{
        const targetRoute = '{route}';
        const currentPath = window.location.pathname;
        const grid_id = '{grid_id}';
        const row_id = '{row_id}';
        const row_id_key = '{row_id_key}';

        // Check if the specific target grid exists on the current page
        const targetGridWrapper = document.querySelector(`[grid-id="${{grid_id}}"]`) ||
                                   document.querySelector(`#${{grid_id}}`) ||
                                   document.querySelector(`[id="${{grid_id}}"]`);

        const isOnTargetPage = currentPath.endsWith(targetRoute) ||
                                currentPath.includes(targetRoute);
        const anyGridExists = document.querySelector('.ag-root-wrapper') !== null;
        const canJumpDirectly = targetGridWrapper !== null || (isOnTargetPage && anyGridExists);

        console.log('Navigate check:', {{
            currentPath, targetRoute, isOnTargetPage,
            targetGridFound: targetGridWrapper !== null,
            anyGridExists, canJumpDirectly, grid_id, row_id
        }});

        {_js_clear_highlight()}

        if (canJumpDirectly) {{
            // Same page or grid visible: jump directly
            window.__pmtHighlightedRow = {{ grid_id: grid_id, row_id: row_id }};
            {_js_get_grid_api(grid_id)}
            {_js_find_and_highlight_row(row_id, row_id_key)}
        }} else {{
            // Different page: store in sessionStorage for pickup after navigation
            sessionStorage.setItem('__pmtPendingHighlight', JSON.stringify({{
                grid_id: grid_id,
                row_id: row_id,
                row_id_key: row_id_key
            }}));
            console.log('Stored pending highlight in sessionStorage, navigating to', targetRoute);
        }}
    }})()
    """


# =============================================================================
# STATE CLASS
# =============================================================================


class NotificationSidebarState(rx.State):
    """
    State for notification sidebar component.
    Enhanced with jump-to-row navigation.
    """

    # Notification data
    notifications: List[NotificationItem] = []

    # Filter
    notification_filter: str = "all"

    # Infinite scroll vars
    visible_count: int = 20
    batch_size: int = 20
    is_loading_more: bool = False

    # Loading state
    is_loading: bool = False

    # Navigation: pending highlight to be executed on grid_ready
    _pending_grid_id: str = ""
    _pending_row_id: str = ""

    # Computed vars
    @rx.var
    def unread_count(self) -> int:
        """Count of unread notifications."""
        return len([n for n in self.notifications if not n.get("read", False)])

    @rx.var
    def filtered_notifications(self) -> List[NotificationItem]:
        """Filter notifications by type."""
        if self.notification_filter == "all":
            return self.notifications
        return [
            n for n in self.notifications if n.get("type") == self.notification_filter
        ]

    @rx.var
    def sorted_notifications(self) -> List[NotificationItem]:
        """Sort notifications by priority (alerts first)."""
        priority_order = {"alert": 0, "warning": 1, "info": 2}
        return sorted(
            self.filtered_notifications,
            key=lambda n: priority_order.get(n.get("type", "info"), 2),
        )

    @rx.var
    def visible_notifications(self) -> List[NotificationItem]:
        """Return first N sorted notifications for lazy rendering."""
        return self.sorted_notifications[: self.visible_count]

    @rx.var
    def has_more_notifications(self) -> bool:
        """Check if there are more notifications to load."""
        return self.visible_count < len(self.sorted_notifications)

    @rx.var
    def total_notifications_count(self) -> int:
        """Total number of filtered notifications."""
        return len(self.sorted_notifications)

    # Event Handlers
    @rx.event
    def load_notifications(self):
        """Load demo notifications on mount."""
        self.notifications = list(DEMO_NOTIFICATIONS)

    @rx.event
    def set_notification_filter(self, filter_val: str):
        """Change the notification filter and reset visible count."""
        self.notification_filter = filter_val
        self.visible_count = self.batch_size

    @rx.event
    def load_more_notifications(self):
        """Load more notifications when scrolling near bottom."""
        if self.is_loading_more or not self.has_more_notifications:
            return
        self.is_loading_more = True
        self.visible_count += self.batch_size
        self.is_loading_more = False

    @rx.event
    def mark_notification_read(self, notif_id: str):
        """Mark a notification as read."""
        updated = []
        for n in self.notifications:
            if n.get("id") == notif_id:
                n = {**n, "read": True}
            updated.append(n)
        self.notifications = updated

    @rx.event
    def dismiss_notification(self, notif_id: str):
        """Remove a notification."""
        self.notifications = [n for n in self.notifications if n.get("id") != notif_id]

    @rx.event
    def add_simulated_notification(self):
        """Add a simulated notification for testing."""
        new_id = f"sim-{random.randint(1000, 9999)}"
        types = ["alert", "info", "warning"]

        # Rotate through the 3 grids for variety
        grid_options = [
            {"grid_id": "market_data_grid", "row_id": random.choice(["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]), "route": "/dashboard/analytics"},
            {"grid_id": "fx_data_grid", "row_id": random.choice(["EUR/USD", "GBP/USD", "USD/JPY"]), "route": "/market-data/fx-data"},
            {"grid_id": "reference_data_grid", "row_id": random.choice(["AAPL", "MSFT", "7203.T", "HSBA.L"]), "route": "/market-data/reference-data"},
        ]
        selected = random.choice(grid_options)

        headers = ["Price Alert", "Volume Spike", "Risk Warning", "FX Alert"]
        new_notification: NotificationItem = {
            "id": new_id,
            "header": random.choice(headers),
            "ticker": selected["row_id"],
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "instruction": f"Alert triggered for {selected['row_id']}",
            "type": random.choice(types),
            "read": False,
            "grid_id": selected["grid_id"],
            "row_id": selected["row_id"],
            "route": selected["route"],
        }
        self.notifications = [new_notification] + self.notifications

    @rx.event
    def navigate_to_item(self, notif_id: str):
        """Navigate to the grid containing the notification's data row.
        
        Handles both cross-page navigation and same-page jumps.
        Uses sessionStorage for SPA navigation and Python state for full-page nav.
        """
        # Find the notification
        notif = None
        for n in self.notifications:
            if n.get("id") == notif_id:
                notif = n
                break
        if not notif:
            return

        # Mark as read
        self.mark_notification_read(notif_id)

        grid_id = notif.get("grid_id", "market_data_grid")
        row_id = notif.get("row_id", "")
        route = notif.get("route", "/dashboard/analytics")

        # Get the row_id_key for this grid from centralized config
        from starter_app.ag_grid_constants import get_grid_row_id_key
        row_id_key = get_grid_row_id_key(grid_id)

        # Store pending highlight for when grid loads (cross-page navigation)
        self._pending_grid_id = grid_id
        self._pending_row_id = row_id

        script = _build_navigate_js(grid_id, row_id, row_id_key, route)
        return [rx.call_script(script), rx.redirect(route)]

    @rx.event
    def jump_to_row(self, row_id: str, grid_id: str = "market_data_grid", row_id_key: str = ""):
        """Jump to and flash a specific row in the grid, with persistent highlight.
        
        Args:
            row_id: The value to match (e.g., "AAPL", "EUR/USD")
            grid_id: The grid identifier
            row_id_key: The field name to match against
        """
        if not row_id_key:
            from starter_app.ag_grid_constants import get_grid_row_id_key
            row_id_key = get_grid_row_id_key(grid_id)

        script = _build_jump_js(grid_id, row_id, row_id_key)
        return rx.call_script(script)

    @rx.event
    def clear_highlight(self):
        """Clear any persistent row highlight."""
        self._pending_grid_id = ""
        self._pending_row_id = ""

        script = """
        (() => {
            window.__pmtHighlightedRow = null;
            if (window.__pmtHighlightInterval) {
                clearInterval(window.__pmtHighlightInterval);
                window.__pmtHighlightInterval = null;
            }
            if (window.__pmtHighlightObserver) {
                window.__pmtHighlightObserver.disconnect();
                window.__pmtHighlightObserver = null;
            }
            document.querySelectorAll('.ag-row.notification-highlight').forEach(el => {
                el.classList.remove('notification-highlight');
            });
        })()
        """
        return rx.call_script(script)

    @rx.event
    def execute_pending_highlight(self, grid_id: str):
        """Called by grid's on_grid_ready — executes stored highlight if it matches.
        
        Checks two sources:
        1. Python state (_pending_grid_id/_pending_row_id) - for full-page navigation
        2. sessionStorage (__pmtPendingHighlight) - for SPA navigation
        """
        # First try Python state (traditional full-page navigation)
        if self._pending_grid_id and self._pending_grid_id == grid_id:
            row_id = self._pending_row_id
            self._pending_grid_id = ""
            self._pending_row_id = ""
            return self.jump_to_row(row_id, grid_id)

        # Second, check sessionStorage for SPA navigation
        script = f"""
        (() => {{
            const pendingData = sessionStorage.getItem('__pmtPendingHighlight');
            if (!pendingData) {{
                console.log('No pending highlight in sessionStorage');
                return null;
            }}
            
            try {{
                const pending = JSON.parse(pendingData);
                console.log('Found pending highlight:', pending);
                
                if (pending.grid_id !== '{grid_id}') {{
                    console.log('Grid ID mismatch:', pending.grid_id, 'vs', '{grid_id}');
                    return null;
                }}
                
                sessionStorage.removeItem('__pmtPendingHighlight');
                return {{ row_id: pending.row_id, grid_id: pending.grid_id, row_id_key: pending.row_id_key || '' }};
            }} catch (e) {{
                console.error('Error parsing pending highlight:', e);
                return null;
            }}
        }})()
        """
        return rx.call_script(
            script, callback=NotificationSidebarState.handle_sessionStorage_highlight
        )

    @rx.event
    def handle_sessionStorage_highlight(self, result: dict | None):
        """Handle result from sessionStorage check for pending highlight."""
        if result:
            row_id = result.get("row_id", "")
            grid_id = result.get("grid_id", "")
            row_id_key = result.get("row_id_key", "")
            if row_id and grid_id:
                return self.jump_to_row(row_id, grid_id, row_id_key)

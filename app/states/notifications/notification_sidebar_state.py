"""
Notification Sidebar State - Dedicated state for the notification sidebar component.

Handles:
- Notification loading from service
- Filtering and pagination
- Jump-to-row functionality for AG Grid navigation
- Cross-page navigation with row highlighting
"""

import reflex as rx
from typing import List
import logging
import random
from datetime import datetime

from app.states.notifications.types import NotificationItem
from app.ag_grid_constants import get_grid_row_id_key

logger = logging.getLogger(__name__)


class NotificationSidebarState(rx.State):
    """
    State for notification sidebar component.

    Consolidated from UIState notification code to follow the
    same pattern as PerformanceHeaderState.
    """

    # Notification data
    notifications: List[NotificationItem] = []

    # Filter and pagination
    notification_filter: str = "all"
    notification_page: int = 1
    notification_page_size: int = 5

    # Loading state
    is_loading: bool = False

    # Pending highlight for cross-page navigation
    pending_highlight: dict = {}
    
    # Persistent highlight (until page change)
    highlighted_grid_id: str = ""
    highlighted_row_id: str = ""

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
    def total_notification_pages(self) -> int:
        """Total pages based on filtered notifications."""
        count = len(self.filtered_notifications)
        return (count + self.notification_page_size - 1) // self.notification_page_size or 1

    @rx.var
    def paginated_notifications(self) -> List[NotificationItem]:
        """Current page of filtered notifications."""
        start = (self.notification_page - 1) * self.notification_page_size
        end = start + self.notification_page_size
        return self.filtered_notifications[start:end]

    # Event Handlers - Data Loading
    @rx.event
    async def load_notifications(self):
        """
        Load notifications from NotificationService.
        Called on_mount of the notification sidebar.
        """
        self.is_loading = True
        try:
            from app.services import NotificationService

            service = NotificationService()
            raw_notifications = await service.get_notifications(limit=20)

            # Transform to NotificationItem format expected by component
            self.notifications = [
                {
                    "id": int(n.get("id", i + 1)),
                    "header": n.get("title", "Notification"),
                    "ticker": n.get("ticker", n.get("row_id", "N/A")),
                    "timestamp": n.get("time_ago", "Just now"),
                    "instruction": n.get("message", ""),
                    "type": "alert" if n.get("category") == "Alerts" else "info",
                    "read": n.get("is_read", False),
                    # Navigation metadata
                    "module": n.get("module", "Market Data"),
                    "subtab": n.get("subtab", "Market Data"),
                    "row_id": n.get("row_id", ""),
                    "grid_id": n.get("grid_id", "market_data_grid"),
                }
                for i, n in enumerate(raw_notifications)
            ]
            logger.info(f"Loaded {len(self.notifications)} notifications")
        except Exception as e:
            logger.exception(f"Error loading notifications: {e}")
            self.notifications = []
        finally:
            self.is_loading = False

    def _extract_ticker(self, message: str) -> str:
        """Extract ticker symbol from message."""
        if not message:
            return "N/A"
        # Simple extraction - get last word if it looks like a ticker
        words = message.split()
        if words:
            last_word = words[-1].strip(".,!?")
            if last_word.isupper() and 2 <= len(last_word) <= 5:
                return last_word
        return "N/A"

    # Event Handlers - Filtering
    @rx.event
    def set_notification_filter(self, filter_val: str):
        """Change the notification filter."""
        self.notification_filter = filter_val
        self.notification_page = 1

    # Event Handlers - Pagination
    @rx.event
    def next_notification_page(self):
        """Go to next page."""
        if self.notification_page < self.total_notification_pages:
            self.notification_page += 1

    @rx.event
    def prev_notification_page(self):
        """Go to previous page."""
        if self.notification_page > 1:
            self.notification_page -= 1

    # Event Handlers - Notification Actions
    @rx.event
    def mark_notification_read(self, notif_id: int):
        """Mark a notification as read."""
        updated = []
        for n in self.notifications:
            if n.get("id") == notif_id:
                n = {**n, "read": True}
            updated.append(n)
        self.notifications = updated

    @rx.event
    def dismiss_notification(self, notif_id: int):
        """Remove a notification."""
        self.notifications = [n for n in self.notifications if n.get("id") != notif_id]

    @rx.event
    def add_simulated_notification(self):
        """Add a simulated notification for testing."""
        new_id = max([n.get("id", 0) for n in self.notifications], default=0) + 1
        types = ["alert", "info", "warning"]
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META"]
        headers = ["Price Alert", "Volume Spike", "Risk Warning", "Settlement Notice"]
        modules = ["Market Data", "Positions", "PnL", "Risk"]

        ticker = random.choice(tickers)
        new_notification = {
            "id": new_id,
            "header": random.choice(headers),
            "ticker": ticker,
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "instruction": f"Alert triggered for {ticker}",
            "type": random.choice(types),
            "read": False,
            "module": random.choice(modules),
            "subtab": "Market Data",
            "row_id": ticker,  # Use ticker as row_id to match grid's row_id_key
            "grid_id": "market_data_grid",
        }
        self.notifications = [new_notification] + self.notifications

    # Event Handlers - Navigation & Jump to Row
    @rx.event
    def navigate_to_item(self, notif_id: int):
        """
        Navigate to the relevant module/subtab and highlight the row.
        Called when clicking the arrow button on a notification.
        
        Handles both cross-page navigation and same-page jumps.
        """
        # Find the notification
        notification = None
        for n in self.notifications:
            if n.get("id") == notif_id:
                notification = n
                break

        if not notification:
            return

        # Mark as read
        self.mark_notification_read(notif_id)

        grid_id = notification.get("grid_id", "market_data_grid")
        row_id = notification.get("row_id", "0")
        
        # Get the row_id_key for this grid from the centralized config
        row_id_key = get_grid_row_id_key(grid_id)

        # Navigate to the correct module/subtab
        module = notification.get("module", "Market Data")
        subtab = notification.get("subtab", "Market Data")

        # Build route (simplified - uses module slug)
        module_slug = module.lower().replace(" ", "-")
        subtab_slug = subtab.lower().replace(" ", "-")
        target_route = f"/{module_slug}/{subtab_slug}"
        
        # Store pending highlight for when grid loads (for cross-page navigation)
        self.pending_highlight = {
            "grid_id": grid_id,
            "row_id": row_id,
            "row_id_key": row_id_key,
        }

        # CRITICAL: Check for the SPECIFIC target grid, not just any grid
        check_and_navigate_script = f"""
        (() => {{
            const targetRoute = '{target_route}';
            const currentPath = window.location.pathname;
            const grid_id = '{grid_id}';
            const row_id = '{row_id}';
            const row_id_key = '{row_id_key}';
            
            // Check if the SPECIFIC target grid exists on the current page
            // First try grid-id attribute, then check if we're in the right module
            const targetGridWrapper = document.querySelector(`[grid-id="${{grid_id}}"]`) ||
                                       document.querySelector(`#${{grid_id}}`) ||
                                       document.querySelector(`[id="${{grid_id}}"]`);
            
            // Check if we're on the right page for this grid
            const isOnTargetPage = currentPath.endsWith(targetRoute) || 
                                   currentPath.includes(targetRoute);
            
            // Also check if any grid exists (for fallback same-module detection)
            const anyGridExists = document.querySelector('.ag-root-wrapper') !== null;
            
            // The key check: specific grid exists OR (on target page AND any grid exists)
            const canJumpDirectly = targetGridWrapper !== null || (isOnTargetPage && anyGridExists);
            
            console.log('Navigate check:', {{ 
                currentPath, targetRoute, isOnTargetPage, 
                targetGridFound: targetGridWrapper !== null,
                anyGridExists, canJumpDirectly, grid_id, row_id 
            }});
            
            // Clear any existing highlight first
            window.__pmtHighlightedRow = null;
            if (window.__pmtHighlightInterval) {{
                clearInterval(window.__pmtHighlightInterval);
                window.__pmtHighlightInterval = null;
            }}
            document.querySelectorAll('.notification-highlight').forEach(el => {{
                el.classList.remove('notification-highlight');
            }});
            
            // Only jump directly if we can find the target grid or are on the right page
            if (canJumpDirectly) {{
                
                // Store in global state
                window.__pmtHighlightedRow = {{ grid_id: grid_id, row_id: row_id }};
                
                // Find the grid wrapper
                const wrapper = document.querySelector('.ag-root-wrapper');
                if (!wrapper) {{
                    console.warn('No AG Grid found on page');
                    return;
                }}
                
                // Traverse React Fiber to find gridApi
                const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
                if (!key) {{
                    console.warn('React Fiber not found');
                    return;
                }}
                
                let fiber = wrapper[key];
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
                
                if (!api) {{
                    console.warn('AG Grid API not found via React Fiber');
                    return;
                }}
                
                // Find the row - first try getRowNode (fast), then forEachNode (fallback)
                let node = api.getRowNode(row_id);
                
                // If getRowNode failed, try field-based matching using forEachNode
                if (!node) {{
                    console.log('getRowNode failed, trying field-based matching with key:', row_id_key);
                    api.forEachNode((rowNode) => {{
                        if (!node && rowNode.data) {{
                            // Match by the configured row_id_key field
                            const fieldValue = rowNode.data[row_id_key];
                            if (fieldValue !== undefined && String(fieldValue) === String(row_id)) {{
                                node = rowNode;
                            }}
                        }}
                    }});
                }}
                
                if (node) {{
                    // Get the actual row ID from the node for DOM selectors
                    const actualRowId = node.id || row_id;
                    
                    // Store in global state with actual row ID
                    window.__pmtHighlightedRow = {{ grid_id: grid_id, row_id: actualRowId, row_id_key: row_id_key }};
                    
                    // Scroll to row
                    api.ensureNodeVisible(node, 'middle');
                    
                    // Flash cells
                    api.flashCells({{rowNodes: [node]}});
                    
                    // Apply highlight using actual row ID
                    const applyHighlight = () => {{
                        const rowEls = document.querySelectorAll(`[row-id='${{actualRowId}}']`);
                        rowEls.forEach(rowEl => {{
                            rowEl.classList.add('notification-highlight');
                        }});
                    }};
                    
                    applyHighlight();
                    requestAnimationFrame(applyHighlight);
                    setTimeout(applyHighlight, 100);
                    setTimeout(applyHighlight, 300);
                    
                    // Set up periodic reapplication
                    window.__pmtHighlightInterval = setInterval(() => {{
                        const highlighted = window.__pmtHighlightedRow;
                        if (!highlighted) {{
                            clearInterval(window.__pmtHighlightInterval);
                            return;
                        }}
                        const rowEls = document.querySelectorAll(`[row-id='${{highlighted.row_id}}']`);
                        rowEls.forEach(el => {{
                            if (!el.classList.contains('notification-highlight')) {{
                                el.classList.add('notification-highlight');
                            }}
                        }});
                    }}, 200);
                    
                    console.log('SUCCESS: Jumped to row:', actualRowId, 'matched by field:', row_id_key, '=', row_id);
                }} else {{
                    console.warn('Row node not found for', row_id_key, '=', row_id);
                }}
            }} else {{
                // Different page - need to redirect via Python callback for proper SPA navigation
                console.log('Cross-page navigation needed to:', '{target_route}');
                
                // Store highlight data in sessionStorage for use after navigation
                sessionStorage.setItem('__pmtPendingHighlight', JSON.stringify({{
                    grid_id: grid_id,
                    row_id: row_id,
                    row_id_key: row_id_key
                }}));
                
                // Return the target route so Python can handle the redirect with rx.redirect()
                // Note: rx.redirect will automatically add the app base path (/pmt)
                return '{target_route}';
            }}
            
            // Return null if we handled it directly (same-page)
            return null;
        }})()
        """
        
        # Use callback to handle cross-page navigation via rx.redirect()
        return rx.call_script(
            check_and_navigate_script,
            callback=NotificationSidebarState.handle_redirect_callback
        )

    @rx.event
    def handle_redirect_callback(self, target_route: str | None):
        """
        Handle the redirect callback from navigate_to_item.
        If target_route is provided, perform SPA-style redirect using rx.redirect().
        """
        if target_route:
            # Use rx.redirect for proper SPA navigation - this is Reflex's internal mechanism
            return rx.redirect(target_route)

    @rx.event
    def jump_to_row(self, row_id: str, grid_id: str = "market_data_grid", row_id_key: str = ""):
        """
        Jump to and flash a specific row in the grid, with persistent highlight.
        Uses DOM-based React Fiber traversal to access AG Grid API.
        
        Args:
            row_id: The value to match (e.g., "AAPL", "0", "USD/JPY")
            grid_id: The grid identifier
            row_id_key: The field name to match against (e.g., "ticker", "id", "underlying")
                       If empty, uses the centralized config or defaults to direct getRowNode
        
        Persistent highlight is achieved via global window state + periodic reapplication.
        """
        # Store the highlight state for clearing later
        self.highlighted_grid_id = grid_id
        self.highlighted_row_id = row_id
        
        # Get row_id_key from config if not provided
        if not row_id_key:
            row_id_key = get_grid_row_id_key(grid_id)
        
        script = f"""
        (() => {{
            console.log('Jump to row:', '{row_id}', 'in grid:', '{grid_id}', 'using key:', '{row_id_key}');
            
            const row_id = '{row_id}';
            const row_id_key = '{row_id_key}';
            
            // Store in global state for persistence across AG Grid re-renders
            window.__pmtHighlightedRow = {{ grid_id: '{grid_id}', row_id: row_id, row_id_key: row_id_key }};
            
            // Find the grid wrapper via DOM
            // Try specific grid first using ID attribute selector, then fallback
            const wrapper = document.querySelector('[id="{grid_id}"] .ag-root-wrapper') 
                         || document.querySelector('.ag-root-wrapper');
            
            if (!wrapper) {{
                console.warn('No AG Grid found on page');
                return;
            }}
            
            // Traverse React Fiber to find gridApi
            const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
            if (!key) {{
                console.warn('React Fiber not found');
                return;
            }}
            
            let fiber = wrapper[key];
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
            
            if (!api) {{
                console.warn('AG Grid API not found via React Fiber');
                return;
            }}
            
            // Find the row - first try getRowNode (fast), then forEachNode (fallback)
            let node = api.getRowNode(row_id);
            
            // If getRowNode failed, try field-based matching using forEachNode
            if (!node) {{
                console.log('getRowNode failed, trying field-based matching with key:', row_id_key);
                api.forEachNode((rowNode) => {{
                    if (!node && rowNode.data) {{
                        // Match by the configured row_id_key field
                        const fieldValue = rowNode.data[row_id_key];
                        if (fieldValue !== undefined && String(fieldValue) === String(row_id)) {{
                            node = rowNode;
                        }}
                    }}
                }});
            }}
            
            if (node) {{
                // Get the actual row ID from the node for DOM selectors
                const actualRowId = node.id || row_id;
                
                // Update global state with actual row ID
                window.__pmtHighlightedRow.row_id = actualRowId;
                
                // Scroll to row
                api.ensureNodeVisible(node, 'middle');
                
                // Flash cells (temporary animation)
                api.flashCells({{rowNodes: [node]}});
                
                // Apply persistent highlight via DOM class
                const applyHighlight = () => {{
                    const highlighted = window.__pmtHighlightedRow;
                    if (!highlighted || highlighted.row_id !== actualRowId) return;
                    
                    // Clear any existing highlights first
                    document.querySelectorAll('.ag-row.notification-highlight').forEach(el => {{
                        if (el.getAttribute('row-id') !== actualRowId) {{
                            el.classList.remove('notification-highlight');
                        }}
                    }});
                    
                    // Find ALL instances of the row (pinned left, center, pinned right)
                    const rowEls = document.querySelectorAll(`[row-id='${{actualRowId}}']`);
                    rowEls.forEach(rowEl => {{
                        if (!rowEl.classList.contains('notification-highlight')) {{
                            rowEl.classList.add('notification-highlight');
                        }}
                    }});
                }};
                
                // Apply immediately and also on delays for AG Grid async rendering
                applyHighlight();
                requestAnimationFrame(applyHighlight);
                setTimeout(applyHighlight, 100);
                setTimeout(applyHighlight, 300);
                setTimeout(applyHighlight, 500);
                
                // Set up periodic reapplication for scroll persistence
                // This is more reliable than MutationObserver for AG Grid virtualization
                if (window.__pmtHighlightInterval) {{
                    clearInterval(window.__pmtHighlightInterval);
                }}
                window.__pmtHighlightInterval = setInterval(() => {{
                    const highlighted = window.__pmtHighlightedRow;
                    if (!highlighted) {{
                        clearInterval(window.__pmtHighlightInterval);
                        return;
                    }}
                    const rowEls = document.querySelectorAll(`[row-id='${{highlighted.row_id}}']`);
                    rowEls.forEach(el => {{
                        if (!el.classList.contains('notification-highlight')) {{
                            el.classList.add('notification-highlight');
                        }}
                    }});
                }}, 200);  // Check every 200ms
                
                console.log('SUCCESS: Jumped to row:', actualRowId, 'matched by field:', row_id_key, '=', row_id);
            }} else {{
                console.warn('Row node not found for', row_id_key, '=', row_id);
            }}
        }})()
        """
        return rx.call_script(script)
    
    @rx.event
    def clear_highlight(self):
        """
        Clear any persistent row highlight.
        Should be called on page navigation.
        """
        self.highlighted_grid_id = ""
        self.highlighted_row_id = ""
        
        # Remove CSS class from DOM and clear global state
        script = """
        (() => {
            // Clear global state
            window.__pmtHighlightedRow = null;
            
            // Clear periodic interval
            if (window.__pmtHighlightInterval) {
                clearInterval(window.__pmtHighlightInterval);
                window.__pmtHighlightInterval = null;
            }
            
            // Disconnect observer (if any)
            if (window.__pmtHighlightObserver) {
                window.__pmtHighlightObserver.disconnect();
                window.__pmtHighlightObserver = null;
            }
            
            // Remove CSS class
            document.querySelectorAll('.ag-row.notification-highlight').forEach(el => {
                el.classList.remove('notification-highlight');
            });
        })()
        """
        return rx.call_script(script)

    @rx.event
    def execute_pending_highlight(self, grid_id: str):
        """
        Execute pending highlight for a grid.
        Called on grid ready event.
        
        Checks two sources:
        1. Python state (self.pending_highlight) - for full-page navigation
        2. sessionStorage (__pmtPendingHighlight) - for SPA navigation via Next.js Router
        """
        # First try Python state (traditional full-page navigation)
        if self.pending_highlight:
            pending_grid_id = self.pending_highlight.get("grid_id", "")
            if pending_grid_id == grid_id:
                row_id = self.pending_highlight.get("row_id", "")
                self.pending_highlight = {}
                return self.jump_to_row(row_id, grid_id)

        # Second, check sessionStorage for SPA navigation
        # This script runs on the client and checks for pending highlight data
        # Returns an object with row_id and grid_id so callback can access both
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
                
                // Clear the pending data
                sessionStorage.removeItem('__pmtPendingHighlight');
                
                // Return row_id, grid_id, and row_id_key for the callback
                return {{ row_id: pending.row_id, grid_id: pending.grid_id, row_id_key: pending.row_id_key || '' }};
            }} catch (e) {{
                console.error('Error parsing pending highlight:', e);
                return null;
            }}
        }})()
        """
        return rx.call_script(
            script,
            callback=NotificationSidebarState.handle_sessionStorage_highlight
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


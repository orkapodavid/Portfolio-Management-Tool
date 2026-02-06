# Notification System Documentation

This document guides LLM coders on implementing new notification providers in the Portfolio Management Tool.

## Architecture Overview

The notification system uses a **Pub/Sub Registry Pattern**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Domain Services                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ PnLService   │ │ RiskService  │ │ YourService  │            │
│  │ (provider)   │ │ (provider)   │ │ (provider)   │            │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘            │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              NotificationRegistry                           ││
│  │  _providers: {                                              ││
│  │    "pnl": _get_pnl_notifications,                          ││
│  │    "risk": _get_risk_notifications,                        ││
│  │    "yourservice": _get_your_notifications,                 ││
│  │  }                                                          ││
│  └──────────────────────────┬──────────────────────────────────┘│
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NotificationService                           │
│  get_notifications() → aggregates from all registered providers │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              NotificationSidebarState                           │
│  - Loads via NotificationService                                │
│  - Handles filtering, pagination, navigation                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              notification_sidebar.py (UI)                       │
│  - Renders notification cards                                   │
│  - Infinite scroll, filter tabs                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start: Adding a Notification Provider

### Step 1: Create the Provider Function

In your domain service file (e.g., `app/services/yourmodule/your_service.py`):

```python
from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)

# === NOTIFICATION PROVIDERS ===
def _get_your_notifications() -> list[dict]:
    """Notification provider for YourModule."""
    return [
        {
            "id": "your-001",                     # Unique ID (prefix with domain)
            "category": NotificationCategory.ALERTS,  # Use enum
            "title": "Your Alert",                # Short title (displayed as header)
            "message": "Detailed message about the notification",
            "time_ago": "5 mins ago",             # Human-readable timestamp
            "is_read": False,                     # Read status
            "icon": NotificationIcon.ALERT_TRIANGLE,  # Use enum
            "color": NotificationColor.YELLOW,    # Use enum
            "module": "YourModule",               # Target module for navigation
            "subtab": "YourSubtab",               # Target subtab
            "row_id": "IDENTIFIER",               # Row identifier value
            "grid_id": GridId.YOUR_GRID,          # Grid ID from ag_grid_constants
            "ticker": "SYMBOL",                   # Display symbol in card
        },
    ]

# Register at module load
NotificationRegistry.register("yourmodule", _get_your_notifications)
```

### Step 2: Add Grid ID (if new grid)

If your grid doesn't exist in `app/ag_grid_constants.py`, add it:

```python
class GridId(StrEnum):
    # ... existing grids ...
    YOUR_GRID = "your_grid"

# Add to GRID_ROUTES
GRID_ROUTES: dict[str, str] = {
    # ... existing routes ...
    GridId.YOUR_GRID: "/your-module/your-subtab",
}

# Add to GRID_ROW_ID_CONFIG - specify the field used to identify rows
GRID_ROW_ID_CONFIG: dict[str, str | list[str]] = {
    # ... existing config ...
    GridId.YOUR_GRID: "ticker",  # or "id", or your unique field
}
```

### Step 3: Ensure Module Import

Make sure your service is imported so registration runs. If using lazy loading, ensure the import path is referenced.

---

## Notification Schema Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `str` | ✅ | Unique identifier. Use prefix pattern: `"domain-001"` |
| `category` | `NotificationCategory` | ✅ | Use enum: `ALERTS`, `PORTFOLIO`, `NEWS`, `SYSTEM` |
| `title` | `str` | ✅ | Short title displayed as card header |
| `message` | `str` | ✅ | Detailed message body |
| `time_ago` | `str` | ✅ | Human-readable timestamp (e.g., `"5 mins ago"`) |
| `is_read` | `bool` | ✅ | Whether notification has been read |
| `icon` | `NotificationIcon` | ⚪ | Use enum (e.g., `BELL`, `ALERT_TRIANGLE`) |
| `color` | `NotificationColor` | ⚪ | Use enum (e.g., `RED`, `AMBER`, `YELLOW`) |
| `module` | `str` | ✅ | Target module name for navigation |
| `subtab` | `str` | ✅ | Target subtab name |
| `row_id` | `str` | ✅ | Row identifier value to highlight |
| `grid_id` | `str` | ✅ | Grid ID from `GridId` enum |
| `ticker` | `str` | ⚪ | Display symbol in notification card |

---

## Existing Providers Reference

| Provider | File | Grid IDs Used |
|----------|------|---------------|
| `system` | `notification_service.py` | `GridId.MARKET_DATA` |
| `market_data` | `market_data_service.py` | `GridId.MARKET_DATA` |
| `fx` | `market_data_service.py` | `GridId.FX_DATA` |
| `pnl` | `pnl_service.py` | `GridId.PNL_CHANGE` |
| `risk` | `risk_service.py` | `GridId.RISK_MEASURES` |
| `positions` | `position_service.py` | `GridId.POSITIONS` |

---

## Navigation Flow

When a user clicks the navigation arrow on a notification:

1. **Same-page jump**: If the target grid is already visible, JavaScript directly scrolls to the row and applies highlight
2. **Cross-page navigation**: If on a different page:
   - Data is stored in `sessionStorage`
   - SPA navigation via `rx.redirect()`
   - After grid loads, pending highlight is applied

The `row_id_key` (from `GRID_ROW_ID_CONFIG`) determines which field to match against `row_id`.

---

## UI Mapping

The sidebar state transforms raw notifications to UI format:

| Service Field | UI Field | Notes |
|---------------|----------|-------|
| `title` | `header` | Card header |
| `message` | `instruction` | Card body |
| `time_ago` | `timestamp` | Time display |
| `category` → | `type` | `"Alerts"` → `"alert"`, else `"info"` |
| `is_read` | `read` | Read status |
| `ticker` / `row_id` | `ticker` | Fallback |

Card types and colors:
- `alert` → Amber background, black border
- `warning` → Amber background, amber border  
- `info` → Blue background, blue border

---

## API Reference

### NotificationRegistry

```python
from app.services.notifications.notification_registry import NotificationRegistry

# Register a provider
NotificationRegistry.register("name", provider_function)

# Unregister  
NotificationRegistry.unregister("name")

# Get all notifications (aggregated)
all_notifications = NotificationRegistry.get_all_notifications()

# List registered providers
providers = NotificationRegistry.get_provider_names()

# Clear all (testing)
NotificationRegistry.clear()
```

### NotificationService

```python
from app.services import NotificationService

service = NotificationService()

# Get notifications with filters
notifications = await service.get_notifications(
    category="Alerts",     # Optional filter
    unread_only=True,      # Only unread
    limit=20               # Max to return
)

# Create notification programmatically
new_notif = await service.create_notification(
    category="Alerts",
    title="New Alert",
    message="Description",
    module="PnL",
    subtab="PnL Change",
    row_id="AAPL",
    grid_id=GridId.PNL_CHANGE,
)
```

---

## Testing Your Provider

1. Register your provider in your service file
2. Run the app: `uv run reflex run`
3. Open DevTools Console
4. Click the notification bell icon
5. Verify your notifications appear
6. Click navigation arrow to test jump-to-row

### Debug Tips

- Check console for: `Provider 'yourmodule' returned N notifications`
- Verify grid exists on target page before testing navigation
- Ensure `row_id` value exists in grid data
- Check `GRID_ROW_ID_CONFIG` matches your grid's unique field

---

## Example: Full Implementation

```python
# app/services/compliance/compliance_service.py

from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry

def _get_compliance_notifications() -> list[dict]:
    """Generate compliance alerts from database or business logic."""
    # In production, query your database here
    alerts = []
    
    # Example: threshold breach detection
    restricted_stocks = get_restricted_list_breaches()
    for breach in restricted_stocks:
        alerts.append({
            "id": f"compliance-restricted-{breach.ticker}",
            "category": "Alerts",
            "title": "Restricted List Breach",
            "message": f"{breach.ticker} trading detected on restricted list",
            "time_ago": calculate_time_ago(breach.detected_at),
            "is_read": breach.acknowledged,
            "icon": "shield-alert",
            "color": "text-red-500",
            "module": "Compliance",
            "subtab": "Restricted List",
            "row_id": breach.ticker,
            "grid_id": GridId.RESTRICTED_LIST,
            "ticker": breach.ticker,
        })
    
    return alerts

# Register at module import
NotificationRegistry.register("compliance", _get_compliance_notifications)
```

---

## Files Reference

| File | Purpose |
|------|---------|
| [`notification_constants.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/notifications/notification_constants.py) | Enums and constants for type-safe notifications |
| [`notification_registry.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/notifications/notification_registry.py) | Pub/sub registry singleton |
| [`notification_service.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/services/notifications/notification_service.py) | Aggregation service + system notifications |
| [`notification_sidebar_state.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/notification_sidebar_state.py) | Reflex state for UI |
| [`notification_sidebar.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/components/shared/notification_sidebar.py) | UI component |
| [`ag_grid_constants.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/ag_grid_constants.py) | Grid IDs and routes |
| [`types.py`](file:///c:/Users/orkap/Desktop/Programming/Portfolio-Management-Tool/app/states/notifications/types.py) | NotificationItem TypedDict |

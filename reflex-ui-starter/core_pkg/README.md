# Starter Core Package (`core_pkg`)

Pure Python business logic package for the Reflex UI Starter. This package is **completely independent** of the Reflex UI layer — it contains zero Reflex imports and can be tested, reused, or swapped independently.

## Architecture Rule

> **`core_pkg` must NEVER import from `reflex` or `starter_app`.**

This ensures business logic remains portable and testable without any UI framework dependency.

## Structure

```
core_pkg/
├── core/
│   ├── __init__.py          # Package root (version, top-level exports)
│   ├── models/              # Domain models and data classes
│   │   └── __init__.py      # Placeholder — add dataclasses/TypedDicts here
│   ├── services/            # Business logic and orchestration
│   │   ├── __init__.py      # Re-exports all services
│   │   ├── user_service.py
│   │   ├── analytics_service.py
│   │   ├── config_service.py
│   │   ├── notification_service.py
│   │   ├── fx_service.py
│   │   └── reference_data_service.py
│   └── repositories/        # Data access abstractions
│       └── __init__.py      # Placeholder — add repository interfaces here
├── tests_core/              # Unit tests for core package
├── pyproject.toml           # Package configuration
└── README.md                # This file
```

## Services

| Service | Description | Key Methods |
|---------|-------------|-------------|
| `UserService` | User data CRUD and mock generation | `get_users()`, `get_by_id()`, `get_active_count()`, `get_recent_activity()` |
| `AnalyticsService` | Market data, stats, and column schemas | `get_market_data()`, `get_summary_stats()`, `get_column_defs()` |
| `ConfigService` | Application configuration CRUD | `get_config()`, `update_config()`, `reset_to_defaults()` |
| `NotificationConfigService` | Notification preferences and channels | `get_preferences()`, `update_preference()`, `get_enabled_channels()` |
| `FxService` | FX currency pair data + live tick generation | `get_fx_data()`, `generate_tick()` |
| `ReferenceDataService` | Instrument reference data | `get_reference_data()` |

## How the UI Layer Consumes Core

```
core_pkg/core/services/   →   starter_app/services/   →   starter_app/states/
    (business logic)            (thin re-exports)          (Reflex state mgmt)
```

1. **Core services** generate and transform data (pure Python)
2. **App services** re-export core services for convenient importing
3. **Reflex state mixins** call service methods and manage UI state (loading, error, search)

### Example Flow

```python
# core_pkg/core/services/fx_service.py
class FxService:
    def get_fx_data(self) -> list[dict]: ...
    def generate_tick(self, rows: list[dict]) -> list[dict]: ...

# starter_app/services/market_data/__init__.py
from core.services.fx_service import FxService  # re-export

# starter_app/states/market_data/mixins/fx_data_mixin.py
_fx_service = FxService()

class FxDataMixin(rx.State, mixin=True):
    fx_row_data: list[dict] = []           # Reflex state var
    is_loading_fx: bool = False            # UI concern

    @rx.event
    def load_fx_data(self):
        self.fx_row_data = _fx_service.get_fx_data()  # delegates to core
```

## Installation

The core package is installed as an editable dependency:

```toml
# In reflex-ui-starter/pyproject.toml
[tool.uv.sources]
starter-core = { path = "./core_pkg", editable = true }
```

Import from the `core` package:

```python
from core.services import UserService, FxService
```

## Adding a New Service

1. Create `core_pkg/core/services/my_service.py`
2. Export it in `core_pkg/core/services/__init__.py`
3. Create a re-export in `starter_app/services/<module>/__init__.py`
4. Create a state mixin in `starter_app/states/<module>/mixins/my_mixin.py`
5. Compose the mixin into the module's state class

## Testing

```bash
cd core_pkg
python -m pytest tests_core/
```

Tests should cover core services independently without any Reflex dependencies.

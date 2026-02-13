# Starter Core Package

Business logic package for the Reflex UI Starter. This is separated from the UI (`starter_app/`) to keep a clean architecture.

## Structure

```
core_pkg/
├── core/
│   ├── models/          # Domain models and data classes
│   ├── services/        # Business logic and orchestration
│   └── repositories/    # Data access layer
├── tests_core/          # Tests for core package
└── pyproject.toml       # Package configuration
```

## Architecture

- **Models**: Pure Python data classes / TypedDicts. No Reflex or UI dependencies.
- **Services**: Business logic that operates on models. Can depend on repositories.
- **Repositories**: Data access abstractions (DB, API, file, etc).

## Usage

The core package is installed as an editable dependency in the main project:

```bash
# In pyproject.toml
[tool.uv.sources]
starter-core = { path = "./core_pkg", editable = true }
```

Import from the `core` package:

```python
from core.models import User
from core.services import UserService
```

# Shared Business Logic Guide (PyQt + Reflex)

This guide explains how to share the existing business logic (currently in `source/` and `resources/`) between the legacy PyQt app and a new Reflex web app without breaking either UI.

## Objectives

* Keep UI layers (PyQt widgets, Reflex pages/state) thin.
* Keep business logic framework-free and installable as one package.
* Preserve the existing PyQt imports via shims; avoid touching Reflex scaffolding.

---

## 1) Organize Shared Logic

* Create a dedicated core package (example: `pmt_core/`) at the repo root.
* Move/alias domain models, services, data access, and config/resource loaders into this package. Avoid any PyQt/Reflex imports inside it.
* Package `resources/` data via `importlib.resources` to remove hard-coded paths.
* **CRITICAL: Maintain existing `.ini` config format** — the current PMT application uses `.ini` files (`env.ini`, `*.report.ini`). Do not convert to YAML or other formats without an explicit migration plan.
* Add `pyproject.toml` (or `setup.cfg`) so `pmt_core` can be installed in editable mode: `pip install -e .` (root) or `pip install -e ./pmt_core` if using a `src/` layout.
* **Enforce strict dependency direction**: `pmt_core` must be framework-agnostic and must NOT import from `source/` (PyQt) or any UI frameworks.

---

## 2) Integration Steps (Reflex)

* Keep Reflex structure intact (e.g., `app.py`, `state.py`, `pages/`).
* Add dependency: `pip install -e ../pmt_core` (from the Reflex venv) and list `pmt_core` in Reflex requirements.
* In `state.py`, import services from `pmt_core` and call them inside event handlers. Use `asyncio.to_thread` for long-running sync work to keep the event loop responsive.
* **CRITICAL: Reflex must depend ONLY on `pmt_core`**, never directly on `source/*` (PyQt modules). This ensures the web app remains independent of desktop-specific code.
* Add small adapters (e.g., `web_app/adapters/`) to translate Reflex state data to/from `pmt_core` DTOs; keep Reflex pages unchanged.
* Load packaged configs via `importlib.resources.files("pmt_core.resources")` so the same logic works for both apps.

---

## 3) Integration Steps (PyQt)

* Leave existing PyQt files in `source/` untouched for now.
* Add thin shim modules in `source/` (same module paths the UI already imports) that re-export functions/classes from `pmt_core`. This preserves old import paths.
* **Ensure one-way dependency**: PyQt (`source/`) imports from `pmt_core` via shims, but `pmt_core` must NEVER import from `source/`. This keeps `pmt_core` framework-agnostic and reusable.
* Update PyInstaller spec to include `pmt_core` package if/when you move code physically.

---

## 4) Separation of Concerns Best Practices

* **Core must be framework-agnostic:** no `PyQt5`, `reflex`, or UI types. Depend only on standard lib + neutral libs (pandas, numpy, etc.).
* **Define DTOs/payloads in core** (dataclasses or Pydantic). Do UI-to-DTO mapping in adapters near each UI.
* **Inject I/O** (DB handles, Bloomberg sessions, file paths) via parameters; avoid global UI-coupled singletons.
* **Keep logging in core generic** (`logging.getLogger("pmt_core")`); let each UI configure handlers/formatters.
* **Test core separately;** keep UI smoke tests light by mocking the core layer.

---

## 5) Example Folder Layout

```text
basket-sender-apac/
├── pmt_core/                # new shared package (installable)
│   ├── pyproject.toml
│   └── pmt_core/
│       ├── __init__.py
│       ├── models/          # enums, dataclasses
│       ├── services/        # pricing, reporting, EMSX glue
│       ├── repositories/    # DB/file access wrappers
│       ├── resources/       # packaged configs/templates
│       └── utilities/       # config/logging helpers (UI-free)
├── source/                  # existing PyQt app (UI + shims)
│   ├── gui/                 # UI only
│   ├── adapters/            # NEW: UI -> core bridges
│   ├── pricers/, reports/, utilities/  # keep interfaces, re-export core
│   └── main.py
├── web_app/                 # Reflex app (keep native structure)
│   ├── rxconfig.py
│   ├── app.py
│   ├── state.py             # imports core services
│   ├── pages/
│   └── adapters/            # Reflex -> core bridges
└── resources/               # legacy data; migrate into pmt_core/resources as needed

```

---

## 6) Import Patterns

```python
# pmt_core/services/pricing.py (framework-free)
def price_basket(req: BasketRequest) -> BasketQuote:
    ...

# source/pricers/basket.py (PyQt shim)
from pmt_core.services.pricing import price_basket
__all__ = ["price_basket"]

# web_app/state.py (Reflex)
import asyncio
import reflex as rx
from pmt_core.services.pricing import price_basket

class AppState(rx.State):
    basket_form: dict = {}
    quote: dict = {}

    async def submit(self):
        # Use to_thread for sync business logic to avoid blocking Reflex
        quote = await asyncio.to_thread(price_basket, self.basket_form)
        self.quote = quote

```

---

## 7) Resource Loading Example

_**IMPORTANT**: The existing PMT application uses **`.ini` configuration files** such as `resources/config/env.ini` and `resources/config/report/**/*.report.ini`. The YAML-based example below is **illustrative only** to demonstrate `importlib.resources` usage. When implementing `pmt_core` config loaders, you must:_

- _Preserve the existing `.ini` format and parsing logic._
- _Use `importlib.resources` to access packaged `.ini` files instead of hard-coded paths._
- _Only consider YAML or other formats if you implement an explicit, backward-compatible migration strategy._

```python
from importlib.resources import files
import configparser  # For .ini files

def load_env_config():
    """
    Example: Load env.ini config using importlib.resources.
    Real implementation should use configparser for .ini format.
    """
    cfg_path = files("pmt_core.resources.config").joinpath("env.ini")
    config = configparser.ConfigParser()
    with cfg_path.open() as f:
        config.read_file(f)
    return config

# YAML example (illustrative only - not for actual use unless migrating)
import yaml

def load_env_config_yaml_example():
    """
    YAML example - DO NOT use unless you have migrated from .ini to YAML.
    """
    cfg_path = files("pmt_core.resources.config").joinpath("env.yaml")
    with cfg_path.open() as f:
        return yaml.safe_load(f)

```

---

## 8) Versioning and Stability

* Treat `pmt_core` as the single source of truth; bump its version on interface changes and pin versions per app.
* **Strict dependency direction**: UI layers (PyQt in `source/`, Reflex web app) depend on `pmt_core` via imports and adapters. `pmt_core` never imports from UI layers or framework-specific code.
* When moving modules, keep old PyQt import paths alive via re-exporting shims to avoid breaking the existing UI.
* **Framework independence**: `pmt_core` must remain installable and testable without PyQt5, Reflex, or any UI framework dependencies.

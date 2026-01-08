I have transcribed the content of the images into the Markdown document below. I've maintained the original hierarchy, code formatting, and folder structure as presented in your screenshots.

---

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
* Add `pyproject.toml` (or `setup.cfg`) so `pmt_core` can be installed in editable mode: `pip install -e .` (root) or `pip install -e ./pmt_core` if using a `src/` layout.

---

## 2) Integration Steps (Reflex)

* Keep Reflex structure intact (e.g., `app.py`, `state.py`, `pages/`).
* Add dependency: `pip install -e ../pmt_core` (from the Reflex venv) and list `pmt_core` in Reflex requirements.
* In `state.py`, import services from `pmt_core` and call them inside event handlers. Use `asyncio.to_thread` for long-running sync work to keep the event loop responsive.
* Add small adapters (e.g., `web_app/adapters/`) to translate Reflex state data to/from `pmt_core` DTOs; keep Reflex pages unchanged.
* Load packaged configs via `importlib.resources.files("pmt_core.resources")` so the same logic works for both apps.

---

## 3) Integration Steps (PyQt)

* Leave existing PyQt files in `source/` untouched for now.
* Add thin shim modules in `source/` (same module paths the UI already imports) that re-export functions/classes from `pmt_core`. This preserves old import paths.
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

```python
from importlib.resources import files
import yaml

def load_env_config():
    # Path-safe way to access data inside the core package
    cfg_path = files("pmt_core.resources.config").joinpath("env.yaml")
    with cfg_path.open() as f:
        return yaml.safe_load(f)

```

---

## 8) Versioning and Stability

* Treat `pmt_core` as the single source of truth; bump its version on interface changes and pin versions per app.
* Avoid circular deps: UI layers depend on core, never the reverse.
* When moving modules, keep old PyQt import paths alive via re-exporting shims to avoid breaking the existing UI.

---

**Would you like me to help you draft the `pyproject.toml` or the specific shim modules for your `source/` directory?**
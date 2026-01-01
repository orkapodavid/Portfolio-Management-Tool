## LLM Prompts for Preparing PMT PyQt ↔ Reflex Integration

### How to Use This File

- **Purpose**: These prompts are designed for use in the **PMT PyQt repository**, after you have copied this Reflex app repo into it as a subfolder (for example: `web_app/` or `Portfolio-Management-Tool/`).
- **Flow**: Run the prompts in order with an LLM coder that has access to the full PMT PyQt repo (including `source/`, `resources/`, and this subfolder) so it can read and modify files there.
- **Constraint**: The prompts focus on creating a shared core package (`pmt_core`) and wiring PyQt + Reflex to it, following the guidance in `docs/PMT Architecture Map.md` and `docs/integration_with_pyqt.md`.

### Architectural Assumptions (Read First)

- **Single shared core**: Treat `pmt_core` as the **only shared business-logic package**. Both PyQt and Reflex should call into `pmt_core`; they should not depend directly on each other.
- **Dependency direction**: `pmt_core` **must not import** from `source/` (PyQt) or any UI frameworks (`PyQt5`, `reflex`). UI layers depend on `pmt_core` via shims/adapters, never the reverse.
- **Config format and location**: The existing app uses **`.ini` configs** (for example `resources/config/env.ini`, `resources/config/report/**/*.report.ini`). Any YAML examples in the docs are **illustrative only**; do not change formats unless you implement an explicit, backward-compatible migration.
- **Interpreting the architecture map**: When `PMT Architecture Map.md` talks about reusing `source/models/*`, `source/reports/*`, and `resources/config/report` directly (e.g., via a `reflex_app/` folder), interpret that as **conceptual guidance**. In this integration, those concepts are surfaced through `pmt_core.services` rather than new code that depends directly on `source/*` from the web app.
- **Report classes and UI separation**: Existing `ReportClass` subclasses in `source/reports/*` often mix UI and data logic. As you refactor, split **UI-free behavior** (data extraction, merges, rules, etc.) into `pmt_core` and keep UI-specific pieces (like `create_ui_tab`) in PyQt modules that call `pmt_core`, not the other way around.

---

### Prompt 1 – Understand the Existing PyQt PMT and New Reflex App

```text
You are helping me integrate an existing PyQt5-based Portfolio Management Tool (PMT) with a new Reflex web app that I have copied into this repo as a subfolder.

1) **Context & Goals**
- The legacy desktop app is a PyQt5 application with a structure similar to:
  - `main.py`, `main.spec`
  - `resources/config/env.ini` and `resources/config/report/**/*.report.ini`
  - `source/` with subfolders:
    - `bloomberg/` (EMSX + ref data services)
    - `gui/` (Qt UI, widgets, workers, actions)
    - `models/` (config + typed models/enums, `class_mapping.py`, `class_model_config.py`, `class_report.py`)
    - `reports/` (one folder per dashboard section: trading, position, pnl, market_data, compliance, analytics, recon, report, event, operation)
    - `utilities/` (config readers, DB helpers, logging)
    - `workers/` (QThread workers)
    - `pricers/` (pricing engines)
- The new Reflex app repo has been copied into this PMT repo as a subfolder (for example `Portfolio-Management-Tool/` or `web_app/`), and it contains its own `app/`, `pages/`, `states/`, `docs/`, and `rxconfig.py`.
- We want to **share business logic** between PyQt and Reflex without breaking either UI, by following the ideas in `docs/PMT Architecture Map.md` and `docs/integration_with_pyqt.md`.

2) **What to Do Now**
- Carefully read the following docs in this repo:
  - `docs/PMT Architecture Map.md` (explains how tabs, reports, workers, and config files are wired in the PyQt app).
  - `docs/integration_with_pyqt.md` (explains how to create a shared `pmt_core` package and integrate both PyQt and Reflex with it).
- Then summarize for me, in your own words:
  - a) How data flows from configuration (`resources/config/report/**/*.report.ini`) through `ReportClass` subclasses into the PyQt UI.
  - b) How a shared `pmt_core` package is supposed to be structured and used by both PyQt and Reflex.
  - c) Any key constraints we must preserve (e.g., keeping old PyQt import paths working, using `importlib.resources` instead of hard-coded file paths, making `pmt_core` framework-agnostic).

3) **Output**
- Provide a concise, bullet-point-style summary of (a)–(c).
- Call out any open questions or assumptions that you will use later when refactoring.
```

---

### Prompt 2 – Design the `pmt_core` Package Layout

```text
You have already read and summarized `docs/PMT Architecture Map.md` and `docs/integration_with_pyqt.md`.

1) **Goal**
Design a concrete folder and module layout for a new shared package called `pmt_core` that will live at the root of this PMT repo and be installable in editable mode.

2) **Constraints & Guidance** (from the docs)
- `pmt_core` should:
  - Be framework-agnostic (no PyQt5 or Reflex imports).
  - Contain domain models, services, data access, and config/resource loaders.
  - Use `importlib.resources` for configuration and templates.
  - Define DTOs/payloads as dataclasses or Pydantic models.
  - Keep I/O injected (DB handles, Bloomberg sessions, file paths passed in rather than global UI singletons).
- The existing PyQt structure includes:
  - `source/models/` (e.g., `class_mapping.py`, `class_model_config.py`, `class_report.py`, enums).
  - `source/reports/` (ReportClass subclasses per dashboard/tab).
  - `source/utilities/` (config readers, DB helpers, logging, etc.).
  - `source/pricers/` and `source/workers/` (to be selectively exposed from core as needed).
- The Reflex app will eventually import `pmt_core` services directly from this shared package.

3) **What to Propose**
- Propose a **concrete directory structure** for `pmt_core`, similar in spirit to the example in `docs/integration_with_pyqt.md`, but tailored to the actual PMT features:
  - Suggest which pieces from `source/models`, `source/reports`, `source/utilities`, `source/pricers`, and `resources/` belong in:
    - `pmt_core/models/`
    - `pmt_core/services/`
    - `pmt_core/repositories/`
    - `pmt_core/resources/`
    - `pmt_core/utilities/`
- For each major subpackage, describe:
  - What responsibilities it will have.
  - Which existing modules or concepts it will absorb.
  - How its public API should look (module-level functions, service classes, etc.).

4) **Output**
- Provide the proposed directory tree using a `text` block.
- Provide a short explanation (a few bullets) per top-level subpackage to justify the design.
```

---

### Prompt 3 – Create the `pmt_core` Package Skeleton (No Behavior Changes Yet)

```text
You have an agreed design for the `pmt_core` directory layout.

1) **Goal**
Create a **skeleton implementation** of the `pmt_core` package in this PMT repo that:
- Matches the agreed directory layout.
- Contains minimal `__init__.py` and placeholder modules with docstrings and TODOs.
- Does **not** change any existing behavior yet (no logic movement, only stubs and structure).

2) **Actions**
Working in this repo:
- Create a `pmt_core/` folder at the repo root (or under `./pmt_core/pmt_core/` if you decide to use a nested `pyproject.toml` as in the integration guide).
- Add the minimal `pyproject.toml` (or equivalent) needed so `pmt_core` can be installed via `pip install -e .` or `pip install -e ./pmt_core`.
- For each subpackage (e.g., `models`, `services`, `repositories`, `resources`, `utilities`):
  - Create `__init__.py` with a short docstring explaining its purpose.
  - Create placeholder modules where we know we will later move logic (for example, `reporting.py`, `pricing.py`, `env_config.py`, `database.py`).
  - In each placeholder module, add just enough structure (empty classes/functions and TODO comments) so future refactors have clear targets.

3) **Constraints**
- Do not move or delete any existing code in `source/` or `resources/` yet.
- Do not change PyQt or Reflex code behavior at this stage.
- Keep your changes focused on creating the new `pmt_core` package and its metadata.

4) **Output**
- Show me the new `pmt_core` directory tree.
- Summarize any decisions you made about packaging layout or configuration.
```

---

### Prompt 4 – Identify and Extract Shared Domain Models and Config Loading

```text
Now that `pmt_core` exists as a skeleton, we want to start moving the **most central, UI-agnostic pieces** into it.

1) **Goal**
Refactor the codebase so that core domain models and configuration loaders live in `pmt_core`, while PyQt and Reflex both depend on them.

2) **What to Analyze**
- In `source/models/`, inspect:
  - `class_report.py` (ReportClass base + Merge/Rule config).
  - `class_model_config.py` (global ModelConfig cache and loader).
  - `class_mapping.py` (mapping from `ReportType` to concrete report classes).
  - All `enum_*.py` files (enums for report types, dashboards, etc.).
- In `source/utilities/`, inspect:
  - `config_reader_env.py` and `config_reader_model.py`.
  - Any other config or model helpers closely tied to `resources/config/`.
- In `resources/config/`, note:
  - How `env.ini` and `report/**/*.report.ini` are read and used.
  - **IMPORTANT**: The existing system uses `.ini` format configs, not YAML. Preserve this format when building `pmt_core` config loaders.

3) **Refactor Plan**
- Propose a specific plan to:
  - Move **framework-agnostic** types (enums, data classes, configuration schemas) into `pmt_core.models`.
  - Move config loader logic into `pmt_core.utilities` / `pmt_core.resources` using `importlib.resources` to access packaged `.ini` configs (maintaining the existing format).
  - Keep PyQt-specific pieces in `source/` (e.g., anything importing PyQt, GUI classes, QThreads) and have them **import from `pmt_core` instead of duplicating logic**.
  - **CRITICAL**: Ensure `pmt_core` does NOT import from `source/` to avoid circular dependencies and maintain framework independence.
- Identify any circular dependency risks between `pmt_core` and `source/` and propose how to avoid them.

4) **Output**
- Provide a step-by-step refactor plan with file-level granularity (which modules/functions/classes move where, which stay and become shims).
- Clearly mark steps as "safe to automate now" vs. "requires human/LLM review".
- Confirm the plan maintains `.ini` config format and `pmt_core` does not depend on `source/`.
```

---

### Prompt 5 – Implement the First Wave of Moves into `pmt_core` (Models + Config)

```text
Using the agreed refactor plan for shared models and config loading, start implementing the changes.

1) **Goal**
Perform the **first wave of actual code moves** into `pmt_core`, focusing on domain models and configuration loading, while keeping the PyQt app fully working.

2) **Actions**
- Move or copy the selected framework-agnostic pieces from `source/models` and `source/utilities` into the appropriate `pmt_core` modules.
- Replace hard-coded file path access for configuration with `importlib.resources` inside `pmt_core` (for example, accessing packaged `env.ini` and `report/*.ini` configs via `files("pmt_core.resources.config")`).
- **Maintain `.ini` format**: Do not convert configs to YAML or other formats unless there is an explicit migration plan with backward compatibility.
- In the PyQt app (`source/`):
  - Update imports to pull shared models and config loaders from `pmt_core`.
  - Where necessary, create thin shim modules in `source/` that simply re-export symbols from `pmt_core` to preserve existing import paths (as suggested in `docs/integration_with_pyqt.md`).
  - **Ensure shims do not leak back**: PyQt modules can import from `pmt_core`, but `pmt_core` must NEVER import from `source/`.

3) **Constraints**
- Do not break PyQt runtime behavior; preserve public interfaces expected by the UI and workers.
- Do not yet change the Reflex app; we will wire it up to `pmt_core` in a later step.
- **Maintain strict dependency direction**: `pmt_core` depends only on standard libraries and neutral packages (pandas, numpy, etc.), not on PyQt or `source/`.

4) **Output**
- Show diffs or summarize which modules were moved or updated.
- Call out any risky changes or places that may need manual test validation.
- Confirm that `pmt_core` does not import from `source/` and config format remains `.ini`.
```

---

### Prompt 6 – Expose Reporting and Pricing Services from `pmt_core`

```text
After domain models and configuration loading are in `pmt_core`, we want to expose high-level services that both PyQt and Reflex can call.

1) **Goal**
Identify and implement service APIs in `pmt_core` that encapsulate reporting and pricing flows, so UIs only call these services rather than low-level utilities.

2) **What to Analyze**
- In `source/reports/`, look at how `ReportClass` subclasses:
  - Implement `create_ui_tab`, `extract_report_data`, `merge_report_data`, and `process_report_data`.
  - Interact with `utilities/database_reader.py`, `worker_report.py`, and other helpers.
- In `source/pricers/` and any `common_pricer` helpers referenced in the architecture map, identify pricing entry points that are UI-agnostic.

3) **Refactor**
- Design `pmt_core.services.reporting` and `pmt_core.services.pricing` modules that:
  - Provide functions like `run_report(report_type, params)` and `price_basket(request)` that return structured DTOs.
  - Extract and reimplement **UI-free behavior** from existing `ReportClass` subclasses (data extraction, merges, rules logic) into `pmt_core`.
  - **CRITICAL**: Do NOT import existing `ReportClass` subclasses from `source/reports/*` into `pmt_core`. Instead, move the business logic into `pmt_core` and leave UI-specific methods (like `create_ui_tab`) in PyQt modules that call into `pmt_core` services.
  - Similarly, extract pricing logic from `source/pricers/` into `pmt_core.services.pricing` without importing PyQt-dependent modules.
- Implement these services in `pmt_core`, ensuring the package remains framework-agnostic (no imports from `source/` or any UI frameworks).
- Update PyQt entry points (buttons, workers) to call the new `pmt_core` services via shims.

4) **Output**
- Describe the new service APIs and show where PyQt will call them.
- Explicitly list which UI-specific logic remains in `source/` and does not move to `pmt_core`.
- Confirm that `pmt_core` does not import from `source/` at any point.
```

---

### Prompt 7 – Wire the Reflex App to `pmt_core` Without Breaking Its Structure

```text
Now integrate the Reflex web app (the subfolder you copied into this repo) with the new `pmt_core` services.

1) **Goal**
Update the Reflex app so that its state and pages call into `pmt_core` for business logic, matching the recommendations in `docs/integration_with_pyqt.md`.

2) **Actions**
- In the Reflex app subfolder (for example `Portfolio-Management-Tool/` or `web_app/`):
  - Locate `rxconfig.py`, `app.py`, `states/`, and `pages/`.
  - Identify the places where the app needs to:
    - Fetch report-style data.
    - Run pricing or analytics.
    - Load configuration or metadata for tables (column labels, formats, etc.).
- Implement state methods (in `states/`) that:
  - Import `pmt_core` services (for example, `from pmt_core.services.reporting import run_report`).
  - **CRITICAL**: Import ONLY from `pmt_core`, never directly from `source/*` (PyQt modules).
  - Call them using `asyncio.to_thread` if the services are synchronous, as suggested in `docs/integration_with_pyqt.md`.
  - Map DTOs returned by `pmt_core` into Reflex-friendly data structures for components.
- If helpful, create a `web_app/adapters/` or equivalent directory (inside the Reflex subfolder) to handle DTO ↔ UI mapping without polluting `pmt_core` with Reflex types.

3) **Constraints**
- Do not change the overall Reflex project structure (keep `app.py`, routing, and core patterns intact).
- Do not introduce any PyQt or desktop-specific code into the Reflex app.
- **Do not import from `source/*`** — all business logic must come through `pmt_core`.

4) **Output**
- Show the key updated state methods and how they call `pmt_core`.
- Provide a brief explanation of the DTO ↔ Reflex mapping strategy you implemented.
- Confirm that the Reflex app depends only on `pmt_core`, not on `source/` modules.
```

---

### Prompt 8 – Maintain PyQt Import Compatibility via Shims

```text
We have moved some logic into `pmt_core` and wired Reflex to it. Now we need to ensure the PyQt app remains stable and maintainable.

1) **Goal**
Ensure that all existing PyQt modules (UI files, workers, pricers) still work and that their imports remain valid, even after refactoring logic into `pmt_core`.

2) **Actions**
- Search through `source/` (especially `gui/`, `reports/`, `pricers/`, `workers/`) for imports that reference modules you have refactored.
- For each such import:
  - Decide whether to update the import to point directly to `pmt_core`.
  - Or, if this risks breaking many files, create a thin shim module in `source/` that re-exports the corresponding symbols from `pmt_core` (for example `source/pricers/basket.py` re-exporting `pmt_core.services.pricing.price_basket`).
- **CRITICAL**: Confirm that no module in `pmt_core` imports from `source/` (to avoid circular dependencies and keep `pmt_core` UI-agnostic and framework-independent).
- Verify the dependency direction is strictly one-way: `source/` → `pmt_core`, never the reverse.

3) **Output**
- Provide a list of shim modules you created and the symbols they re-export.
- Summarize any import changes you made and any areas that might need extra manual testing.
- Explicitly confirm that `pmt_core` does not import from `source/` anywhere in the codebase.
```

---

### Prompt 9 – Add Minimal Tests for `pmt_core` Contracts

```text
To improve safety of future refactors, we want basic tests around `pmt_core` contracts.

1) **Goal**
Create a small but meaningful test suite focused on `pmt_core` models and services.

2) **Actions**
- Decide on a test framework (pytest is preferred if not already used).
- Add tests that:
  - Validate configuration loading (e.g., that `.ini` env and report configs can be loaded via `importlib.resources` and parsed into the expected models).
  - Exercise key service entry points (e.g., `run_report`, `price_basket`) in a way that does not require a full DB or Bloomberg connection (use mocks or lightweight fakes if necessary).
  - **Confirm that `pmt_core` does not import PyQt or Reflex** by importing all `pmt_core` modules in a test environment without these dependencies installed.
  - Verify dependency direction: ensure tests can import `pmt_core` without needing `source/` or any UI frameworks.
- Organize tests in a directory like `tests/pmt_core/` at the repo root.

3) **Output**
- Show test file names and a brief explanation of what each covers.
- Mention any external dependencies (DB, Bloomberg, etc.) that you mocked or abstracted.
- Confirm that `pmt_core` tests run independently of PyQt and Reflex.
```

---

### Prompt 10 – Final Integration Review and Cleanup

```text
Finally, review the integrated PyQt + Reflex + pmt_core setup for consistency and maintainability.

1) **Goal**
Ensure the repo is in a clean state where:
- `pmt_core` is the single source of truth for shared business logic.
- PyQt and Reflex depend on `pmt_core` but not on each other.
- Configuration and resource loading are stable and path-safe.

2) **Actions**
- Review the overall directory structure of the repo (root, `pmt_core`, `source`, `resources`, Reflex subfolder).
- Check for any remaining duplicated business logic between PyQt and Reflex and propose consolidations in `pmt_core`.
- Confirm that logging, error handling, and configuration patterns are consistent and documented in code docstrings.
- Suggest any small refactors or comments that would make future maintenance easier, without introducing new frameworks or major redesigns.

3) **Output**
- Provide a short report summarizing:
  - The final architecture (1–2 paragraphs).
  - Any remaining technical debt or TODOs.
  - Recommended next steps for future work.
```

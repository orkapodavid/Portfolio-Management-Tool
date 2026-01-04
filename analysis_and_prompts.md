# PMT Reflex Integration Analysis & Prompts

## 1. High-Level Summary

### Current Architecture
*   **Monolithic State Machine**: The core logic resides in `PortfolioDashboardState` (`app/states/dashboard/portfolio_dashboard_state.py`), which manages navigation, UI state, and data fetching for the entire dashboard.
*   **Adapter Pattern**: The app uses an `Adapter` layer (`app/adapters/`) to decouple the UI from data sources. Currently, these adapters primarily interface with mock services or internal generators.
*   **Integration Modes**: controlled by `PMT_INTEGRATION_MODE` (`mock`, `real`, `standalone`). "Standalone" relies on internal data generators within the state file, while "Mock" uses the `app/mocks/pmt_core` package.
*   **Component Structure**: The UI follows a strict 4-region layout (Top Nav, Performance Header, Contextual Workspace, Notification Sidebar). The `contextual_workspace.py` component uses `rx.match` to dynamically render sub-module views based on state.
*   **Data Flow**: `PortfolioDashboardState` triggers `load_data_from_adapters` on page load or refresh. This calls async adapter methods which fetch DTOs and transform them for the UI.

### Planned Reflex Integration
*   **Shared `pmt_core`**: The target architecture involves a shared, framework-agnostic `pmt_core` package that encapsulates business logic, models, and services. Both the legacy PyQt app and the new Reflex app will consume this core.
*   **Strict Dependency Direction**: Reflex (UI) -> Adapters -> `pmt_core`. The `pmt_core` package must not know about Reflex or PyQt.
*   **Migration Path**:
    1.  Refactor Reflex app to fully use the Adapter pattern and remove internal "standalone" logic.
    2.  Develop `pmt_core` (initially mocked in `app/mocks/pmt_core`).
    3.  Swap the mock with the real `pmt_core` package once available.
*   **UI Parity**: The Reflex app aims to replicate the dense, data-heavy interface of the PyQt application, including specific tables for PnL, Positions, Compliance, and Operations.

## 2. Assumptions & Constraints

### Assumptions
*   **`pmt_core` Availability**: The real `pmt_core` package does not yet exist in this repository and will be installed as an external dependency or submodule later.
*   **Async/Sync Boundary**: `pmt_core` services will likely be synchronous (blocking). Reflex is async. We assume `asyncio.to_thread` will be used in adapters to prevent blocking the event loop.
*   **Data Models**: The DTOs defined in `app/mocks/pmt_core/models/dtos.py` (implied) and `app/states/dashboard/portfolio_dashboard_types.py` accurately reflect the intended schema of the future `pmt_core`.
*   **Deployment**: The app will be deployed in an environment where it can access the same resources (DB, APIs) as the PyQt app via `pmt_core`.

### Constraints
*   **No Direct Logic in UI**: Business logic (calculations, rules, data merging) must not reside in Reflex components or states. It must be delegated to the Adapter/Service layer.
*   **Performance**: The dashboard displays large datasets (e.g., 400+ rows). The UI must remain responsive. Virtualization or pagination is already partially implemented but critical.
*   **Layout**: The 4-region layout is strict. New features must fit into the existing `contextual_workspace` subtab structure.
*   **Styling**: Must use Tailwind CSS (via `class_name`) and `rx.el` components. No raw HTML or React.

## 3. Risk & Gap Assessment

### Potential Risks
*   **State Bloat**: `PortfolioDashboardState` is already over 900 lines long. Adding real integration logic and error handling could make it unmaintainable. *Mitigation: Split state into sub-states per module (e.g., `PnLState`, `PositionsState`).*
*   **Data synchronization**: The "Standalone" mode uses different logic (`_generate_*` functions) than the "Mock" mode (Adapters). This creates a risk where the standalone development version diverges from the integration version. *Mitigation: Deprecate Standalone mode in favor of Mock mode.*
*   **Subtab Implementation**: While `PortfolioDashboardState` lists many subtabs, some components in `contextual_workspace.py` map to `mock_data_table()` or placeholder views. We need to verify which functional requirements are actually met by existing components.
*   **Complex Logic Migration**: The PyQt app has complex "Merge" and "Rule" logic in `.ini` files. Porting this to `pmt_core` and exposing it cleanly to Reflex is a non-trivial backend task that affects the UI data shape.

### Information Gaps
*   **`pmt_core` API Spec**: We have mocks, but no concrete specification for the `pmt_core` API methods (arguments, return types, error states). The mocks are currently our only "spec".
*   **Authentication**: There is no mention of authentication or user sessions in the code reviewed. Integration with `pmt_core` might require passing user credentials.
*   **Write Operations**: Most analysis focuses on *reading* data. The requirements mention "Manual Booking" and "Orders". We need to understand how write operations (updates, inserts) will be handled via Adapters.

## 4. Follow-Up Prompts for LLM Coding Sessions

### Theme: Architecture Refactoring & Cleanup

#### [Theme: Refactor]
**Prompt Title:** Refactor PortfolioDashboardState to reduce bloat
**Prompt:**
"Refactor `app/states/dashboard/portfolio_dashboard_state.py` to reduce its size and complexity.
1. Create a new directory `app/states/dashboard/modules/`.
2. Extract the logic for 'Positions' data (loading, filtering, state variables like `positions_data`, `stock_positions`, etc.) into a new sub-state `app/states/dashboard/modules/positions_state.py`.
3. Extract 'PnL' data logic into `app/states/dashboard/modules/pnl_state.py`.
4. Ensure `PortfolioDashboardState` inherits or composes these new states so the UI components in `contextual_workspace.py` still have access to the data.
5. Verify that `load_data_from_adapters` still works correctly by coordinating these sub-states."

#### [Theme: Refactor]
**Prompt Title:** Standardize on Mock Mode and Remove Standalone Generators
**Prompt:**
"The application currently has two ways to generate fake data: internal `_generate_*` functions in `PortfolioDashboardState` (Standalone mode) and `app/mocks/pmt_core` services (Mock mode).
1. Refactor `app/states/dashboard/portfolio_dashboard_state.py` to remove all `_generate_*_data` functions.
2. Update the `standalone` mode logic to simple alias to `mock` mode, or remove `standalone` mode entirely from `app/config.py`.
3. Ensure that `load_data_from_adapters` is the *only* way data enters the state, using the `app/adapters/` layer.
4. Verify that `app/adapters/` correctly points to `app/mocks/pmt_core` when `PMT_INTEGRATION_MODE` is 'mock'."

### Theme: Feature Implementation (Missing Views)

#### [Theme: Feature]
**Prompt Title:** Implement Compliance View Components
**Prompt:**
"Implement the missing UI components for the 'Compliance' module in `app/components/compliance/`.
1. Reference `docs/User Interface and Functional Requirements_ Portfolio Management Tool.md` section 3.2.
2. Review `app/states/dashboard/portfolio_dashboard_types.py` for the data structures (`RestrictedListItem`, `UndertakingItem`, etc.).
3. Update `app/components/compliance/compliance_views.py` (create if needed) to implement real tables for:
   - `restricted_list_table`
   - `undertakings_table`
   - `beneficial_ownership_table`
   - `monthly_exercise_limit_table`
4. Use `app/components/shared/table_utils.py` (or similar existing patterns in `contextual_workspace.py`) for consistent styling (header cells, row styling).
5. Ensure these components bind correctly to the data in `PortfolioDashboardState`."

#### [Theme: Feature]
**Prompt Title:** Implement Reconciliation View Components
**Prompt:**
"Implement the UI components for the 'Reconciliation' module.
1. Reference `docs/User Interface and Functional Requirements_ Portfolio Management Tool.md` section 3.5.
2. Create/Update `app/components/reconciliation/reconciliation_views.py`.
3. Implement tables for:
   - `pps_recon_table`
   - `settlement_recon_table`
   - `failed_trades_table`
   - `pnl_recon_table`
   - `risk_input_recon_table`
4. Ensure columns match the requirements and the DTOs in `app/states/dashboard/portfolio_dashboard_types.py`.
5. Update `app/components/shared/contextual_workspace.py` to import and use these new components instead of `mock_data_table`."

### Theme: Integration & Data Layer

#### [Theme: Integration]
**Prompt Title:** Expand Mocks for Write Operations
**Prompt:**
"The current mocks in `app/mocks/pmt_core` are read-only. We need to support basic write operations for the 'Orders' module.
1. Update `app/mocks/pmt_core/services/trading.py` (create if missing) to add methods:
   - `create_emsx_order(order: EMSAOrderDTO) -> ResultDTO`
   - `update_emsx_order(id: str, updates: dict) -> ResultDTO`
2. Create corresponding Adapter methods in `app/adapters/trading_adapter.py`.
3. Update `app/states/dashboard/portfolio_dashboard_state.py` to include event handlers for creating/updating orders (`submit_order`, `update_order_status`).
4. Ensure the state updates the local list of orders upon success to reflect the change in the UI."

#### [Theme: Integration]
**Prompt Title:** Add Error Handling and Loading States to Adapters
**Prompt:**
"Enhance the robustness of the Adapter layer.
1. Modify `app/adapters/base_adapter.py` and specific adapters (`portfolio_adapter.py`, `reporting_adapter.py`) to wrap `pmt_core` calls in try/except blocks.
2. Define a standard `AppError` type or structure.
3. Update `PortfolioDashboardState` to handle these errors:
   - If an adapter fails, set a specific error message in the state (e.g., `self.error_message`).
   - Show a `rx.toast` with the error details.
   - Ensure `is_loading` is set to `False` even if an error occurs.
4. Test this by temporarily throwing an exception in one of the mock services."

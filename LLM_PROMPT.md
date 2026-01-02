# Code Improvement Task: Complete Reflex UI Integration Preparation

**Context:**
The repository is in the process of preparing a Reflex web application for integration with a Python backend (`pmt_core`). A guide at `docs/reflex_ui_integration_prep.md` outlines the necessary steps. An initial review has determined that Phases 1 and 2 are mostly complete (adapters and mocks exist), but significant parts of Phase 3 and 4 are missing.

**Your Task:**
Complete the following specific implementation tasks to finish the integration preparation. Do not modify existing working code unless necessary for these tasks.

### 1. Refactor `app/states/portfolio/portfolio_state.py` (Refer to Prompt 5)
The file `app/states/portfolio/portfolio_state.py` currently uses hardcoded data. You must refactor it to use the adapter layer, similar to how `app/states/dashboard/portfolio_dashboard_state.py` is implemented.

*   **Action:** Modify `PortfolioState` to fetch data using `app.adapters.portfolio_adapter.PortfolioAdapter`.
*   **Details:**
    *   **Enhance Adapter:** The current `PortfolioAdapter` only fetches flat lists of positions. You need to add functionality to `PortfolioAdapter` (and corresponding mocks in `app/mocks/pmt_core`) to support the data structure required by `PortfolioState` (specifically `holdings`, and optionally `transactions`/`dividends` if feasible, otherwise keep them empty or mocked).
        *   Implement a method like `get_user_portfolio_holdings(portfolio_id)` in the adapter.
        *   Map the `PositionItem` or `StockPositionItem` from the core/mock to the `Holding` TypedDict used in `PortfolioState`.
    *   **Update State:**
        *   Import `PortfolioAdapter`.
        *   In `PortfolioState`, replace the hardcoded `holdings` list in the `portfolios` state variable with data fetched from the adapter.
        *   Use `asyncio.to_thread` for mock service calls if needed (handled by Adapter base class usually).
        *   Initialize the state by fetching data in an event handler (e.g., `on_load` or similar) or keep a default structure that populates on first access.
    *   **Maintain State Structure:** Keep the `Portfolio` TypedDict and `portfolios` list structure to ensure UI compatibility. Group fetched positions by account ID or create a default portfolio to hold them.
    *   **Handle Mode:** Ensure the `PMT_INTEGRATION_MODE` check is handled implicitly via the Adapter.

### 2. Update `requirements.txt` (Refer to Prompt 7)
The dependency file is missing the placeholder for the future `pmt_core` package.

*   **Action:** Add the following lines to `requirements.txt`:
    ```text
    # PMT Core integration (uncomment when pmt_core is available)
    # -e ../pmt_core
    ```

### 3. Create Integration Status Documentation (Refer to Prompt 10)
The status tracking document is missing.

*   **Action:** Create `docs/reflex_integration_status.md`.
*   **Details:**
    *   List what has been done (Adapters, Mocks, Dashboard State integration).
    *   List what you have just completed (Portfolio State integration, Config).
    *   Create the "Integration Checklist" as described in Prompt 10 of the prep guide.

**Note:**
*   You do **not** need to create `app/components/pmt/` (Prompt 9) as similar components appear to have been integrated directly into domain-specific folders (e.g., `app/components/compliance`).
*   Ensure all new code adheres to the existing project style.

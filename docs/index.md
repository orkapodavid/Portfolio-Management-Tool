# Documentation Index

Central navigation for all Portfolio Management Tool documentation.

---

## Getting Started

| Document | Description |
|---|---|
| [onboarding.md](onboarding.md) | Connecting to MS SQL Server, environment setup, service layer architecture |
| [setups/memurai.md](setups/memurai.md) | Memurai (Windows-native Redis) installation & configuration |
| [setups/garnet.md](setups/garnet.md) | Microsoft Garnet server setup on Windows |
| [setups/windows_iis_auth.md](setups/windows_iis_auth.md) | Windows IIS authentication setup |
| [setups/auth_approaches.md](setups/auth_approaches.md) | Alternative authentication approaches |

---

## Architecture

| Document | Description |
|---|---|
| [style_guides/reflex-architecture-guide.md](style_guides/reflex-architecture-guide.md) | **Canonical reference** — Multi-region layout, state management, service layer, component patterns |
| [pmt.md](pmt.md) | PyQt desktop app architecture map (for code reuse reference) |
| [pmt_web_plan.md](pmt_web_plan.md) | Strategy for sharing business logic between PyQt and Reflex apps via `pmt_core` |

---

## Feature Guides

| Document | Description |
|---|---|
| [reflex_ag_grid/ag-grid-config.md](reflex_ag_grid/ag-grid-config.md) | AG Grid configuration package — factory, toolbar, filters, context menus |
| [reflex_ag_grid/ag_grid_factory_migration.md](reflex_ag_grid/ag_grid_factory_migration.md) | AG Grid factory migration — quick start guide for `create_standard_grid()` |
| [plotly/Reflex Plotly Integration Guide.md](plotly/Reflex%20Plotly%20Integration%20Guide.md) | Plotly chart integration — events, responsive design, theming, 3D surfaces |
| [notifications/NOTIFICATIONS.md](notifications/NOTIFICATIONS.md) | Notification system — Pub/Sub registry pattern, adding providers |

---

## LLM Prompt Templates

Reusable task prompts for AI-assisted development:

| Prompt | Purpose |
|---|---|
| [prompts/create_new_page.md](prompts/create_new_page.md) | Create a complete module page (state, service, route, navigation) |
| [prompts/create_new_tab.md](prompts/create_new_tab.md) | Add a new tab to an existing module |
| [prompts/create_input_form.md](prompts/create_input_form.md) | Build a validated input form (Pydantic + Reflex) |
| [prompts/refactor_to_module_structure.md](prompts/refactor_to_module_structure.md) | Refactor `pmt_core` to module-based folder structure |
| [prompts/nav_bar_refactoring.md](prompts/nav_bar_refactoring.md) | Implement the shared top navigation bar |
| [prompts/reflex-module-layout-tabs-prompt.md](prompts/reflex-module-layout-tabs-prompt.md) | Convert module pages to tabbed layout |
| [prompts/reflex-style-migration-prompts.md](prompts/reflex-style-migration-prompts.md) | Phase-based architecture refactoring prompts |

---

## Reference

| Document | Description |
|---|---|
| [web/pages.md](web/pages.md) | Complete list of all pages, routes, tabs, and states |

---

---

## Archived

Completed or superseded documents:

| Document | Notes |
|---|---|
| [archive/service_layer_migration.md](archive/service_layer_migration.md) | ✅ Phase 1 completed — all 14 mixins migrated |
| [archive/service_layer_migration_2.md](archive/service_layer_migration_2.md) | ✅ Phase 2 completed — remaining 6 domains migrated |
| [archive/generic_prompts.md](archive/generic_prompts.md) | SPA→route migration plan (superseded by current architecture) |
| [archive/milestone-0-preparation-checklist.md](archive/milestone-0-preparation-checklist.md) | ✅ Infrastructure preparation (superseded by Milestone 1) |
| [archive/milestone-1-pre-integration-checklist.md](archive/milestone-1-pre-integration-checklist.md) | ✅ Pre-integration preparation (actionable items complete) |
| [archive/pre_integration_review.md](archive/pre_integration_review.md) | ✅ Code review — critical issues resolved |
| [archive/ag_grids/table_improvement.md](archive/ag_grids/table_improvement.md) | ✅ AG Grid Phase 1 — wrapper + 15 demo pages |
| [archive/ag_grids/table_improvement_2.md](archive/ag_grids/table_improvement_2.md) | ✅ AG Grid Phase 2 — advanced features |
| [archive/ag_grids/table_improvement_v3.md](archive/ag_grids/table_improvement_v3.md) | ✅ AG Grid Phase 3 — v35 migration |
| [archive/ag_grids/status_bar_rollout.md](archive/ag_grids/status_bar_rollout.md) | ✅ Status bar rollout — all 48 grids |
| [archive/ag_grids/table_improvement_v4.md](archive/ag_grids/table_improvement_v4.md) | ✅ AG Grid Phase 4 — overlays, tree data, quick filter, column state |
| [archive/plotly/design_chart.md](archive/plotly/design_chart.md) | ✅ Pricer chart design |
| [archive/plotly/implementation_plan.md](archive/plotly/implementation_plan.md) | ✅ Plotly integration plan |


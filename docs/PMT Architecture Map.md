# PMT Architecture Map (PyQt, Windows)

This notes the structure and data plumbing of the Portfolio Management Tool (PyQt5 desktop app packaged by `main.spec`). Docs are ignored; focus is on the runtime code that drives the UI.

## File Structure (docs excluded)

```text
.
|-- main.py
|-- main.spec
|-- requirements.txt
|-- resources/
|   |-- config/
|   |   |-- env.ini                 # DB/Bloomberg/log settings
|   |   |-- report/                 # One .report.ini per tab/page
|   |   |   |-- analytics_tab/      # e.g. pricer_bond.report.ini
|   |   |   |-- compliance_tab/
|   |   |   |-- event_tab/
|   |   |   |-- instrument_tab/
|   |   |   |-- market_data_tab/
|   |   |   |-- operation_tab/
|   |   |   |-- pnl_tab/
|   |   |   |-- position_tab/
|   |   |   |-- recon_tab/
|   |   |   |-- report_tab/
|   |   |   `-- trading_tab/        # e.g. emsx_order.report.ini
|   `-- icon/                       # toolbar/tab icons + h.ico
|-- source/
|   |-- bloomberg/                  # EMSX + ref data service glue
|   |   |-- bbg_service_connector.py
|   |   |-- service/ (emsx_* handlers, market/ref data queries)
|   |   `-- utility/ (message/request helpers)
|   |-- gui/
|   |   |-- ui/                     # generated UI + actions/workers
|   |   |   |-- ui_window_base.py / ui_window_main.py / ui_window_tabs.py
|   |   |   |-- ui_action_*.py (menus, exports, alerts, rules)
|   |   |   |-- ui_worker_*.py (Qt worker launchers for DB/BBG/files)
|   |   |   `-- ui_data_report.py / ui_utility_report.py (table rendering)
|   |   `-- widget/                 # reusable widgets (tables, dialogs)
|   |       `-- widget_widget.py (tab container + buttons/menus wiring)
|   |-- models/                     # config + typed models/enums
|   |   |-- class_mapping.py        # ReportType -> ReportClass subclass
|   |   |-- class_model_config.py   # global ModelConfig cache
|   |   |-- class_report.py         # ReportClass base + Merge/Rule cfg
|   |   `-- enum_*.py
|   |-- reports/                    # one folder per dashboard section
|   |   |-- shared_class.py / shared_data.py / shared_*calculator.py
|   |   |-- trading_tab/emsx_order/, emsx_route/
|   |   |-- position_tab/position_full/, position_eod_*/, trade_summary/
|   |   |-- pnl_tab/, market_data_tab/, compliance_tab/, analytics_tab/
|   |   `-- recon_tab/, report_tab/, event_tab/, operation_tab/
|   |-- utilities/                  # config readers, DB helpers, logger
|   |   |-- config_reader_env.py / config_reader_model.py
|   |   |-- database_reader.py / config_database_query.py / dataframe_processor.py
|   |   `-- logger.py, signal_tracker.py, utility_* helpers
|   |-- workers/                    # QThread workers for data/processes
|   |   |-- worker_report.py (TabWorker), worker_database.py, worker_market_data.py
|   |   `-- worker_emsx_order.py, worker_emsx_route.py, worker_process.py, ...
|   |-- pricers/                    # pricing engines (shared by analytics tabs)
|   `-- symphony/room_listener.py   # Symphony chat hook
|-- pricers/                        # stand-alone sample pricer scripts (GUI/MC)
`-- outputs/                        # generated artifacts (ignored at runtime)

```

---

## How tabs are built and fed with data

* **Startup chain:** `main.py` -> `init_env_config()` (reads `resources/config/env.ini`) -> `init_model_config()` (reads every `resources/config/report/**/*.report.ini`, instantiates `ReportClass` subclasses via `class_mapping.py`) -> `Ui_Main` (base window and toolbar) -> `Ui_Tabs` (creates one `Widget` per enabled report and inserts it into the correct `QTabWidget` by `dashboard_name` plus `sequence`).
* **Per-tab config comes from `.report.ini**`
* `[Basic]`: dashboard name, `report_type`, tab label (`report_name`), `auto_refresh`, order `sequence`, notes.
* `[Data_Model]`: field types, display labels, key flags, formatting, editability.
* `[Headers]`: default visible columns; `[Email_Headers]`: email export templates.
* `[Query]`: inline SQL or a symbolic name; if blank, the subclass supplies data.
* `[Merges]`: how this tab joins data from other report types (left/right keys, background refresh).
* `[Rules]`: per-row alert rules evaluated after data loads.


* **Class-specific plumbing:** Each `ReportClass` subclass (for example `source/reports/trading_tab/emsx_order/emsx_order_class.py`, `position_full_class.py`, `market_data_class.py`) overrides:
* `create_ui_tab` to add extra buttons/menus/inputs beyond the default "Generate ..." button.
* `extract_report_data` to fetch the raw data (DB SQL via `utilities/database_reader.execute_query`, Bloomberg EMSX via `worker_emsx_*`, flat files, or calculator output).
* `merge_report_data` to apply the `[Merges]` rules using upstream tab data.
* `process_report_data` to push side-effects (for example subscribe to BBG tickers, upsert DB rows).


* **Execution path when a tab refreshes:** button click (or auto-refresh timer) -> `ui_worker_report.create_report_worker` -> `TabWorker.generate_report_data` -> `ReportClass.extract_report_data` -> merges -> diffs computed vs current table -> UI updated in `ui_data_report.display_data` -> merge-dependents refreshed if needed -> rules run -> status cleared.
* **Examples of data drivers**
* **Trading > EMSX Order:** config `resources/config/report/trading_tab/emsx_order.report.ini`; class `emsx_order_class.py`; data comes from live EMSX via `EMSXOrderWorker` (Bloomberg) with DB snapshot fallback (`get_emsx_order_from_db`); merges in market/reference data, routes, positions, settlement, restricted list.
* **Positions > Positions:** config `position_tab/position_full.report.ini`; class `position_full_class.py`; data from DB via `extract_current_positions`; merges EMSX orders, FX, market/ref data; calendar selector sets `report_params[position_date]`.
* **Market Data > Market Data:** config `market_data_tab/market_data.report.ini`; class `market_data_class.py`; data pulled from Bloomberg real time through `worker_market_data.py` (no SQL).
* **Compliance > Restricted List / Undertaking / Beneficial Ownership:** configs in `compliance_tab/`; classes in matching folders; extractors pull DB tables, rules mark restricted tickers.
* **Analytics > Pricers (bond/warrant):** configs in `analytics_tab/`; classes delegate to `source/pricers/*` engines and enrichment helpers in `common_pricer/`.



---

## How to find the data source for any page/tab

1. **Identify the report type:** In the UI, the tab title matches `report_name` in a `.report.ini`. Search `resources/config/report/**` for that name. Note the `report_type` value and `dashboard_name`.
2. **Locate the subclass:** Open `source/models/class_mapping.py` to map `ReportType.<name>` to a concrete class, for example `ReportType.emsx_order -> EMSXOrder`. The class lives under `source/reports/<dashboard>/<report>/<report>_class.py`.
3. **Inspect `extract_report_data`:** This method shows the true source:
* Calls to `execute_query(self.report_type, self.query)` mean the SQL comes from `[Query]/query` in the `.report.ini` (or a helper in `..._queries.py`).
* Calls to functions in `*_extractor.py` reveal DB tables, Bloomberg services, or file paths.
* Auto-merges are driven by `[Merges]` and the class's `merge_report_data` overrides.


4. **Check auto-refresh and dependencies:** `[Basic]/auto_refresh` controls polling; merges listed in the `.report.ini` determine which other tabs must load first.
5. **Runtime tweaks:** If data is editable, `process_report_data` or `process_ui_data` will show DB upserts, EMSX actions, or BBG subscriptions triggered after data arrives.

---

## How to trace what a UI button does

* **Default "Generate ..." button:** created in `widget_widget.py:create_buttons`; connected to `ui_worker_report.create_report_worker` and the refresh pipeline above.
* **Tab-specific buttons/menus:** open the tab's `*_class.py` and look at `create_ui_tab`. Extra buttons are added either directly (`tab.create_button(...)`) or via helper factories like `create_emsx_order_buttons` in `emsx_order_ui_table.py`. Follow the `.clicked.connect(...)` targets (often in `*_ui_action.py` or `ui_action_*` modules) to the business logic.
* **Context menus:** built in the same `create_ui_tab` chain; menu items live in `*_ui_table.py` or `ui_action_*` and are added to `tab.menus[menu_right_click_name]`.
* **Signals and background workers:** buttons that trigger long work typically call `create_report_worker`, `create_db_worker`, `create_bbg_worker`, or `worker_*`. Search for these in the tab's folder to see the actual handler.

---

## Reusing the codebase in a Python Reflex app (keep filesystem intact)

* **Keep the data layer:** reuse `resources/config/report` plus `source/models/*` and `source/reports/*` classes. They already expose `ReportClass.extract_report_data`, `merge_report_data`, and `data_model_header` (column metadata). No file moves needed.
* **Add a thin API/service layer:** create a new folder (for example `reflex_app/`) alongside existing code that imports `ModelConfig` and `class_mapping`. Provide FastAPI-style endpoints or Reflex `State` methods that call `report_class.extract_report_data()` and serialize `data_model_header` for column definitions.
* **Build Reflex views from configs:** for each `ReportClass`, generate tables using `data_model_header` (labels, formats, freeze/display flags) and auto-wire refresh intervals from `auto_refresh`. Use `[Merges]` to orchestrate upstream fetch order in state.
* **Reuse rules and exports:** port `Rules` by evaluating their pandas conditions server side (logic is in `ui_action_rule` plus `RuleConfig`). Exports (Excel/email) can call the existing helpers in `ui_action_export`.
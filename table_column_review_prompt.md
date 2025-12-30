### Prompt 1: Global Table Review Strategy

#### 1. Context

You are working on the **Portfolio Management Tool** implemented in this repository. The **authoritative specification** for all table columns and related UI behavior is defined in the requirements document:

- `User Interface and Functional Requirements_ Portfolio Management Tool.md`

Your task is to **systematically review all table-like UIs in the codebase** against this document and **correct any discrepancies**.

The review must cover **all modules** and their tabs as specified in the document:

- Positions & Trade Summary View
- Compliance & Holdings View
- Pay-To-Hold & Settlement View
- PnL View
- Reconciliation View
- Operational Processes View
- Market Data & Events View
- Ticker & Instrument Analysis View
- Risk & Pricing View
- EMSA Order Management View

#### 2. Overall Objectives

1. **Cross-verify every table and its columns** in the implemented UI against the specification in the requirements document.
2. **Identify and list all issues**, including:
   - Missing columns
   - Extra/unexpected columns
   - Incorrect column names or labels
   - Incorrect column ordering
   - Incorrect data types or formats (e.g., dates, percentages, currency, numeric vs. text)
   - Incorrect or missing contextual actions (e.g., buttons like "Generate Positions")
3. **Implement fixes** to bring the UI fully into alignment with the requirements document.
4. **Document the changes** you make and the rationale for each correction.

#### 3. Discovery: Locate All Tables in the Codebase

1. **Scan the codebase** for all table-like components, grids, and tabular UIs. In this project, these may be implemented as:
   - Generic table/grid components
   - Per-module table components (e.g., in `components/` or `pages/` folders)
   - Any layout that presents rows/columns of structured data
2. For each table, determine:
   - Which **module** it belongs to (e.g., PnL View, Reconciliation View)
   - Which **tab** it corresponds to (e.g., PnL Change, Restricted List, PPS Recon)
   - Where in the code it is defined (file path and component/function name)

Create a mapping table for yourself, e.g.:

- **Module**: Positions & Trade Summary View
  - **Tab**: Positions
    - **Implementation**: `<file(s)/component(s)>`
  - **Tab**: Stock Position
    - **Implementation**: `<file(s)/component(s)>`
  - etc.

You will use this mapping to ensure every specified table is accounted for.

#### 4. Cross-Referencing Procedure (Per Module & Tab)

For **each module** and **each tab** defined in the requirements document, perform the following steps:

1. **Identify the specification**
   - In `User Interface and Functional Requirements_ Portfolio Management Tool.md`, locate the section for the relevant module and tab.
   - Extract the **exact list and order of columns** specified for that tab.

2. **Locate the implementation**
   - Find the component(s) that render the corresponding table.
   - Confirm which tab and module it belongs to (via naming, labels, or context).

3. **Compare columns one by one**
   For each column in the specification, check the implementation for:
   - **Presence**: Is the column implemented at all?
   - **Label/Name**: Does the label exactly match the spec (case, punctuation, spacing where meaningful)?
   - **Order**: Is the column displayed in the same order as in the requirements document?
   - **Type and format**:
     - Dates (e.g., `Trade Date`, `Value Date`, `Event Date`, `Maturity Date`)
     - Numeric values (e.g., `PnL`, `Shares`, `Amounts`, `Rates`, percentages like `1D Change %`)
     - Identifiers (e.g., `Deal Num`, `SecID`, `ISIN`, `SEDOL`)
     - Text fields (e.g., `Notes`, `Company Name`, `Event Type`)
   - **Derived/compound fields** where implied
   - **Filtering/sorting behavior** if applicable (e.g., ensure they behave sensibly for the data type)

4. **Identify discrepancies**
   - Columns present in the spec but **missing** in the implementation.
   - Columns implemented but **not present** in the spec.
   - Columns whose **labels differ** from the spec.
   - Columns whose **ordering** is inconsistent with the spec.
   - Columns whose **data type or formatting** does not match the intent implied by the spec.

5. **Check related UI elements**
   Where specified, also verify:
   - Contextual filter bars (date pickers, dropdowns, search fields) relevant to that table.
   - Action buttons associated with the view (e.g., **"Generate Positions"** in the Positions & Trade Summary View).
   - Auto-refresh controls where applicable.

---

### Prompt 2: Module-by-Module Checklist and Fix Implementation

#### 1. Module-by-Module Checklist

Use the following module-specific checklist to ensure no table is missed.

##### 1.1 Positions & Trade Summary View

Tabs to verify (per spec):
- **Positions Tab**
- **Stock Position Tab**
- **Warrant Position Tab**
- **Bond Positions Tab**
- **Trade Summary (War/Bond) Tab**

For each tab:
- Verify all columns listed in the requirements document are implemented with correct:
  - Names (e.g., `Trade Date`, `Deal Num`, `Detail ID`, `Underlying`, `Ticker`, `Company Name`, `Account ID`, `Pos Loc`, `SecID`, `Sec Type`, `Subtype`, `Currency`, `Position Location`, `Notional`, `Closing Date`, `Divisor` etc.).
  - Ordering and visibility.
- Confirm the **"Generate Positions"** action/button is present and wired appropriately in the view.

##### 1.2 Compliance & Holdings View

Tabs to verify:
- **Restricted List**
- **Undertakings**
- **Beneficial Ownership**
- **Monthly Exercise Limit**

Check that all specified columns (e.g., `In EMDX?`, `Compliance Type`, `Firm_Block`, `NDA End`, `MNPI End`, `NOSH (Reported)`, `NOSH (BBG)`, `NOSH Proforma`, `Stock Shares`, `Warrant Shares`, `Bond Shares`, `Total Shares`, etc.) are correctly implemented, named, and ordered.

##### 1.3 Pay-To-Hold & Settlement View

Tabs to verify:
- **Pay-To-Hold**
- **Short ECL**
- **Stock Borrow**
- **PO Settlement**
- **Deal Indication**
- **Reset Dates**
- **Coming Resets**
- **CB Installments**
- **Excess Amount**

Ensure all columns (e.g., `PTH Amount SOD`, `PTH Amount`, `EMSA Order`, `Short Position`, `Short Ownership`, `Last Volume`, `Borrow Rate`, `FX Rate`, `Current Position`, `Shares Allocated`, `Announcement Date`, `Installment Amount`, `Excess Amount Threshold`, etc.) match the spec.

##### 1.4 PnL View

Tabs to verify:
- **PnL Change**
- **PnL Summary**
- **PnL Currency**

Verify columns such as `PnL YTD`, `PnL Chg 1D`, `PnL Chg 1W`, `PnL Chg 1M`, `PnL Chg% 1D/1W/1M`, `Price (T-1)`, `FX Rate (T-1)`, `FX Rate Change`, `DTL`, `ADV 3M`, `USD Exposure`, `POS CCY Expo`, `CCY Hedged PnL`, `POS CCY PnL`, etc. have correct types and formats.

##### 1.5 Reconciliation View

Tabs to verify:
- **PPS Recon**
- **Settlement Recon**
- **Failed Trades**
- **PnL Recon**
- **Risk Input Recon**

Check all identifiers and reconciliation fields (e.g., `Value Date`, `ML Report Date`, `Position Settled`, `ML Inventory`, `ISIN`, `SEDOL`, `Glass Reference`, `Row Index`, `Stock SecID`, `Warrant SecID`, `Bond SecID`) are correctly implemented.

##### 1.6 Operational Processes View

Tabs to verify:
- **Daily Procedure Check**
- **Operation Process**

Ensure columns such as `Check Date`, `Host Run Date`, `Scheduled Time`, `Procedure Name`, `Status`, `Error Message`, `Frequency`, `Scheduled Day`, `Created By`, `Created Time`, `Last Run Time` match the spec.

##### 1.7 Market Data & Events View

Tabs to verify:
- **Market Data**
- **FX Data**
- **Historical Data**
- **Trading Calendar**
- **Market Hours**
- **Event Calendar**
- **Event Stream** (including the filter form + table)
- **Reverse Inquiry**

Pay particular attention to:
- Percentage and numeric fields (e.g., `1D Change %`, `Implied Vol %`, `Market Cap LOC`, etc.).
- Event-related fields and form inputs (e.g., `Record Date`, `Event Date`, `Subject`, `Notes`, `Symbol`, `Event Type`, `Recur Freq`, `On Month`, `On Dec`, `Alert` checkbox).

##### 1.8 Ticker & Instrument Analysis View

Tabs to verify:
- **Ticker Data**
- **Stock Screener** (filters + table)
- **Special Term**
- **Instrument Data**
- **Instrument Term**

Ensure all analytic and reference fields (e.g., `FMat Cap`, `SMkt Cap`, `37% Market Cap`, `Market Cap (MM LOC)`, `Market Cap (MM USD)`, `ADV 3M`, `Locate Qty (MM)`, `Locate F`, `Effective Date`, `Maturity Date`, `First Reset Date`, etc.) are correctly reflected.

##### 1.9 Risk & Pricing View

Tabs to verify:
- **Delta Change**
- **Risk Measures**
- **Risk Inputs**
- **Pricer Warrant** (two-panel layout: Terms + Simulations/Outputs)
- **Price Bond** (two-panel layout: Terms + Results grid)

For tables and grids:
- Confirm columns such as `Pos Delta`, `posDelta`, `Pos G`, `Seed`, `Simulation#`, `Trial#`, `Is Private`, `National`, `National Used`, `National Current`, `Spot Price`, and pricing outputs (`Fair Value`, `Delta`, `Discount`) are implemented as specified.
- For two-panel layouts, ensure that the **left-side inputs** and **right-side result grids** match the described fields and labels.

##### 1.10 EMSA Order Management View

Tabs to verify:
- **EMSA Order**
- **EMSA Route**

Both tabs share the same column structure (`Sequence`, `Underlying`, `Ticker`, `Broker`, `Pos Loc`, `Side`, `Status`, `EMSA Amount`, `EMSA Routed`, `EMSA Working`, `EMSA Filled`). Ensure this is accurately implemented, and any routing-specific behavior for the Route tab is consistent with the spec.

#### 2. Implementing Corrections

For **each discrepancy** you find, perform the following:

1. **Missing column**
   - Add the column definition to the table/grid component.
   - Ensure label, order, type, and default formatting follow the requirements document.
   - Wire the column to appropriate data from the backend or state. If data source does not yet provide the field, add a clear TODO and, if appropriate, a placeholder or computed value, noting the dependency.

2. **Extra/non-specified column**
   - Decide whether to remove the column or justify its presence.
   - If it is not explicitly justified by the requirements, remove or hide it to match the spec.

3. **Incorrect column name/label**
   - Update the display label to match the spec exactly.

4. **Incorrect column ordering**
   - Reorder columns to match the sequence specified in the requirements document.

5. **Incorrect type/formatting**
   - Update the column definition to use appropriate:
     - Date formatting for dates
     - Numeric formatting for quantities, amounts, and percentages
     - Currency formatting for monetary fields
     - Text rendering for free-text/notes fields

6. **Missing contextual elements**
   - Add missing filter controls (date pickers, dropdowns, search fields) where the spec indicates a contextual filter bar.
   - Add or fix action buttons at the bottom of views (e.g., `Generate Positions`, `Filter Event`, `Upload Event`).
   - Implement auto-refresh toggles where called for, or stub them with clear TODOs if backend support is pending.

#### 3. Validation and Consistency Checks

After implementing changes:

1. **Manually review each module and tab**
   - Re-open each view and confirm that the visible columns and their order match the spec.
2. **Spot-check data types and formatting**
   - Ensure that date columns show dates, numeric columns show numbers with appropriate formatting, and percentages are rendered clearly.
3. **Check for regressions**
   - Ensure that existing functionality (sorting, filtering, pagination, etc.) still works after modifications.

#### 4. Reporting Your Work

At the end of the process, produce a concise summary that includes:

- **Per module and tab**:
  - A list of discrepancies found.
  - The fixes you implemented (code locations + nature of change).
- **Open items / TODOs**:
  - Any columns or behaviors that could not be fully implemented due to missing backend data or unclear requirements.

Your goal in Prompt 2 is to leave the Portfolio Management Tool with **all tables and associated UI elements fully aligned** with the specifications in `User Interface and Functional Requirements_ Portfolio Management Tool.md`.
#### 8. Reporting Your Work

At the end of the process, produce a concise summary that includes:

- **Per module and tab**:
  - A list of discrepancies found.
  - The fixes you implemented (code locations + nature of change).
- **Open items / TODOs**:
  - Any columns or behaviors that could not be fully implemented due to missing backend data or unclear requirements.

Your goal is to leave the Portfolio Management Tool with **all tables and associated UI elements fully aligned** with the specifications in `User Interface and Functional Requirements_ Portfolio Management Tool.md`.
   - Ensure that date columns show dates, numeric columns show numbers with appropriate formatting, and percentages are rendered clearly.
3. **Check for regressions**
   - Ensure that existing functionality (sorting, filtering, pagination, etc.) still works after modifications.

#### 8. Reporting Your Work

At the end of the process, produce a concise summary that includes:

- **Per module and tab**:
  - A list of discrepancies found.
  - The fixes you implemented (code locations + nature of change).
- **Open items / TODOs**:
  - Any columns or behaviors that could not be fully implemented due to missing backend data or unclear requirements.

Your goal is to leave the Portfolio Management Tool with **all tables and associated UI elements fully aligned** with the specifications in `User Interface and Functional Requirements_ Portfolio Management Tool.md`.
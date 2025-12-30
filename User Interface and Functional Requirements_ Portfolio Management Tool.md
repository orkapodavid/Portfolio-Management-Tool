### User Interface and Functional Requirements: Portfolio Management Tool

#### 1.0 Introduction and System Overview

This document defines the comprehensive specification for the user interface (UI) and functional components of the "Portfolio Management Tool." Its purpose is to serve as the primary blueprint for an LLM Coder to accurately recreate the application's pages, features, and interactive elements. By meticulously detailing the structure, layout, and data requirements of each screen, this specification will guide the development process and ensure a faithful reconstruction of the system's intended functionality.The application is built upon a consistent, multi-panel layout that provides users with persistent access to key information and navigation controls. This high-level architecture ensures a predictable and efficient user experience across all modules. The primary components are:

* **Main Application Window:**  The top-level container for all UI components.  
* **Header Dashboard:**  A persistent panel at the top of the window that displays a high-level summary of key performance indicators and market movers.  
* **Vertical Navigation Bar:**  The primary navigation element, located on the left side, which provides icon-based access to the application's core functional modules.  
* **Main Content Area:**  The central, dynamic section of the application. This area displays detailed data tables, input forms, and interactive controls corresponding to the module selected from the navigation bar.  
* **Notifications Sidebar:**  A persistent panel on the right side of the window that displays a real-time feed of system alerts and important updates.The following sections will provide a detailed breakdown of these global UI elements before delving into the specific functional requirements of each core application page.

#### 2.0 Global UI Elements and Layout

The strategic definition of global UI elements is paramount to the application's usability. These components form the foundational structure present on every screen, creating a consistent and intuitive user experience. By standardizing these components, the application reduces cognitive load on the user and streamlines development by creating reusable, system-wide components.

##### Header Dashboard Analysis

The Header Dashboard functions as a persistent, at-a-glance summary of key financial metrics and market activity. It is always visible at the top of the main application window, providing crucial context without interrupting the user's workflow. The dashboard is composed of six distinct panels, each presenting a specific data slice. Within these panels, negative financial figures are consistently rendered in red text for immediate visual identification of losses or negative movements.| Panel Title | Description || \------ | \------ || Daily PnL | Displays a summary of daily Profit and Loss figures across various categories. || Top Daily Ops PnL Movers | Lists the top tickers driving daily operational Profit and Loss, showing both positive and negative movers. || Top YTD PnL Movers | Lists the top tickers driving Year-To-Date Profit and Loss. || Top Daily $Delta Movers | Shows the tickers with the most significant daily changes in their dollar delta value. || Top Price Movers | Highlights the tickers with the largest percentage-based price movements for the day. || Top Volume Movers (%ADV) | Identifies tickers with the highest trading volume relative to their Average Daily Volume (%ADV). |

##### Left Vertical Navigation Bar

This vertical bar is the primary tool for navigating between the application's major functional modules. Each icon corresponds to a distinct page, which loads into the Main Content Area upon selection.

* **Positions & Trade Summary View**  (Icon of a house containing a bar chart)  
* **Compliance & Holdings View**  (Icon of a shield with a restricted symbol)  
* **Pay-To-Hold & Settlement View**  (Icon of an open book)  
* **PnL View**  (Icon of a document with lines of text)  
* **Reconciliation View**  (Icon of a dollar sign)  
* **Operational Processes View**  (Icon resembling an abacus)  
* **Market Data & Events View**  (Icon of a globe)  
* **Ticker & Instrument Analysis View**  (Icon of a magnifying glass over a document)  
* **Risk & Pricing View**  (Icon of a delta symbol within a calculation grid)  
* **EMSA Order Management View**  (Icon of a network flow diagram)

##### Right Notifications Sidebar

The sidebar on the far right serves as a real-time feed for system and user-generated alerts. This component ensures that users are immediately aware of important events, such as compliance warnings or trade booking status updates. Each notification includes a title, a timestamp, and descriptive text.

* **Amber: Begin Covering:**  A notification detailing a short-selling coverage requirement (e.g., Report: Short ECL, Time: 2025-12-26 16:21:58, Ticker 1619 JP should start covering as trade at 151, less than 5% above).  
* **Amber: Manual Booking:**  An alert indicating a manual booking has occurred (e.g., Report: Positions, Time: 2025-12-26 16:10:10, Ticker 9348 JP has manual booking quantity \#63,300 today, matching).With the global structure defined, the focus now shifts to the detailed specifications for each of the application's core pages.

#### 3.0 Core Application Pages: Functional Specifications

The following subsections dissect each major page of the application, accessible via the left vertical navigation bar. For each page, the associated tabs, tabular data displays, interactive controls, and specific layouts are meticulously detailed to ensure an accurate and functional replication.

##### 3.1 Positions & Trade Summary View

This module provides functionality for viewing current holdings across various asset classes. It presents a detailed, tabular breakdown of positions and trade summaries.

* **Positions Tab Columns:**  
* Trade Date  
* Deal Num  
* Detail ID  
* Underlying  
* Ticker  
* Company Name  
* Account ID  
* Pos Loc  
* **Stock Position Tab Columns:**  
* Trade Date  
* Deal Num  
* Detail ID  
* Ticker  
* Company Name  
* SecID  
* Sec Type  
* Currency  
* Account ID  
* Position Location  
* Notional  
* **Warrant Position Tab Columns:**  
* Trade Date  
* Deal Num  
* Detail ID  
* Underlying  
* Ticker  
* Company Name  
* SecID  
* Sec Type  
* Subtype  
* Currency  
* Account ID  
* **Bond Positions Tab Columns:**  
* Trade Date  
* Deal Num  
* Detail ID  
* Underlying  
* Ticker  
* Company Name  
* SecID  
* Sec Type  
* Subtype  
* Currency  
* Account ID  
* **Trade Summary (War/Bond) Tab Columns:**  
* Deal Num  
* Detail ID  
* Ticker  
* Underlying  
* Account ID  
* Company Name  
* SecID  
* Sec Type  
* Subtype  
* Currency  
* Closing Date  
* DivisorA "Generate Positions" button is present at the bottom of the content area for this view.

##### 3.2 Compliance & Holdings View

This module provides essential tools for monitoring compliance with internal policies and external regulations, including tracking restricted lists, undertakings, and beneficial ownership limits.

* **Restricted List Tab Columns:**  
* Ticker  
* Company Name  
* In EMDX?  
* Compliance Type  
* Firm\_Block  
* Compliance Start  
* NDA End  
* MNPI End  
* WC End  
* **Undertakings Tab Columns:**  
* Deal Num  
* Ticker  
* Company Name  
* Account  
* Undertaking Expiry  
* Undertaking Type  
* Undertaking Details  
* **Beneficial Ownership Tab Columns:**  
* Trade Date  
* Ticker  
* Company Name  
* NOSH (Reported)  
* NOSH (BBG)  
* NOSH Proforma  
* Stock Shares  
* Warrant Shares  
* Bond Shares  
* Total Shares  
* **Monthly Exercise Limit Tab Columns:**  
* Underlying  
* Ticker  
* Company Name  
* Sec Type  
* Original Nosh  
* Original Quantity  
* Monthly Exercised Quantity  
* Monthly Exercised %  
* Monthly Sal

##### 3.3 Pay-To-Hold & Settlement View

This section is dedicated to managing the operational aspects of the portfolio, including Pay-To-Hold instruments, settlements, stock borrowing, and instruments with special terms.

* **Pay-To-Hold Tab Columns:**  
* Trade Date  
* Ticker  
* Currency  
* Counter Party  
* Side  
* SL Rate  
* PTH Amount SOD  
* PTH Amount  
* EMSA Order  
* EMSA Order Remark  
* EMSA Working  
* EMSA order  
* EMSA order Filled  
* **Short ECL Tab Columns:**  
* Trade Date  
* Ticker  
* Company Name  
* Pos Loc  
* Account  
* Short Position  
* NOSH  
* Short Ownership  
* Last Volume  
* ShortPos/ (truncated)  
* **Stock Borrow Tab Columns:**  
* Trade Date  
* Ticker  
* Company Name  
* JPM Request Locate  
* JPM Firm Locate  
* Borrow Rate  
* BofA Request Locate  
* BofA Firm Locate  
* **PO Settlement Tab Columns:**  
* Deal Num  
* Ticker  
* Company Name  
* Structure  
* Currency  
* FX Rate  
* Last Price  
* Current Position  
* Shares Allocated  
* Shares in Swap  
* Shares Hedged  
* **Deal Indication Tab Columns:**  
* Ticker  
* Company Name  
* Identification  
* Deal Type  
* Agent  
* Deal Captain  
* Indication Date  
* Currency  
* Market Cap LOC  
* Gross Proceed LOC  
* Indication Amount  
* **Reset Dates Tab Columns:**  
* Underlying  
* Ticker  
* Company Name  
* Sec Type  
* Currency  
* Trade Date  
* First Reset Date  
* Expiry Date  
* Latest Reset Date  
* Reset Up/Down  
* Market Price  
* **Coming Resets Tab Columns:**  
* Deal Num  
* Detail ID  
* Ticker  
* Account  
* Company Name  
* Announcement Date  
* Closing Date  
* Cal Days Since Announced  
* Biz Days Since Announced  
* **CB Installments Tab Columns:**  
* Underlying  
* Ticker  
* Currency  
* Installment Date  
* Total Amount  
* Outstanding Amount  
* Redeemed Amount  
* Deferred Amount  
* Converted Amount  
* Installment Amount  
* Period  
* **Excess Amount Tab Columns:**  
* Deal Num  
* Underlying  
* Ticker  
* Company Name  
* Warrants  
* Excess Amount  
* Excess Amount Threshold  
* CB Redeem/Converted Amt  
* Redeem/Converted Amt

##### 3.4 PnL View

This module is dedicated to the analysis of Profit and Loss from multiple perspectives, allowing users to dissect performance based on time-based changes and the impact of currency fluctuations.

* **PnL Change Tab Columns:**  
* Trade Date  
* Underlying  
* Ticker  
* PnL YTD  
* PnL Chg 1D  
* PnL Chg 1W  
* PnL Chg 1M  
* PnL Chg% 1D  
* PnL Chg% 1W  
* PnL Chg% 1M  
* **PnL Summary Tab Columns:**  
* Trade Date  
* Underlying  
* Currency  
* Price  
* Price (T-1)  
* Price Change  
* FX Rate  
* FX Rate (T-1)  
* FX Rate Change  
* DTL  
* Last Volume  
* ADV 3M  
* **PnL Currency Tab Columns:**  
* Trade Date  
* Currency  
* FX Rate  
* FX Rate (T-1)  
* FX Rate Change  
* CCY Exposure  
* USD Exposure  
* POS CCY Expo  
* CCY Hedged PnL  
* POS CCY PnL  
* Net CC  
* POS C (truncated)

##### 3.5 Reconciliation View

This section provides a suite of tools designed to reconcile data across different systems. These views are critical for ensuring data integrity and identifying discrepancies in positions, PnL, and trades.

* **PPS Recon Tab Columns:**  
* Value Date  
* Trade Date  
* Underlying  
* Ticker  
* Code  
* Company Name  
* Sec Type  
* Pos Loc  
* Account  
* **Settlement Recon Tab Columns:**  
* Trade Date  
* ML Report Date  
* Underlying  
* Ticker  
* Company Name  
* Pos Loc  
* Currency  
* Sec Type  
* Position Settled  
* ML Inventory  
* **Failed Trades Tab Columns:**  
* Report Date  
* Trade Date  
* Value Date  
* Settlement Date  
* Portfolio Code  
* Instrument Ref  
* Instrument Name  
* Ticker  
* Company Name  
* ISIN  
* SEDOL  
* Broker  
* Glass Reference  
* Trade Reference  
* Deal Type  
* Q  
* **PnL Recon Tab Columns:**  
* Trade Date  
* Report Date  
* Deal Num  
* Row Index  
* Underlying  
* Pos Loc  
* Stock SecID  
* Warrant SecID  
* Bond SecID  
* Stock Position  
* **Risk Input Recon Tab Columns:**  
* Value Date  
* Underlying  
* Ticker  
* Sec Type  
* Spot (MC)  
* Spot (PPD)  
* Position  
* Value (MC)  
* Value (PPD)

##### 3.6 Operational Processes View

This module serves as a dashboard for monitoring the status of automated and manual operational tasks. It provides visibility into the execution of daily procedures and their outcomes.

* **Daily Procedure Check Tab Columns:**  
* Check Date  
* Host Run Date  
* Scheduled Time  
* Procedure Name  
* Status  
* Error Message  
* Frequency  
* Scheduled Day  
* Created By  
* Created Time  
* **Operation Process Tab Columns:**  
* Process  
* Status  
* Last Run Time

##### 3.7 Market Data & Events View

This section acts as a comprehensive resource for market-related information, consolidating pricing data, trading calendars, and corporate events into a single module.

* **Market Data Tab Columns:**  
* Ticker  
* Listed Shares (mm)  
* Last Volume  
* Last Price  
* vWAP Price  
* Bid  
* Ask  
* 1D Change %  
* Implied Vol %  
* Market Status  
* Created by  
* **FX Data Tab Columns:**  
* Ticker  
* Last Price  
* Bid  
* Ask  
* Created by  
* Created Time  
* Updated by  
* Update  
* **Historical Data Tab Columns:**  
* Trade Date  
* Ticker  
* vWAP Price  
* Last Price  
* Last Volume  
* 1D Change %  
* Created By  
* Created Time  
* Updated By  
* Update  
* **Trading Calendar Tab Columns:**  
* Trade Date  
* Day of Week  
* USA  
* HKG  
* JPN  
* AUS  
* NZL  
* KOR  
* CHN  
* TWN  
* IND  
* **Market Hours Tab Columns:**  
* Market  
* Ticker  
* Session  
* Local Time  
* Session Period  
* Is Open?  
* Timezone  
* **Event Calendar Tab Columns:**  
* Underlying  
* Ticker  
* Company  
* Event Date  
* Day Of Week  
* Event Type  
* Time  
* **Event Stream Tab:**  
* This tab features a form for data entry and filtering above a data table. The form contains input fields for Record Date, Event Date, Subject, Notes, Symbol, Event Type, Recur Freq:, On Month:, On Dec:, an Alert checkbox, and buttons for Filter Event and Upload Event.  
* **Columns:**  
* Symbol  
* Record Date  
* Event Date  
* Day of Week  
* Event Type  
* Subject  
* Notes  
* Alerted?  
* Recur?  
* Created By  
* Created Time  
* Updated By  
* Updated Time  
* **Reverse Inquiry Tab Columns:**  
* Ticker  
* Company  
* Inquiry Date  
* Expiry Date  
* Deal Point  
* Agent  
* Notes

##### 3.8 Ticker & Instrument Analysis View

This module provides tools for screening, filtering, and analyzing specific financial instruments. It allows users to query the instrument universe based on various criteria.

* **Ticker Data Tab Columns:**  
* Ticker  
* Currency  
* FX Rate  
* Sector  
* Company  
* PO Lead Manager  
* FMat Cap  
* SMkt Cap  
* 1D%  
* DTL  
* **Stock Screener Tab:**  
* This tab includes filtering controls: Select Country, Sector, Recorder, Sort 1, Sort 2, ADC.  
* **Columns:**  
* OTL  
* 37% Market Cap  
* Ticker  
* Company  
* Country  
* Industry  
* Last Price  
* Market Cap (MM LOC)  
* Market Cap (MM USD)  
* ADV 3M  
* Locate Qty (MM)  
* Locate F  
* **Special Term Tab Columns:**  
* Deal Num  
* Ticker  
* Company Name  
* Sec Type  
* Position Location  
* Account  
* Effective Date  
* Position  
* **Instrument Data Tab Columns:**  
* Deal Num  
* Detail ID  
* Underlying  
* Ticker  
* Company Name  
* SecID  
* Sec Type  
* Position Location  
* Account  
* **Instrument Term Tab Columns:**  
* Deal Num  
* Detail ID  
* Underlying  
* Ticker  
* Company Name  
* Sec Type  
* Effective Date  
* Maturity Date  
* First Reset Da (truncated)

##### 3.9 Risk & Pricing View

This section is dedicated to advanced financial modeling, including risk measurement, scenario simulation, and the pricing of complex instruments like warrants and bonds.

* **Delta Change Tab Columns:**  
* Ticker  
* Company Name  
* Structure  
* Currency  
* FX Rate  
* Current Price  
* Valuation Price  
* Pos Delta  
* posDelta  
* Pos G  
* **Risk Measures Tab & Risk Inputs Tab:**  
* These two tabs share a similar data table structure for displaying risk simulation data.  
* **Columns:**  
* Seed  
* Simulation\#  
* Trial\#  
* Underlying  
* Ticker  
* Sec Type  
* Is Private  
* National  
* National Used  
* National Current  
* Currency  
* FX Rate  
* Spot Price  
* **Pricer Warrant Tab:**  
* This tab features a two-panel layout where user-editable inputs on the left drive calculations displayed on the right.  
* **Left Panel ("Terms"):**  Contains input fields for the warrant's terms, including: Valuation Date, Effective Date, Maturity Date, Underlying, Maturity Ticker, Spot Price, Strike Price, Hit Fee Dec, Currency, Hit Rate, and Interest Rate.  
* **Right Panel ("Simulations" and "Outputs"):**  Displays grids for simulation inputs (Simulations\#, Jump to 0, etc.) and the resulting calculated output values, such as Fair Value and Delta.  
* **Price Bond Tab:**  
* This tab utilizes a two-panel layout where user-editable inputs on the left drive calculations displayed on the right.  
* **Left Panel ("Terms"):**  Contains input fields for the bond's terms, such as Valuation Date, Coupon Rate, etc.  
* **Right Panel (Data Grid):**  Displays a data table with the pricing results.  
* **Columns:**  
* Ticker  
* Spot Price  
* Fair Value  
* Discount

##### 3.10 EMSA Order Management View

This module provides functionality for managing and routing EMSA (Electronic Market and Securities Access) orders, offering a clear view of order status and execution details.

* **EMSA Order Tab Columns:**  
* Sequence  
* Underlying  
* Ticker  
* Broker  
* Pos Loc  
* Side  
* Status  
* EMSA Amount  
* EMSA Routed  
* EMSA Working  
* EMSA Filled  
* **EMSA Route Tab Columns:**  
* Sequence  
* Underlying  
* Ticker  
* Broker  
* Pos Loc  
* Side  
* Status  
* EMSA Amount  
* EMSA Routed  
* EMSA Working  
* EMSA Filled  
* *Note: While the column structure is identical to the 'EMSA Order' tab, it is presumed that this tab provides a view of the same data filtered by a specific routing status or destination, a detail to be confirmed during development.*Having detailed the core application pages, the following section will summarize the common interactive elements used throughout the system.

#### 4.0 Common Interactive Elements

This section consolidates the definition of common user interface controls that appear throughout the application. Standardizing these elements is crucial for usability and development efficiency.

* **Contextual Filter Bar:**  Positioned directly above most data tables, this bar contains a set of controls specific to the current view. This may include:  
* **Date Pickers:**  Standard date selection controls (e.g., "Select Position Date") that present a calendar interface for user input.  
* **Dropdown Menus:**  Selection controls for filtering by predefined criteria (e.g., Select Country, Sector).  
* **Text Search Field:**  An input field for dynamically filtering table results based on typed text.  
* **Action Buttons:**  Buttons that trigger specific backend processes are consistently located at the bottom of the main content area. Examples include "Generate Positions," "Restart Service," or "Delete Orders," each corresponding to the context of the current view.  
* **Auto-Refresh Control:**  An "Enable Auto-Refresh" checkbox, typically located in the contextual filter bar, which allows users to toggle periodic, automatic data updates for the current view, ensuring the displayed information remains current without manual intervention.

#### 5.0 Conclusion

This requirements document delivers a detailed, feature-by-feature, and screen-by-screen specification for the "Portfolio Management Tool." The comprehensive breakdown of pages, tabs, data structures, and common interactive elements provides a clear and actionable blueprint. This report equips the development team with the necessary information to accurately reconstruct the application's user interface and core functionality, ensuring the final product aligns with the specified design and operational requirements.  

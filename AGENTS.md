# Agents Guide

This repository is designed to be friendly to AI agents.

## Project Overview
This is a Portfolio Management Tool built with **Reflex** (Python web framework). It features a dashboard for managing financial positions, compliance, risk, and operations.

## Project Structure
- `app/`: Source code for the Reflex application.
- `docs/`: specific requirements and design documents.
- `pyproject.toml`: Dependency management using `uv`.
- `rxconfig.py`: Reflex configuration.
- `.agents/`: Contains skills and other agent-specific resources.

## Development
- **Package Manager**: `uv`
- **Run Command**: `uv run reflex run`
- **Frontend**: http://localhost:3001
- **Backend**: http://0.0.0.0:8001

## Key Features & Navigation
The application uses a **Top Navigation Bar** with icons to switch between views:
- **Positions**: View holdings (Stocks, Warrants, Bonds). Includes "Generate Positions" button.
- **Compliance**: Restricted lists and undertakings.
- **PnL**: Profit and Loss analysis.
- **Risk**: Delta change and risk measures.
- **Portfolio Tools**: Pay-To-Hold and settlement views.
- **Market Data**, **Instrument**, **Events**, **Operations**, **Orders**: Additional functional modules.

**Global Elements**:
- **Header Dashboard**: Key metrics summary at the top.
- **Notifications Sidebar**: Real-time alerts on the right.

## Verification
1. Run the app: `uv run reflex run`.
2. Browse to `http://localhost:3001/`.
3. Verify that the Dashboard and Top Navigation load.
4. Click through the icons to ensure data tables render.
5. Check the Notifications Sidebar for alerts.

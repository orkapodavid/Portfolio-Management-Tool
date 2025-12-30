
# Portfolio Management Dashboard

A professional portfolio management web dashboard built with [Reflex](https://reflex.dev) (Python). This is a reimplementation of a PyQt-based desktop tool as a high-performance web application, designed for institutional trading and portfolio management workflows.

## Features

- **11-Module Navigation**: Market Data, Positions, PnL, Risk, Recon, Compliance, Portfolio Tools, Instruments, Events, Operations, Orders
- **52 Sub-Pages**: Dynamic subtab interface per module
- **Real-Time KPIs**: Daily PnL, FX Changes, YTD metrics
- **Top Movers Grids**: 5 mini-tables showing top performers
- **PnL Analysis**: Change, Full, Summary, Currency views with sparklines
- **Notification Sidebar**: Live alert cards with pagination
- **Stock Research**: Integration with yfinance for real-time data
- **Watchlist Management**: Track stocks with price alerts

## Prerequisites

- **Python**: 3.11 or higher
- **Reflex**: 0.8.20+
- **Node.js**: 18+ (installed automatically by Reflex)

## Installation

1. **Clone the repository**:
   bash
   git clone <repository-url>
   cd portfolio-dashboard
   

2. **Create a virtual environment**:
   bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   

3. **Install dependencies**:
   bash
   pip install -r requirements.txt
   

   The `requirements.txt` includes:
   
   reflex==0.8.20
   yfinance
   PyGithub
   

4. **Initialize the Reflex project** (first time only):
   bash
   reflex init
   

## Running the Application

### Development Mode

bash
reflex run


This will:
- Start the backend server on `http://localhost:8000`
- Start the frontend on `http://localhost:3000`
- Enable hot-reload for development

### Production Mode

bash
reflex run --env prod


## Project Structure


app/
├── app.py                  # Main entry point
├── constants.py            # UI constants (colors, sizes)
├── states/                 # State management classes
├── components/             # Reusable UI components
├── pages/                  # Secondary page definitions
└── services/               # External API integrations

assets/                     # Static files (favicon, placeholder images)
rxconfig.py                 # Reflex configuration


## Configuration

### rxconfig.py


import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[rx.plugins.TailwindV3Plugin()]
)


### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub API access (optional) | No |

## Key Routes

| Route | Description |
|-------|-------------|
| `/` | Main dashboard with 4-region layout |
| `/portfolios` | Portfolio management |
| `/watchlist` | Stock watchlist & alerts |
| `/research` | Stock research & analysis |
| `/reports` | Performance reports |
| `/goals` | Financial goals tracker |
| `/profile` | User profile |
| `/settings` | Application settings |

## Tech Stack

- **Framework**: [Reflex](https://reflex.dev) (Python → React/Next.js)
- **Styling**: TailwindCSS v3
- **Icons**: Lucide Icons via `rx.icon()`
- **Charts**: Recharts via `rx.recharts`
- **Data**: yfinance for market data

## Development Notes

### State Management

All application state is managed through `rx.State` classes in the `app/states/` directory. The primary state is `PortfolioDashboardState` which controls:
- Active module/subtab navigation
- Table data and pagination
- KPI metrics
- Notification feed

### UI Architecture

The app follows a 4-region layout:
1. **Top Navigation**: Module selector
2. **Performance Header**: KPIs + Top Movers
3. **Contextual Workspace**: Data tables with subtabs
4. **Notification Sidebar**: Alert cards

### Adding New Modules

1. Add subtabs to `MODULE_SUBTABS` dict in `portfolio_dashboard_state.py`
2. Create view component in `components/`
3. Add to `rx.match` in `contextual_workspace.py`

## Troubleshooting

### Common Issues

**Port already in use**:
bash
reflex run --frontend-port 3001 --backend-port 8001


**Dependency conflicts**:
bash
pip install --upgrade reflex


**Frontend not building**:
bash
rm -rf .web
reflex run


## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the patterns in `AGENTS.md`
4. Submit a pull request


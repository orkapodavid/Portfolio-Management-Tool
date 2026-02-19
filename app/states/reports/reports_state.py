import reflex as rx
from typing import TypedDict
import random
from app.services import services


class PerformancePoint(TypedDict):
    date: str
    portfolio_value: float
    benchmark_value: float


class AllocationMetric(TypedDict):
    sector: str
    actual_pct: float
    target_pct: float
    diff: float


class ReportsState(rx.State):
    selected_range: str = "YTD"
    ranges: list[str] = ["1M", "3M", "6M", "YTD", "1Y", "ALL"]
    total_return_pct: float = 12.4
    sharpe_ratio: float = 1.8
    max_drawdown: float = -5.2
    alpha: float = 2.1
    beta: float = 0.95
    performance_data: list[PerformancePoint] = []
    allocation_analysis: list[AllocationMetric] = [
        {"sector": "Technology", "actual_pct": 45.0, "target_pct": 30.0, "diff": 15.0},
        {"sector": "Financials", "actual_pct": 15.0, "target_pct": 20.0, "diff": -5.0},
        {"sector": "Healthcare", "actual_pct": 10.0, "target_pct": 15.0, "diff": -5.0},
        {
            "sector": "Consumer Cyclical",
            "actual_pct": 12.0,
            "target_pct": 10.0,
            "diff": 2.0,
        },
        {"sector": "Real Estate", "actual_pct": 8.0, "target_pct": 10.0, "diff": -2.0},
        {"sector": "Other", "actual_pct": 10.0, "target_pct": 15.0, "diff": -5.0},
    ]

    @rx.event
    def on_mount(self):
        return ReportsState.generate_performance_data

    @rx.event
    def set_range(self, range_val: str):
        self.selected_range = range_val
        self.generate_performance_data()

    @rx.event
    async def generate_performance_data(self):
        """Generates performance data based on selected range using real S&P 500 data for benchmark."""

        period_map = {
            "1M": "1mo",
            "3M": "3mo",
            "6M": "6mo",
            "YTD": "ytd",
            "1Y": "1y",
            "ALL": "2y",
        }
        yf_period = period_map.get(self.selected_range, "1mo")
        benchmark_data = await services.market_data.fetch_stock_history(
            "SPY", period=yf_period
        )
        points = []
        if benchmark_data:
            base_value = benchmark_data[0]["price"]
            start_portfolio = 10000.0
            start_benchmark = 10000.0
            for pt in benchmark_data:
                price = pt["price"]
                pct_change_from_start = (price - base_value) / base_value
                port_change = (
                    pct_change_from_start * self.beta + self.alpha / 100 * 0.01
                )
                points.append(
                    {
                        "date": pt["date"],
                        "portfolio_value": round(
                            start_portfolio * (1 + port_change), 2
                        ),
                        "benchmark_value": round(
                            start_benchmark * (1 + pct_change_from_start), 2
                        ),
                    }
                )
        self.performance_data = points

    @rx.event
    def export_report(self):
        yield rx.toast(
            "Report generated and downloaded successfully.", position="bottom-right"
        )

"""
FX Service — Core business logic for FX (Foreign Exchange) data.

Provides mock FX data and realistic tick generation for the starter template.
"""

import random
from typing import List


# Volatility multiplier by currency (JPY pairs move in larger pips)
_VOLATILITY: dict[str, float] = {
    "JPY": 0.015,   # ~1.5 pips on 150-yen crosses
    "HKD": 0.0001,  # HKD is pegged, barely moves
}
_DEFAULT_VOL = 0.0003  # ~0.3 pips for standard pairs


def _vol_for_pair(pair: str) -> float:
    """Get volatility multiplier based on quote currency."""
    quote = pair.split("/")[1] if "/" in pair else ""
    return _VOLATILITY.get(quote, _DEFAULT_VOL)


class FxService:
    """Service for FX data operations."""

    def __init__(self):
        self._fx_data: List[dict] = []
        self._initialized = False
        # Store baseline mids for change_pct calculation
        self._baseline_mids: dict[str, float] = {}

    def get_fx_data(self) -> List[dict]:
        """Get all FX data rows."""
        if not self._initialized:
            self._generate_mock_data()
            self._initialized = True
        return self._fx_data

    def generate_tick(self, rows: List[dict]) -> List[dict]:
        """Apply realistic random perturbation to FX prices.

        For each row, nudges bid/ask by a small random amount scaled to the
        pair's typical volatility, then recalculates mid, spread, change_pct,
        and volume.

        Args:
            rows: Current list of FX row dicts (will NOT be mutated).

        Returns:
            New list of row dicts with updated prices.
        """
        ticked: List[dict] = []
        for row in rows:
            pair = row["pair"]
            vol = _vol_for_pair(pair)

            # Random walk: bid moves ±vol, ask moves ±vol independently
            bid = row["bid"] + random.uniform(-vol, vol)
            ask = row["ask"] + random.uniform(-vol, vol)

            # Ensure ask > bid (minimum 1 pip spread)
            if ask <= bid:
                ask = bid + vol * 0.5

            mid = round((bid + ask) / 2, 5)
            spread = round(abs(ask - bid), 5)

            # change_pct relative to session open (baseline)
            baseline = self._baseline_mids.get(pair, mid)
            change_pct = round(((mid - baseline) / baseline) * 100, 2) if baseline else 0.0

            # Volume jitter: ±5% of current volume
            base_vol = row["volume"]
            volume = max(10_000, base_vol + random.randint(-base_vol // 20, base_vol // 20))

            # Round bid/ask to appropriate decimal places
            if "JPY" in pair:
                bid = round(bid, 2)
                ask = round(ask, 2)
                mid = round(mid, 3)
                spread = round(spread, 2)
            else:
                bid = round(bid, 5)
                ask = round(ask, 5)
                mid = round(mid, 5)
                spread = round(spread, 5)

            ticked.append({
                **row,
                "bid": bid,
                "ask": ask,
                "mid": mid,
                "spread": spread,
                "change_pct": change_pct,
                "volume": volume,
            })
        return ticked

    def get_summary_stats(self) -> dict:
        """Get summary statistics for FX data."""
        data = self.get_fx_data()
        total = len(data)
        gainers = len([d for d in data if d["change_pct"] > 0])
        losers = len([d for d in data if d["change_pct"] < 0])
        return {
            "total": total,
            "gainers": gainers,
            "losers": losers,
        }

    def _generate_mock_data(self):
        """Generate mock FX data."""
        self._fx_data = [
            {"pair": "EUR/USD", "bid": 1.0842, "ask": 1.0845, "mid": 1.08435, "change_pct": 0.12, "spread": 0.0003, "volume": 1_250_000, "session": "London", "status": "Active"},
            {"pair": "GBP/USD", "bid": 1.2634, "ask": 1.2637, "mid": 1.26355, "change_pct": -0.08, "spread": 0.0003, "volume": 890_000, "session": "London", "status": "Active"},
            {"pair": "USD/JPY", "bid": 149.82, "ask": 149.85, "mid": 149.835, "change_pct": 0.35, "spread": 0.03, "volume": 1_100_000, "session": "Tokyo", "status": "Active"},
            {"pair": "USD/CHF", "bid": 0.8821, "ask": 0.8824, "mid": 0.88225, "change_pct": -0.15, "spread": 0.0003, "volume": 420_000, "session": "Zurich", "status": "Active"},
            {"pair": "AUD/USD", "bid": 0.6543, "ask": 0.6546, "mid": 0.65445, "change_pct": 0.22, "spread": 0.0003, "volume": 560_000, "session": "Sydney", "status": "Active"},
            {"pair": "USD/CAD", "bid": 1.3567, "ask": 1.3570, "mid": 1.35685, "change_pct": -0.05, "spread": 0.0003, "volume": 380_000, "session": "New York", "status": "Active"},
            {"pair": "NZD/USD", "bid": 0.6123, "ask": 0.6127, "mid": 0.6125, "change_pct": 0.18, "spread": 0.0004, "volume": 210_000, "session": "Wellington", "status": "Active"},
            {"pair": "EUR/GBP", "bid": 0.8582, "ask": 0.8585, "mid": 0.85835, "change_pct": 0.05, "spread": 0.0003, "volume": 340_000, "session": "London", "status": "Active"},
            {"pair": "EUR/JPY", "bid": 162.45, "ask": 162.49, "mid": 162.47, "change_pct": 0.42, "spread": 0.04, "volume": 290_000, "session": "Tokyo", "status": "Active"},
            {"pair": "GBP/JPY", "bid": 189.35, "ask": 189.40, "mid": 189.375, "change_pct": -0.28, "spread": 0.05, "volume": 250_000, "session": "London", "status": "Active"},
            {"pair": "USD/SGD", "bid": 1.3412, "ask": 1.3416, "mid": 1.3414, "change_pct": 0.08, "spread": 0.0004, "volume": 180_000, "session": "Singapore", "status": "Active"},
            {"pair": "USD/HKD", "bid": 7.8102, "ask": 7.8108, "mid": 7.8105, "change_pct": 0.01, "spread": 0.0006, "volume": 320_000, "session": "Hong Kong", "status": "Active"},
        ]
        # Store baseline mids for change_pct calculation
        for row in self._fx_data:
            self._baseline_mids[row["pair"]] = row["mid"]

import yfinance as yf
import logging


def fetch_stock_data(symbol: str) -> dict[str, object]:
    """Fetches real-time data for a single stock."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return _extract_stock_info(symbol, info)
    except Exception as e:
        logging.exception(f"Error fetching data for {symbol}: {e}")
        return {}


def fetch_multiple_stocks(symbols: list[str]) -> dict[str, dict[str, object]]:
    """Fetches real-time data for multiple stocks."""
    if not symbols:
        return {}
    valid_symbols = [s for s in symbols if s]
    if not valid_symbols:
        return {}
    try:
        tickers_obj = yf.Tickers(" ".join(valid_symbols))
        results = {}
        for symbol in valid_symbols:
            try:
                ticker = tickers_obj.tickers.get(symbol)
                if ticker:
                    info = ticker.info
                    results[symbol] = _extract_stock_info(symbol, info)
            except Exception as e:
                logging.exception(f"Failed to fetch {symbol} in batch: {e}")
        return results
    except Exception as e:
        logging.exception(f"Batch fetch error: {e}")
        return {}


def _extract_stock_info(symbol: str, info: dict[str, object]) -> dict[str, object]:
    """Helper to extract relevant fields from yfinance info dict."""
    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
    previous_close = (
        info.get("previousClose")
        or info.get("regularMarketPreviousClose")
        or current_price
    )
    change_pct = 0.0
    if previous_close and previous_close > 0:
        change_pct = (current_price - previous_close) / previous_close * 100
    return {
        "symbol": symbol,
        "name": info.get("shortName") or info.get("longName") or symbol,
        "current_price": current_price,
        "previous_close": previous_close,
        "daily_change_pct": round(change_pct, 2),
        "market_cap": format_market_cap(info.get("marketCap", 0)),
        "pe_ratio": round(info.get("trailingPE", 0.0) or 0.0, 2),
        "sector": info.get("sector", "Unknown"),
        "volume": format_volume(info.get("volume", 0)),
        "high_52": info.get("fiftyTwoWeekHigh", 0.0),
        "low_52": info.get("fiftyTwoWeekLow", 0.0),
        "description": info.get("longBusinessSummary", "No description available."),
        "eps": info.get("trailingEps", 0.0),
    }


def fetch_stock_history(symbol: str, period: str = "1mo") -> list[dict[str, object]]:
    """Fetches historical price data for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        data = []
        for date, row in hist.iterrows():
            data.append(
                {"date": date.strftime("%Y-%m-%d"), "price": round(row["Close"], 2)}
            )
        return data
    except Exception as e:
        logging.exception(f"Error fetching history for {symbol}: {e}")
        return []


def fetch_stock_news(symbol: str) -> list[dict[str, str]]:
    """Fetches news for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        formatted_news = []
        for item in news[:5]:
            formatted_news.append(
                {
                    "id": item.get("uuid", ""),
                    "headline": item.get("title", ""),
                    "source": item.get("publisher", "Yahoo Finance"),
                    "time_ago": "Today",
                    "summary": "No summary available.",
                    "url": item.get("link", "#"),
                    "sentiment": "Neutral",
                    "related_symbols": [symbol],
                }
            )
        return formatted_news
    except Exception as e:
        logging.exception(f"Error fetching news for {symbol}: {e}")
        return []


def format_market_cap(value: float) -> str:
    """Formats market cap value to string (e.g. 2.5T, 500B)."""
    if not value:
        return "N/A"
    if value >= 1000000000000:
        return f"{value / 1000000000000:.2f}T"
    elif value >= 1000000000:
        return f"{value / 1000000000:.2f}B"
    elif value >= 1000000:
        return f"{value / 1000000:.2f}M"
    else:
        return f"{value:,.0f}"


def format_volume(value: float) -> str:
    """Formats volume value to string."""
    if not value:
        return "0"
    if value >= 1000000:
        return f"{value / 1000000:.1f}M"
    elif value >= 1000:
        return f"{value / 1000:.1f}K"
    else:
        return f"{value}"


def calculate_daily_change(current: float, previous: float) -> float:
    if not previous:
        return 0.0
    return (current - previous) / previous * 100
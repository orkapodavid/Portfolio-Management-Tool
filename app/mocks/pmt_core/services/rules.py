def get_active_alerts() -> list[dict]:
    """Mock service to get active rule alerts."""
    return [
        {
            "id": 1,
            "header": "Begin Covering",
            "ticker": "AAPL",
            "timestamp": "09:30 AM",
            "instruction": "Action required before market open",
            "type": "alert",
            "read": False,
        },
        {
            "id": 2,
            "header": "Risk Alert",
            "ticker": "TSLA",
            "timestamp": "11:00 AM",
            "instruction": "Delta exposure exceeds threshold",
            "type": "warning",
            "read": False,
        },
    ]
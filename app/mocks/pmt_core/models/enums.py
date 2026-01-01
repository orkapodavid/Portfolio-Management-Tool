from enum import Enum


class ReportType(Enum):
    PNL = "pnl"
    POSITIONS = "positions"
    RISK = "risk"
    MARKET_DATA = "market_data"
    COMPLIANCE = "compliance"


class AssetClass(Enum):
    EQUITY = "Equity"
    BOND = "Bond"
    FX = "FX"
    OPTION = "Option"
    WARRANT = "Warrant"
    COMMODITY = "Commodity"
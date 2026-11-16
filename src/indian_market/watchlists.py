"""Starter symbol watchlists; these are not a live price feed."""
NIFTY_WATCHLIST = [
    {"symbol": "NIFTY", "exchange": "NSE", "kind": "index"},
    {"symbol": "BANKNIFTY", "exchange": "NSE", "kind": "index"},
]

def validate_watchlist(items: list[dict]) -> list[dict]:
    validated = []
    for item in items:
        symbol = str(item.get("symbol", "")).strip().upper()
        exchange = str(item.get("exchange", "")).strip().upper()
        if not symbol or exchange not in {"NSE", "BSE"}:
            raise ValueError(f"Invalid watchlist item: {item!r}")
        validated.append({**item, "symbol": symbol, "exchange": exchange})
    return validated

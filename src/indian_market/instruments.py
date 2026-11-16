"""Indian instrument metadata helpers.

Keep exchange/contract data external and timestamped; do not hard-code changing
lot sizes or expiry calendars as authoritative market data.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Instrument:
    symbol: str
    exchange: str
    segment: str
    lot_size: int | None = None


def validate_exchange(exchange: str) -> str:
    exchange = exchange.upper()
    if exchange not in {"NSE", "BSE"}:
        raise ValueError("Exchange must be NSE or BSE")
    return exchange

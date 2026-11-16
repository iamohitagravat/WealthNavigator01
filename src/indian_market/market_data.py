"""Provider-neutral market data contracts."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

@dataclass(frozen=True)
class Candle:
    symbol: str
    exchange: str
    interval: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def validate(self) -> None:
        if self.exchange not in {"NSE", "BSE"}:
            raise ValueError("exchange must be NSE or BSE")
        if min(self.open, self.high, self.low, self.close) <= 0:
            raise ValueError("OHLC prices must be positive")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("invalid candle high")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("invalid candle low")
        if self.volume < 0:
            raise ValueError("volume cannot be negative")

@dataclass(frozen=True)
class Quote:
    symbol: str
    exchange: str
    last_price: float
    timestamp: datetime
    source: str

class MarketDataProvider(Protocol):
    def get_quote(self, symbol: str, exchange: str) -> Quote: ...
    def get_history(self, symbol: str, exchange: str, interval: str,
                    start: datetime, end: datetime) -> list[Candle]: ...

def is_fresh(timestamp: datetime, max_age_seconds: int,
             now: datetime | None = None) -> bool:
    if timestamp.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    age = (current - timestamp).total_seconds()
    return 0 <= age <= max_age_seconds

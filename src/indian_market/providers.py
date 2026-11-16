"""Provider adapter scaffolding. No unauthorised scraping or fake live quotes."""
from dataclasses import dataclass
from datetime import datetime
from .market_data import Candle, Quote, MarketDataProvider

@dataclass
class NotConfiguredProvider:
    reason: str = "No market-data provider configured."
    def get_quote(self, symbol: str, exchange: str) -> Quote:
        raise RuntimeError(self.reason + " Import licensed CSV data or configure a provider.")
    def get_history(self, symbol: str, exchange: str, interval: str,
                    start: datetime, end: datetime) -> list[Candle]:
        raise RuntimeError(self.reason + " Import licensed CSV data or configure a provider.")

def provider_status(provider: MarketDataProvider | None) -> dict:
    if provider is None or isinstance(provider, NotConfiguredProvider):
        return {"configured": False, "live_data": False,
                "message": "No provider configured; do not create live trade signals."}
    return {"configured": True, "live_data": True,
            "message": "Provider supplied; validate entitlement and quote timestamps."}

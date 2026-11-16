"""Optional Yahoo Finance historical-data adapter via yfinance."""
from datetime import datetime
from .market_data import Candle, Quote

INDEX_TICKERS = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK"}

def yahoo_ticker(symbol: str, exchange: str) -> str:
    symbol, exchange = symbol.strip().upper(), exchange.strip().upper()
    if exchange not in {"NSE", "BSE"}:
        raise ValueError("Only NSE and BSE symbols are supported")
    if exchange == "NSE" and symbol in INDEX_TICKERS:
        return INDEX_TICKERS[symbol]
    return symbol + (".NS" if exchange == "NSE" else ".BO")

class YahooFinanceHistoryProvider:
    def get_quote(self, symbol: str, exchange: str) -> Quote:
        raise RuntimeError("Historical candles only; no certified live quote timestamps.")

    def get_history(self, symbol: str, exchange: str, interval: str,
                    start: datetime, end: datetime) -> list[Candle]:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise RuntimeError("Install optional dependency: pip install yfinance") from exc
        if start.tzinfo is None or end.tzinfo is None:
            raise ValueError("start and end must be timezone-aware")
        ticker = yahoo_ticker(symbol, exchange)
        frame = yf.Ticker(ticker).history(start=start, end=end, interval=interval,
                                          auto_adjust=False, actions=False)
        if frame.empty:
            return []
        results = []
        for stamp, row in frame.iterrows():
            ts = stamp.to_pydatetime()
            if ts.tzinfo is None:
                raise ValueError("Provider returned a naive timestamp")
            candle = Candle(symbol.upper(), exchange.upper(), interval, ts,
                float(row["Open"]), float(row["High"]), float(row["Low"]),
                float(row["Close"]), int(row.get("Volume", 0)))
            candle.validate()
            results.append(candle)
        return results

"""CSV OHLCV import for user-owned/licensed historical market data."""
import csv
from datetime import datetime
from pathlib import Path
from .market_data import Candle

def load_candles_csv(path: str | Path) -> list[Candle]:
    candles: list[Candle] = []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "symbol", "exchange", "interval", "open", "high", "low", "close", "volume"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV is missing required OHLCV columns")
        for line_no, row in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(row["timestamp"].strip().replace("Z", "+00:00"))
                if timestamp.tzinfo is None:
                    raise ValueError("timestamp must include timezone")
                candle = Candle(row["symbol"].strip().upper(), row["exchange"].strip().upper(),
                    row["interval"].strip(), timestamp, float(row["open"]), float(row["high"]),
                    float(row["low"]), float(row["close"]), int(row["volume"]))
                candle.validate()
                candles.append(candle)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid CSV row {line_no}: {exc}") from exc
    return candles

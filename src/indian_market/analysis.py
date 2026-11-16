from dataclasses import dataclass
from typing import Literal

Signal = Literal["BUY", "SELL", "WAIT"]

@dataclass
class TradePlan:
    signal: Signal
    entry: float | None
    stop_loss: float | None
    targets: list[float]
    risk_reward: float | None
    rationale: list[str]


def sma(values: list[float], period: int) -> float | None:
    if len(values) < period or period <= 0:
        return None
    return sum(values[-period:]) / period


def basic_trade_plan(closes: list[float], support: float | None = None,
                     resistance: float | None = None) -> TradePlan:
    """Conservative educational signal helper; not financial advice."""
    if len(closes) < 20:
        return TradePlan("WAIT", None, None, [], None, ["At least 20 closes are required."])
    last = closes[-1]
    fast = sma(closes, 5)
    slow = sma(closes, 20)
    rationale = [f"Last={last:.2f}", f"SMA5={fast:.2f}", f"SMA20={slow:.2f}"]
    if fast and slow and fast > slow and (resistance is None or last > resistance):
        entry = last
        stop = support if support and support < entry else entry * 0.99
        target = entry + 2 * (entry - stop)
        return TradePlan("BUY", entry, stop, [target], 2.0, rationale + ["Short-term trend is above the 20-period average."])
    if fast and slow and fast < slow and (support is None or last < support):
        entry = last
        stop = resistance if resistance and resistance > entry else entry * 1.01
        target = entry - 2 * (stop - entry)
        return TradePlan("SELL", entry, stop, [target], 2.0, rationale + ["Short-term trend is below the 20-period average."])
    return TradePlan("WAIT", None, None, [], None, rationale + ["No high-confidence trigger under the basic rules."])

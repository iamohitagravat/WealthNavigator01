from dataclasses import dataclass

@dataclass
class PositionSize:
    quantity: int
    risk_per_unit: float
    total_risk: float


def position_size(capital: float, risk_pct: float, entry: float, stop: float, lot_size: int = 1) -> PositionSize:
    if capital <= 0 or risk_pct <= 0 or entry <= 0 or stop <= 0 or entry == stop or lot_size <= 0:
        raise ValueError("Invalid risk or price inputs")
    risk_budget = capital * risk_pct / 100
    risk_per_unit = abs(entry - stop)
    raw_qty = int(risk_budget // risk_per_unit)
    quantity = (raw_qty // lot_size) * lot_size
    return PositionSize(quantity, risk_per_unit, quantity * risk_per_unit)

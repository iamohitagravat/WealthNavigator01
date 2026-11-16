"""Local paper-trading ledger. This module never sends broker orders."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fill:
    symbol: str
    side: str
    quantity: int
    price: float
    fees: float
    timestamp: str


@dataclass
class Position:
    quantity: int = 0
    average_price: float = 0.0


@dataclass
class PaperAccount:
    initial_cash: float
    fee_bps: float = 3.0
    slippage_bps: float = 2.0
    cash: float = field(init=False)
    positions: dict[str, Position] = field(default_factory=dict)
    fills: list[Fill] = field(default_factory=list)
    realized_pnl: float = 0.0

    def __post_init__(self):
        if self.initial_cash <= 0 or self.fee_bps < 0 or self.slippage_bps < 0:
            raise ValueError("Cash must be positive and costs cannot be negative")
        self.cash = float(self.initial_cash)

    def _execute(self, symbol: str, side: str, quantity: int,
                 reference_price: float, timestamp: str = "") -> Fill:
        symbol = symbol.strip().upper()
        if not symbol or side not in {"BUY", "SELL"}:
            raise ValueError("A symbol and BUY/SELL side are required")
        if quantity <= 0 or reference_price <= 0:
            raise ValueError("Quantity and price must be positive")
        slip = self.slippage_bps / 10000
        price = reference_price * (1 + slip if side == "BUY" else 1 - slip)
        gross = price * quantity
        fees = gross * self.fee_bps / 10000
        pos = self.positions.setdefault(symbol, Position())
        if side == "BUY":
            debit = gross + fees
            if debit > self.cash:
                raise ValueError("Insufficient cash for paper BUY")
            new_qty = pos.quantity + quantity
            pos.average_price = ((pos.average_price * pos.quantity) + gross) / new_qty
            pos.quantity = new_qty
            self.cash -= debit
        else:
            if quantity > pos.quantity:
                raise ValueError("SELL quantity exceeds held position; shorting is disabled")
            self.cash += gross - fees
            self.realized_pnl += (price - pos.average_price) * quantity - fees
            pos.quantity -= quantity
            if pos.quantity == 0:
                pos.average_price = 0.0
        fill = Fill(symbol, side, quantity, price, fees, timestamp)
        self.fills.append(fill)
        return fill

    def buy(self, symbol: str, quantity: int, price: float, timestamp: str = "") -> Fill:
        return self._execute(symbol, "BUY", quantity, price, timestamp)

    def sell(self, symbol: str, quantity: int, price: float, timestamp: str = "") -> Fill:
        return self._execute(symbol, "SELL", quantity, price, timestamp)

    def equity(self, marks: dict[str, float] | None = None) -> float:
        marks = marks or {}
        value = 0.0
        for symbol, pos in self.positions.items():
            mark = marks.get(symbol, pos.average_price)
            if mark <= 0:
                raise ValueError("Mark prices must be positive")
            value += pos.quantity * mark
        return self.cash + value

    def unrealized_pnl(self, marks: dict[str, float] | None = None) -> float:
        marks = marks or {}
        return sum((marks.get(s, p.average_price) - p.average_price) * p.quantity
                   for s, p in self.positions.items())

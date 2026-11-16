"""Simple moving-average crossover backtest with next-bar-open execution."""
from dataclasses import dataclass
from .market_data import Candle
from .paper_trading import PaperAccount


@dataclass(frozen=True)
class BacktestResult:
    initial_cash: float
    final_equity: float
    net_pnl: float
    return_pct: float
    trades: int
    win_rate_pct: float
    max_drawdown_pct: float


def run_sma_crossover(candles: list[Candle], initial_cash: float = 100000,
                      fast_period: int = 5, slow_period: int = 20,
                      quantity: int = 1, fee_bps: float = 3,
                      slippage_bps: float = 2) -> BacktestResult:
    """Long-only crossover. Signal uses completed closes; fill occurs next candle open."""
    if fast_period <= 0 or slow_period <= fast_period or quantity <= 0:
        raise ValueError("Require 0 < fast_period < slow_period and positive quantity")
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    if len(candles) < slow_period + 1:
        raise ValueError("Not enough candles for the requested periods and next-bar execution")
    ordered = sorted(candles, key=lambda c: c.timestamp)
    for candle in ordered:
        candle.validate()
    if len({c.timestamp for c in ordered}) != len(ordered):
        raise ValueError("Duplicate candle timestamps are not allowed")
    symbol = ordered[0].symbol
    if any(c.symbol != symbol for c in ordered):
        raise ValueError("Backtest accepts one symbol at a time")

    account = PaperAccount(initial_cash, fee_bps, slippage_bps)
    completed_trade_pnls: list[float] = []
    entry_equity = None
    peak = initial_cash
    max_dd = 0.0
    marks = {symbol: ordered[0].close}

    for i in range(slow_period, len(ordered)):
        # Signal is calculated only from bars strictly before the execution bar.
        history = [c.close for c in ordered[:i]]
        fast_now = sum(history[-fast_period:]) / fast_period
        slow_now = sum(history[-slow_period:]) / slow_period
        prev_fast = sum(history[-fast_period-1:-1]) / fast_period
        prev_slow = sum(history[-slow_period-1:-1]) / slow_period
        bar = ordered[i]
        marks[symbol] = bar.close
        held = account.positions.get(symbol)
        has_position = bool(held and held.quantity)
        crossed_up = prev_fast <= prev_slow and fast_now > slow_now
        crossed_down = prev_fast >= prev_slow and fast_now < slow_now

        if crossed_up and not has_position:
            try:
                account.buy(symbol, quantity, bar.open, bar.timestamp.isoformat())
                entry_equity = account.realized_pnl
            except ValueError:
                pass
        elif crossed_down and has_position:
            before = account.realized_pnl
            account.sell(symbol, held.quantity, bar.open, bar.timestamp.isoformat())
            completed_trade_pnls.append(account.realized_pnl - before)
            entry_equity = None

        equity = account.equity(marks)
        peak = max(peak, equity)
        if peak:
            max_dd = max(max_dd, (peak - equity) / peak * 100)

    # Liquidate any open position at the final close for a closed-trade result.
    held = account.positions.get(symbol)
    if held and held.quantity:
        before = account.realized_pnl
        last = ordered[-1]
        account.sell(symbol, held.quantity, last.close, last.timestamp.isoformat())
        completed_trade_pnls.append(account.realized_pnl - before)
    final_equity = account.cash
    net = final_equity - initial_cash
    wins = sum(p > 0 for p in completed_trade_pnls)
    return BacktestResult(initial_cash, final_equity, net,
        net / initial_cash * 100, len(completed_trade_pnls),
        wins / len(completed_trade_pnls) * 100 if completed_trade_pnls else 0.0,
        max_dd)

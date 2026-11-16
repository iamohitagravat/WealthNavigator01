import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from indian_market.market_data import Candle
from indian_market.backtest import run_sma_crossover


def make_candles(closes):
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return [Candle("TEST", "NSE", "1d", start + timedelta(days=i),
                   c, c + 1, c - 1, c, 1000) for i, c in enumerate(closes)]


def test_backtest_returns_valid_metrics():
    prices = [100] * 25 + list(range(100, 120)) + list(range(120, 90, -1))
    result = run_sma_crossover(make_candles(prices), fast_period=3, slow_period=8,
                               quantity=1, fee_bps=0, slippage_bps=0)
    assert result.trades >= 1
    assert result.final_equity > 0
    assert result.return_pct == result.net_pnl / result.initial_cash * 100

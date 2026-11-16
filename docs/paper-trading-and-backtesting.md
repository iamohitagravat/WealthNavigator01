# Paper Trading and Backtesting

## Paper account
`PaperAccount` is a local simulation ledger. It supports BUY/SELL fills, average-cost positions, cash, realized/unrealized P&L, marked equity, configurable fee and slippage basis points, and prevents short selling and overspending. It never connects to a broker.

Example:

```python
from indian_market.paper_trading import PaperAccount

account = PaperAccount(initial_cash=100000, fee_bps=3, slippage_bps=2)
account.buy("RELIANCE", 10, 1250, "2025-01-01T09:30:00+05:30")
print(account.equity({"RELIANCE": 1260}))
account.sell("RELIANCE", 10, 1260, "2025-01-01T15:00:00+05:30")
print(account.realized_pnl)
```

## Backtest
`run_sma_crossover` is an educational long-only moving-average crossover example. It calculates a signal from completed candles and executes at the following candle's open, avoiding same-bar look-ahead. Any open position is liquidated at the final close. It reports net P&L, return, closed trades, win rate and peak-to-trough drawdown.

```python
from datetime import datetime, timezone
from indian_market.yfinance_provider import YahooFinanceHistoryProvider
from indian_market.backtest import run_sma_crossover

provider = YahooFinanceHistoryProvider()
candles = provider.get_history(
    "NIFTY", "NSE", "1d",
    datetime(2023, 1, 1, tzinfo=timezone.utc),
    datetime(2025, 1, 1, tzinfo=timezone.utc),
)
result = run_sma_crossover(candles, initial_cash=100000, fast_period=5, slow_period=20)
print(result)
```

Yahoo Finance is an unofficial historical-data source and can be incomplete or delayed. Results are hypothetical, sensitive to parameters, and do not model taxes, exchange charges, STT, GST, stamp duty, market impact, corporate actions beyond provider adjustments, or F&O contract/lot rules. Configure realistic costs before relying on results. This is not investment advice.

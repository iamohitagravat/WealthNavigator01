# Indian Market Pro Trading Assistant

A Python trading-research and paper-trading toolkit for Indian markets (NSE/BSE), including NIFTY, BANK NIFTY and equities.

## Included
- Technical-analysis helper and risk-based position sizing
- NSE/BSE instrument validation, market-session context and watchlists
- CSV OHLCV import and optional Yahoo Finance historical candles
- Local paper account: cash, positions, average-cost basis, fees, slippage, realized/unrealized P&L and equity
- Long-only SMA crossover backtest with next-bar-open execution and performance metrics
- Automated unit tests

## Quick start
Python 3.10+ recommended.

```bash
git clone https://github.com/iamohitagravat/WealthNavigator01.git
cd WealthNavigator01
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
```

## Historical data example
Install the optional Yahoo Finance adapter (already listed in requirements):

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
result = run_sma_crossover(candles, initial_cash=100000)
print(result)
```

Run examples from the repository root with `PYTHONPATH=src` (PowerShell: `$env:PYTHONPATH="src"`).

## Important limitations
- Yahoo Finance integration is unofficial historical research data, not a certified real-time feed. It can be delayed, incomplete or unavailable.
- No broker connection, live quotes, live orders, or automated execution is implemented. Paper trading only.
- The included crossover is an educational baseline, not a validated profitable strategy.
- Backtests are hypothetical and do not fully model Indian taxes/charges, liquidity, market impact, corporate actions, F&O expiry/lot-size changes or option Greeks. Use realistic assumptions and out-of-sample validation.
- This project is educational software, not investment advice. Trading can cause substantial losses.

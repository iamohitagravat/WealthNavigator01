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

## Visual dashboard (GitHub Pages)

A responsive browser dashboard is available at `index.html`. It includes a sample watchlist, chart, risk calculator and local paper-order simulator. The sample prices are explicitly illustrative, not live market data. CSV import reads Close values locally in your browser.

To publish it:
1. Open the repository on GitHub and go to **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **main**, folder **/ (root)**, then click **Save**.
4. Wait for GitHub Pages to publish. The site URL will appear in Settings → Pages.

Dashboard source: [index.html](index.html). No broker credentials are requested and no real orders can be sent.

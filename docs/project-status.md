# Project Status

## Implemented
- NSE/BSE instrument and market-session helpers
- Basic SMA trade-plan helper and risk-based position sizing
- Provider-neutral OHLCV/quote contracts and data freshness checks
- CSV historical candle loader
- Optional unofficial Yahoo Finance historical-candle adapter
- Local paper account with fee/slippage assumptions and no short selling
- Educational long-only SMA crossover backtest using next-bar-open fills
- Unit tests and GitHub Actions test workflow

## Not implemented
- Broker login, live market-data streaming, live order placement or auto-trading
- Exchange-certified real-time data
- Complete Indian transaction-cost/tax model
- Options-chain analytics, Greeks, expiry-aware F&O contract selection or lot-size automation
- Production-grade portfolio/risk monitoring

## How to validate
Install `requirements-dev.txt` and run `PYTHONPATH=src pytest -q` from the repository root. GitHub Actions will run the same tests on pushes and pull requests to main.

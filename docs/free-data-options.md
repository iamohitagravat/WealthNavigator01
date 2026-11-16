# Free / low-cost Indian market data

## Recommended first step
Use official exchange-published end-of-day reports where available, or import
historical OHLCV files you are authorised to use. NSE's research-data list
identifies public datasets including daily security-wise OHLC/price-volume and
historical reports:
https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Data%20list%20under%20NSE%20Data%20Sharing%20Policy%20for%20Research%20and%20Analysis_20250728.pdf

## Optional Yahoo Finance historical adapter
The repository includes YahooFinanceHistoryProvider as an optional personal
research/education adapter. Install dependencies with pip install -r
requirements.txt. Examples: RELIANCE on NSE maps to RELIANCE.NS; NIFTY maps to
^NSEI; BANKNIFTY maps to ^NSEBANK.

Limitations:
- yfinance is an unofficial community library, not affiliated with Yahoo.
- Its README says Yahoo Finance data is intended for personal use only.
- Availability, history depth, intervals and latency can change.
- The adapter returns historical candles only; it deliberately does not claim
  a live quote or execution-grade timestamp.
- It does not provide a complete Indian options-chain/expired-options feed.
- Do not redistribute data or use it commercially without required rights.

References:
- https://github.com/ranaroussi/yfinance
- https://www.nseindia.com/market-data

## Safety
Never use delayed or stale data to generate an actionable live order. Confirm
prices and contract details with an authorised source before any trade. The
project remains paper-trading-first and has no live order execution.

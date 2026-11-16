# Market data setup without a broker

## Current integration
Import OHLCV CSV files from a source you are authorised to use. The loader
validates required columns, timezone-aware timestamps, NSE/BSE exchange codes
and OHLCV consistency. The sample CSV contains illustrative test data, not
actual market prices.

## Real-time data
No live NSE/BSE feed is enabled in this repository. NSE Data & Analytics offers
real-time feeds and authorised-vendor routes; subscription, permitted use and
pricing depend on the product and agreement. Review:
- https://www.nseindia.com/market-data/real-time-data-subscription
- https://www.nseindia.com/static/market-data/nse-data-policy

Do not scrape exchange websites or depend on undocumented endpoints as a live
trading feed. Confirm NSE/BSE coverage, index and F&O entitlements, latency,
historical depth, redistribution rights, API limits and cost before choosing
a vendor.

## Configure a vendor later
Implement MarketDataProvider in src/indian_market/market_data.py using the
vendor's documented SDK/API. Keep credentials in environment variables or a
secret manager, never in Git. Add adapter tests with mocked responses.
The default NotConfiguredProvider intentionally raises an error rather than
returning fabricated prices.

## CSV format
timestamp,symbol,exchange,interval,open,high,low,close,volume

Example timestamp: 2026-11-13T09:15:00+05:30.
All imported data must be licensed/authorised for your intended use.

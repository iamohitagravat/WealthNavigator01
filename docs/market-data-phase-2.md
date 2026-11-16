# Phase 2 — Indian market data foundation

## Included
- Provider-neutral quote and OHLCV candle contracts
- Timestamp freshness validation
- NSE/BSE symbol watchlist validation
- Approximate IST weekday cash-session context
- Example provider configuration

## Not yet included
This phase does not fetch live NSE/BSE prices, option chains, FII/DII flows,
corporate announcements or exchange holiday calendars. Those require a chosen
data provider, credentials where applicable, and compliance with provider
licences and exchange terms.

## Next integration
Choose a broker API you already use or a licensed market-data vendor. Implement
the MarketDataProvider interface, add provider contract tests, and keep secrets
in environment variables. Verify timestamps, instrument identifiers, rate
limits and data entitlements.

## Trading safety
Stale or missing data must result in WAIT / no-trade. Never generate a
confident entry from a delayed quote without clearly labelling its delay.

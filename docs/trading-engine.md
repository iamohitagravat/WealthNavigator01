# Trading Engine

The first implementation is intentionally provider-neutral.

## Signal flow
1. Load timestamped market data.
2. Validate instrument/exchange and data freshness.
3. Calculate trend and structure.
4. Identify support/resistance and derivatives context when available.
5. Generate a setup only when entry and invalidation are explicit.
6. Calculate position size from a fixed risk budget.
7. Route to paper trading by default.

## No fabricated data
If live prices, open interest, FII/DII numbers, corporate events, lot sizes or expiry information are unavailable, the assistant must say so rather than invent values.

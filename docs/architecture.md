# Architecture

The assistant is organized into four layers:

1. **Market data** — price/volume, instruments, corporate events and market calendar.
2. **Analysis** — trend, price action, support/resistance, indicators and derivatives context.
3. **Risk** — position sizing, stop/invalidation, risk/reward and exposure limits.
4. **Execution** — paper trading by default; live broker integration only as a separately authorized layer.

Future integrations should use adapters so data and broker providers can be changed without rewriting the analysis layer.

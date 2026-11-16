import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from indian_market.market_data import Candle, is_fresh
from indian_market.market_context import regular_session_context
from indian_market.watchlists import NIFTY_WATCHLIST, validate_watchlist

def test_candle_validates():
    Candle("ABC", "NSE", "5m", datetime.now(timezone.utc),
           100, 105, 98, 103, 1000).validate()

def test_freshness():
    now = datetime.now(timezone.utc)
    assert is_fresh(now - timedelta(seconds=10), 30, now)
    assert not is_fresh(now - timedelta(seconds=60), 30, now)

def test_watchlist():
    assert validate_watchlist(NIFTY_WATCHLIST)[0]["symbol"] == "NIFTY"

def test_session_has_caveat():
    result = regular_session_context(datetime(2026, 11, 16, 10, 0,
                                              tzinfo=timezone.utc))
    assert "Approximate" in result.note

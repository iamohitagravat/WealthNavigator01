import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from indian_market.yfinance_provider import yahoo_ticker, YahooFinanceHistoryProvider

def test_symbol_mapping():
    assert yahoo_ticker("RELIANCE", "NSE") == "RELIANCE.NS"
    assert yahoo_ticker("NIFTY", "NSE") == "^NSEI"
    assert yahoo_ticker("BANKNIFTY", "NSE") == "^NSEBANK"
    assert yahoo_ticker("RELIANCE", "BSE") == "RELIANCE.BO"

def test_no_fake_live_quote():
    try:
        YahooFinanceHistoryProvider().get_quote("NIFTY", "NSE")
    except RuntimeError as exc:
        assert "Historical candles only" in str(exc)
    else:
        raise AssertionError("Historical adapter must not claim a live quote")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from indian_market.csv_feed import load_candles_csv
from indian_market.providers import NotConfiguredProvider, provider_status

def test_sample_csv_loads():
    path = Path(__file__).parents[1] / "examples" / "sample_ohlcv.csv"
    candles = load_candles_csv(path)
    assert len(candles) == 2
    assert candles[0].symbol == "RELIANCE"

def test_provider_fails_closed():
    provider = NotConfiguredProvider()
    assert provider_status(provider)["live_data"] is False
    try:
        provider.get_quote("NIFTY", "NSE")
    except RuntimeError as exc:
        assert "No market-data provider configured" in str(exc)
    else:
        raise AssertionError("Unconfigured provider must not fabricate a quote")

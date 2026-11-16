import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from indian_market.analysis import basic_trade_plan, sma
from indian_market.risk import position_size


def test_sma():
    assert sma([1, 2, 3, 4, 5], 5) == 3


def test_wait_when_insufficient_data():
    assert basic_trade_plan([100] * 10).signal == "WAIT"


def test_position_size():
    p = position_size(100000, 1, 100, 98, 1)
    assert p.quantity == 500
    assert p.total_risk == 1000

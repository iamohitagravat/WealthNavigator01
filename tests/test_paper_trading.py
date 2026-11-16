import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pytest
from indian_market.paper_trading import PaperAccount


def test_buy_sell_accounting_and_costs():
    account = PaperAccount(10000, fee_bps=0, slippage_bps=0)
    account.buy("RELIANCE", 10, 100)
    assert account.cash == 9000
    assert account.equity({"RELIANCE": 110}) == 10100
    account.sell("RELIANCE", 10, 110)
    assert account.cash == 10100
    assert account.realized_pnl == 100


def test_prevents_short_selling_and_overspend():
    account = PaperAccount(1000, fee_bps=0, slippage_bps=0)
    with pytest.raises(ValueError):
        account.buy("NIFTY", 100, 100)
    with pytest.raises(ValueError):
        account.sell("NIFTY", 1, 100)


def test_costs_reduce_cash():
    account = PaperAccount(10000, fee_bps=10, slippage_bps=10)
    fill = account.buy("ABC", 1, 100)
    assert fill.price > 100
    assert account.cash < 9900

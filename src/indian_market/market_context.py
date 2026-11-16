"""Indian market context helpers; schedules and contract metadata are data-fed."""
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

@dataclass(frozen=True)
class MarketSession:
    is_regular_session: bool
    local_time: datetime
    note: str

def regular_session_context(now: datetime | None = None) -> MarketSession:
    """Approximate standard NSE/BSE cash session, weekdays 09:15–15:30 IST.

    Does not account for holidays, special sessions, Muhurat trading or
    segment-specific schedules. Verify the official exchange calendar.
    """
    local = (now or datetime.now(IST)).astimezone(IST)
    weekday = local.weekday() < 5
    minutes = local.hour * 60 + local.minute
    active = weekday and 555 <= minutes <= 930
    return MarketSession(active, local,
        "Approximate weekday cash-market window only; verify official exchange calendar.")

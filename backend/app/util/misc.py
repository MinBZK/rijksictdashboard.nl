import datetime

from dateutil.relativedelta import relativedelta


def get_timedelta_in_years(
    start: datetime.date | None, end: datetime.date | None
) -> float | None:
    if start is not None and end is not None:
        return (
            relativedelta(end, start).years
            + relativedelta(end, start).months / 12
            + relativedelta(end, start).days / 365
        )

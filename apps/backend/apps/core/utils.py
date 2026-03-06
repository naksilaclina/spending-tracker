from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from dateutil.relativedelta import relativedelta

TWOPLACES = Decimal("0.01")


def clamp_day(year: int, month: int, day_value: str | int) -> int:
    if str(day_value).upper() == "LAST":
        return monthrange(year, month)[1]
    return min(int(day_value), monthrange(year, month)[1])


def month_sequence(start: date, end: date) -> list[date]:
    cursor = start.replace(day=1)
    boundary = end.replace(day=1)
    months: list[date] = []
    while cursor <= boundary:
        months.append(cursor)
        cursor = cursor + relativedelta(months=1)
    return months


def split_amount(total: Decimal, count: int) -> list[Decimal]:
    if count <= 0:
        return []
    base = (total / count).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    values = [base for _ in range(count)]
    difference = total - sum(values)
    if values:
        values[-1] = (values[-1] + difference).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return values


def decimal_to_str(value: Decimal) -> str:
    return format(value.quantize(TWOPLACES), "f")

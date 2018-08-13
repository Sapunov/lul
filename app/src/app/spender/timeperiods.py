from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from app.spender.models import Transaction


def start_of_day(day=None):

    if day is None:
        day = timezone.now()

    without_time = datetime(day.year, day.month, day.day, tzinfo=day.tzinfo)

    return without_time


def end_of_day(day):

    return datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=day.tzinfo)


def end_of_month(day_of_month):

    delta = timedelta(days=1)
    end_day = day_of_month
    last_date = day_of_month + delta

    while last_date.month == end_day.month:
        end_day = end_day + delta
        last_date = last_date + delta

    return end_of_day(end_day)


def today():

    now = timezone.now()
    return start_of_day(now), now


def week():

    now = timezone.now()
    delta = timedelta(days=now.weekday())
    start_of_week = start_of_day(now - delta)

    return start_of_week, now


def month():

    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=pytz.utc)

    return start_of_month, now


def yesterday():

    now = timezone.now()
    delta = timedelta(days=1)
    yesterday = now - delta

    start_of_yesterday = start_of_day(yesterday)
    end_of_yesterday = end_of_day(yesterday)

    return start_of_yesterday, end_of_yesterday


def year():

    now = timezone.now()
    start_of_year = datetime(now.year, 1, 1)

    return start_of_year, now


def month_one():

    now = timezone.now()
    month_one = now.month - 1
    if month_one < 0:
        month_one = 11
        year = now.year - 1
    else:
        year = now.year

    start_of_month = datetime(year, month_one, 1, tzinfo=pytz.utc)

    return start_of_month, end_of_month(start_of_month)


def month_two():

    now = timezone.now()
    month_one = now.month - 2
    if month_one < 0:
        month_one = 11
        year = now.year - 1
    else:
        year = now.year

    start_of_month = datetime(year, month_one, 1, tzinfo=pytz.utc)

    return start_of_month, end_of_month(start_of_month)


def whole(owner):

    first_date = min(it.timestamp for it in Transaction.objects.filter(owner=owner))

    return first_date, timezone.now()

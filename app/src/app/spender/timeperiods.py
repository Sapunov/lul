from django.utils import timezone
from datetime import datetime, timedelta


def start_of_day(day=None):

    if day is None:
        day = timezone.now()

    without_time = datetime(day.year, day.month, day.day, tzinfo=day.tzinfo)

    return without_time


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
    delta = timedelta(days=30)
    start_of_month = start_of_day(now - delta)

    return start_of_month, now


def yesterday():

    start_of_today = start_of_day(timezone.now())
    delta = timedelta(days=1)
    start_of_yesterday = start_of_today - delta

    return start_of_yesterday, start_of_today


def quarter():

    now = timezone.now()
    delta = timedelta(days=90)
    start_of_quarter = start_of_day(now - delta)

    return start_of_quarter, now


def year():

    now = timezone.now()
    delta = timedelta(days=365)
    start_of_year = start_of_day(now - delta)

    return start_of_year, now

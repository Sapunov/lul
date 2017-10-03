import re

from constants import(
    UI, TODAY, YESTERDAY, HOUR, MINUTE, SECOND, HALF_HOUR,
    NUMBER, SPACE, AUGUST, APRIL, DECEMBER, JULY, JUNE, MAY, MARCH,
    NOVEMBER, OCTOBER, SEPTEMBER, FEBRUARY, JANUARY, WEIGHT)


def find_time(string):

    time_word = r"({0}|{1}|{2}|{3})".format(HOUR, MINUTE, SECOND, HALF_HOUR)
    time = r"({0}{1}{2}|{2}{1}{0}|{2})".format(NUMBER, SPACE, time_word)

    result = re.search(time, string, UI)

    if result is not None:
        return result.group()


def find_date(string):

    date_word = "(" + (r"|".join("{{{0}}}".format(i) for i in range(12))).format(
        AUGUST, APRIL, DECEMBER, JULY, JUNE, MAY, MARCH,
        NOVEMBER, OCTOBER, SEPTEMBER, FEBRUARY, JANUARY) + ")"

    date_relative = r"({0}|{1})".format(TODAY, YESTERDAY)

    date = r"({0}{1}{2})|{2}{1}{0}|{3}".format(NUMBER, SPACE, date_word, date_relative)

    result = re.search(date, string, UI)

    if result is not None:
        return result.group()


def find_weight(string):

    weight_result = re.search(WEIGHT, string, UI)

    if not weight_result:
        return None

    number_result = re.search(NUMBER, string)

    if number_result:
        return number_result.group()

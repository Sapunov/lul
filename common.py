import re
import string as string_lib

from nltk.tokenize import word_tokenize


NUMBER = r"([0-9]+)(\.[0-9]+)?"
SPACE = r"[ \n\t]"

HALF_HOUR = r"полчас(а|ам|ами|ах|е|ой|у|ы)?"
HOUR = r"час(а|ам|ами|ах|е|ов|ом|у|ы)?"
MINUTE = r"минут(а|ам|ами|ах|е|ой|у|ы)?"
SECOND = r"секунд(а|ам|ами|ах|е|ой|у|ы)?"

TODAY = r"сегодня"
YESTERDAY = r"вчера"

AUGUST = r"август(а|ам|ами|ах|е|ов|ом|у|ы)?"
APRIL = r"апрел(е|ей|ем|и|ь|ю|я|ям|ями|ях)"
DECEMBER = r"декабр(ь|и|я|ей|ю|ям|ём|ями|е|ях)"
JULY = r"июл(ь|и|я|ей|ю|ям|ем|ями|е|ях)"
JUNE = r"июн(ь|и|я|ей|ю|ям|ем|ями|е|ях)"
MAY = r"ма(й|и|я|ев|ю|ям|ем|ями|е|ях)"
MARCH = r"март(ы|а|ов|у|ам|ом|ами|е|ах)?"
NOVEMBER = r"ноябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)"
OCTOBER = r"октябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)"
SEPTEMBER = r"сентябр(ь|и|я|ей|ю|ям|ём|ями|е|ях)"
FEBRUARY = r"феврал(ь|и|я|ей|ю|ям|ём|ями|е|ях)"
JANUARY = r"январ(ь|и|я|ей|ю|ям|ём|ями|е|ях)"

WEIGHT = r"ве(с|са|сов|су|сам|сом|сами|се|сах|сить|шу)"


def find_time(string):

    time_word = r"({0}|{1}|{2}|{3})".format(HOUR, MINUTE, SECOND, HALF_HOUR)
    time = r"({0}{1}{2}|{2}{1}{0}|{2})".format(NUMBER, SPACE, time_word)

    result = re.search(time, string, re.UNICODE | re.IGNORECASE)

    if result is not None:
        return result.group()


def find_date(string):

    date_word = "(" + (r"|".join("{{{0}}}".format(i) for i in range(12))).format(
        AUGUST, APRIL, DECEMBER, JULY, JUNE, MAY, MARCH,
        NOVEMBER, OCTOBER, SEPTEMBER, FEBRUARY, JANUARY) + ")"

    date_relative = r"({0}|{1})".format(TODAY, YESTERDAY)

    date = r"({0}{1}{2})|{2}{1}{0}|{3}".format(NUMBER, SPACE, date_word, date_relative)

    result = re.search(date, string, re.UNICODE | re.IGNORECASE)

    if result is not None:
        return result.group()


def find_weight(string):

    weight_result = re.search(WEIGHT, string, re.UNICODE | re.IGNORECASE)

    if not weight_result:
        return None

    number_result = re.search(NUMBER, string)

    if number_result:
        return number_result.group()


def replace_datepointer(string, replace_on="DATEPOINTER"):

    pointer = find_date(string)

    if pointer:
        string = string.replace(pointer, replace_on)

    return string


def replace_timepointer(string, replace_on="TIMEPOINTER"):

    pointer = find_time(string)

    if pointer:
        string = string.replace(pointer, replace_on)

    return string


def replace_weightpointer(string, replace_on="WEIGHTPOINTER"):

    weight = find_weight(string)

    # Если нашли именно вес, то ставим указатель
    if weight:
        string = re.sub(WEIGHT, replace_on, string, re.UNICODE | re.IGNORECASE)

        # И удаляем цифру чтобы не смущать классификатор
        string = re.sub(NUMBER, "", string)

    return string


def replace_numbers(string, replace_on="NUM"):

    return re.sub(NUMBER, replace_on, string)


def replace_letterdigits(string):

    tokens = word_tokenize(string)

    for i in range(len(tokens)):
        match = re.match(r"^(([0-9]+)(\.[0-9]+)?)(k|к)$", tokens[i], re.UNICODE)

        if match:
            tokens[i] = str(int(float(match.group(1)) * 1000))

    return " ".join(tokens)


def delete_punctuation(string):

    tokens = word_tokenize(string)

    for token in tokens:
        if token in string_lib.punctuation:
            tokens.remove(token)

    return " ".join(tokens)

import re

from collections import namedtuple

import pickle
import zlib
import os.path

from constants import (SPACE, ANY, NUMBER, LETTER_NUMBER, HOUR, MINUTE,
                       SECOND, HALF_HOUR, HOUR_AND_HALF, TODAY, YESTERDAY,
                       TOMORROW, RUBLES, DOLLARS, EURO, AUGUST, APRIL,
                       DECEMBER, JULY, JUNE, MAY, MARCH, NOVEMBER, OCTOBER,
                       SEPTEMBER, FEBRUARY, JANUARY)


UI = re.UNICODE | re.IGNORECASE

DICTS_DIRECTORY = "dicts"

CACHE = {}

multimatch_result = namedtuple("multimatch_result", ["pos", "value"])

match_result = namedtuple("result", ["pos", "entity"])


def match(pattern, text):

    pattern = r"^{0}$".format(pattern)

    if re.match(pattern, text, UI) is not None:
        return True

    return False


def multi_match(pattern, tokens):

    out = []

    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens) + 1):
            temp = " ".join(tokens[i:j])

            if match(pattern, temp):
                out.append(multimatch_result(pos=(i, j), value=temp))

    # Возвращаем самое длинное совпадение
    if out:
        return sorted(out, key=lambda it: len(it.value), reverse=True)[0]
    else:
        return None


def load_dict(dict_name, suffix=".pickle.gz"):

    if dict_name not in CACHE:
        filename = os.path.join(DICTS_DIRECTORY, dict_name + suffix)

        with open(filename, "rb") as fid:
            CACHE[dict_name] = pickle.loads(zlib.decompress(fid.read()))

    return CACHE[dict_name]


class AnalysisResult:
    """Результат анализа"""

    def __init__(self, text, tokens, result=None):

        self.text = text
        self.tokens = tokens
        self.result = result

        self.result.sort(key=lambda it: it.pos[0])

    def __str__(self):

        return "<AnalysisResult: text={0}; tokens={1}; result={2}>".format(
            self.text, self.tokens, self.result)

    def __repr__(self):

        return self.__str__()


class Number:
    """Число"""

    weight = 1

    def __init__(self, value):

        if "." in value:
            self.value = float(value)
        else:
            self.value = int(value)

    def __str__(self):

        return "<Number: value={0}; weight={1}>".format(self.value, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(NUMBER, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class LetterNumber:
    """Число с буквой. Например, 5к"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._number = self.convert_to_number(value)

    def __str__(self):

        return "<LetterNumber: value={0}; _number={1}; weight={2}>".format(
            self.value, self._number, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def convert_to_number(cls, value):

        num = re.match(NUMBER, value).group(0)

        return int(float(num) * 1000)

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(LETTER_NUMBER, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class Numeral:
    """Числительное"""

    weight = 1

    def __init__(self, value, number):

        self.value = value
        self._number = number

    def __str__(self):

        return "<Numeral: value={0}; _number={1}; weight={2}>".format(
            self.value, self._number, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens, limit=100):

        numerals_dict = load_dict("numerals")

        out = []

        for num in range(limit + 1):
            try:
                item = numerals_dict[num]

                for form in item.values():
                    # Так как у некоторых числительных не определены склонения
                    if form:
                        numeral_match = multi_match(form, tokens)
                    else:
                        continue

                    if numeral_match:
                        out.append(
                            match_result(
                                pos=numeral_match.pos,
                                entity=cls(numeral_match.value, num)
                            )
                        )
                        break
            except KeyError:
                break

        return out


class Hour:
    """Час"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._seconds = 60 * 60

    def __str__(self):

        return "<Hour: value={0}; _seconds={1}; weight={2}>".format(
            self.value, self._seconds, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(HOUR, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class Minute:
    """Минута"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._seconds = 60

    def __str__(self):

        return "<Minute: value={0}; _seconds={1}; weight={2}>".format(
            self.value, self._seconds, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(MINUTE, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class Second:
    """Секунда"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._seconds = 1

    def __str__(self):

        return "<Second: value={0}; _seconds={1}; weight={2}>".format(
            self.value, self._seconds, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(SECOND, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class HalfHour:
    """Полчаса"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._seconds = 60 * 30

    def __str__(self):

        return "<HalfHour: value={0}; _seconds={1}; weight={2}>".format(
            self.value, self._seconds, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(HALF_HOUR, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


class HourAndHalf:
    """Полтора часа"""

    weight = 1

    def __init__(self, value):

        self.value = value
        self._seconds = 60 * 90

    def __str__(self):

        return "<HourAndHalf: value={0}; _seconds={1}; weight={2}>".format(
            self.value, self._seconds, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        match = multi_match(HOUR_AND_HALF, tokens)

        if match:
            out.append(match_result(pos=match.pos, entity=cls(match.value)))

        return out


class Month:
    """Месяц"""

    weight = 1

    POINTERS = (
        (JANUARY, "январь", 0),
        (FEBRUARY, "февраль", 1),
        (MARCH, "март", 2),
        (APRIL, "апрель", 3),
        (MAY, "май", 4),
        (JUNE, "июнь", 5),
        (JULY, "июль", 6),
        (AUGUST, "август", 7),
        (SEPTEMBER, "сентябрь", 8),
        (OCTOBER, "октябрь", 9),
        (NOVEMBER, "ноябрь", 10),
        (DECEMBER, "декабрь", 11)
    )

    def __init__(self, value, month_name, secnum):

        self.value = value
        self._month = month_name
        self._secnum = secnum

    def __str__(self):

        return "<Month: value={0}; _month={1}; _secnum={2}; weight={3}>".format(
            self.value, self._month, self._secnum, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            for month in cls.POINTERS:
                if match(month[0], token):
                    out.append(
                        match_result(
                            pos=(i, i + 1),
                            entity=cls(token, month[1], month[2])
                        )
                    )

        return out


class DatePointer:
    """Указатель на относительную дату"""

    weight = 1

    POINTERS = (
        (YESTERDAY, "вчера", -1),
        (TODAY, "сегодня", 0),
        (TOMORROW, "завтра", 1),
    )

    def __init__(self, value, pointer_name, add):

        self.value = value
        self._pointer = pointer_name
        self._add = add

    def __str__(self):

        return "<DatePointer: value={0}; _pointer={1}; _add={2}; weight={3}>".format(
            self.value, self._pointer, self._add, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            for pointer in cls.POINTERS:
                if match(pointer[0], token):
                    out.append(
                        match_result(
                            pos=(i, i + 1),
                            entity=cls(token, pointer[1], pointer[2])
                        )
                    )

        return out


class Currency:
    """Валюта"""

    weight = 1

    POINTERS = (
        (RUBLES, "rubl"),
        (DOLLARS, "dolr"),
        (EURO, "euro"),
    )

    def __init__(self, value, currency_name):

        self.value = value
        self._name = currency_name

    def __str__(self):

        return "<Currency: value={0}; _name={1}; weight={2}>".format(
            self.value, self._name, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            for pointer in cls.POINTERS:
                if match(pointer[0], token):
                    out.append(
                        match_result(
                            pos=(i, i + 1),
                            entity=cls(token, pointer[1])
                        )
                    )

        return out


class Any:
    """Какая-угодно строка"""

    weight = 0

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return "<Any: value={0}; weight={1}>".format(self.value, self.weight)

    def __repr__(self):

        return self.__str__()

    @classmethod
    def recognize(cls, tokens):

        out = []

        for i, token in enumerate(tokens):
            if match(ANY, token):
                out.append(match_result(pos=(i, i + 1), entity=cls(token)))

        return out


def remove_polysemy(analysis_result):
    """Удаление многозначности из результатов лексического анализа"""

    length = len(analysis_result.tokens)
    results = analysis_result.result

    positions = [None for _ in range(length)]

    for pos in range(length):
        # Нет ли там уже какого-то результата
        if positions[pos] is not None:
            continue

        pos_max_weight = max(
            it.entity.weight for it in results if it.pos[0] == pos)

        items = [it for it in results if (
            it.entity.weight == pos_max_weight and it.pos[0] == pos)]

        if len(items) > 1:
            pos_max_len = max(
                it.pos[1] - it.pos[0] for it in items if it.pos[0] == pos)

            items = [it for it in items if (
                (it.pos[1] - it.pos[0]) == pos_max_len and it.pos[0] == pos)]

        # На данный момент должен остаться лишь один вариант
        item = items[0]

        # Если результат охватывает больше, чем один токен, то нужно застолбить
        # все его позиции. Столбим флагом -1, а после заполнения всех позиций
        # удаляет ячейки с -1
        for i in range(item.pos[0], item.pos[1]):
            if pos == i:
                positions[i] = item
            else:
                positions[i] = -1

    # Удалим пустые ячейки с -1
    positions = [it for it in positions if it != -1]

    return AnalysisResult(analysis_result.text, analysis_result.tokens, positions)


def analyze(text, remove_polysemy_=True):
    """Лексический анализ"""

    tokens = [token for token in text.split(" ") if token != ""]
    results = []

    results.extend(Number.recognize(tokens))
    results.extend(LetterNumber.recognize(tokens))
    results.extend(Hour.recognize(tokens))
    results.extend(Minute.recognize(tokens))
    results.extend(Second.recognize(tokens))
    results.extend(HalfHour.recognize(tokens))
    results.extend(HourAndHalf.recognize(tokens))
    results.extend(Numeral.recognize(tokens))
    results.extend(Month.recognize(tokens))
    results.extend(DatePointer.recognize(tokens))
    results.extend(Currency.recognize(tokens))
    results.extend(Any.recognize(tokens))

    result = AnalysisResult(text, tokens, results)

    if remove_polysemy_:
        return remove_polysemy(result)

    return result

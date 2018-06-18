import re

from .constants import MINUTE, HOUR
from .patterns import (
    P_SPACE, P_NUMBER, P_LETTER_NUMBER,
    P_HOUR, P_MINUTE, P_SECOND,
    P_HALF_HOUR, P_HOUR_AND_HALF, P_RUB,
    P_USD, P_EUR, P_VND,
    P_CNY, P_TAG)


UI = re.UNICODE | re.IGNORECASE


def find_all(patterns, text, flags=0):

    flags |= UI

    for i, pattern in enumerate(patterns):
        if re.search(pattern, text, flags):
            return (i, list(re.finditer(pattern, text, flags)))
    return (-1, [])


def preprocess_number(text):

    text = text.replace(',', '.')
    return text


def str_to_digit(digit_text):

    digit_text = preprocess_number(digit_text)
    return float(digit_text) if '.' in digit_text else int(digit_text)


class BaseEntity:

    def __init__(self, raw, value, position):

        self.raw = raw
        self.value = value

        assert isinstance(position, tuple), \
            '`Position` must be tuple, not {0}'.format(type(position))
        assert len(position) == 2, 'You need to pass 2d tuple as `position`'

        self.span = position
        self.start = position[0]
        self.end = position[1]
        self.size = self.end - self.start

        self.entity_name = self.__class__.__name__

    def __str__(self):

        attrs = self.get_attrs()
        attrs_keys = sorted(attrs.keys())

        return "<{0}: {1}>".format(
            self.entity_name,
            '; '.join('{0}={1}'.format(key, attrs[key]) for key in attrs_keys))

    def __repr__(self):

        return self.__str__()

    def get_attrs(self):

        prohibited = set([
            'start', 'end', 'entity_name',
            'span', 'size', 'raw',
            'value'])
        attrs = self.__dict__.copy()
        for key in list(attrs.keys()):
            if key in prohibited:
                attrs.pop(key)

        return attrs


class NumberEntity(BaseEntity):

    patterns = (P_NUMBER,)

    def __init__(self, raw, value, position):

        value = str_to_digit(value)
        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), res.group(0), res.span()) for res in results]

        return entities


class NumberWithThousandEntity(BaseEntity):

    patterns = (P_LETTER_NUMBER,)

    def __init__(self, raw, value, position):

        value = str_to_digit(value) * 1000
        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), res.group(1), res.span()) for res in results]

        return entities


class CurrencyEntity(BaseEntity):

    _pattern_string = '(({0}|{1})({2})?{3})'
    patterns = (
        _pattern_string.format(P_NUMBER, P_LETTER_NUMBER, P_SPACE, P_RUB),
        _pattern_string.format(P_NUMBER, P_LETTER_NUMBER, P_SPACE, P_USD),
        _pattern_string.format(P_NUMBER, P_LETTER_NUMBER, P_SPACE, P_EUR),
        _pattern_string.format(P_NUMBER, P_LETTER_NUMBER, P_SPACE, P_VND),
        _pattern_string.format(P_NUMBER, P_LETTER_NUMBER, P_SPACE, P_CNY)
    )
    _currencies = [
        'rub',
        'usd',
        'eur',
        'vnd',
        'cny'
    ]

    currency = None

    def __init__(self, raw, amount, pattern_i, position):

        amount = preprocess_number(amount)
        res = re.search(P_LETTER_NUMBER, amount)
        if res:
            amount = str_to_digit(res.group(1)) * 1000
        else:
            amount = str_to_digit(amount)

        self.currency = self._currencies[pattern_i]
        return super().__init__(raw, amount, position)

    @classmethod
    def extract(cls, text):

        pattern_i, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), res.group(2), pattern_i, res.span()) for res in results]

        return entities


class TagEntity(BaseEntity):

    patterns = (P_TAG,)

    def __init__(self, raw, value, position):

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), res.group(2), res.span()) for res in results]

        return entities


class HalfAnHourEntity(BaseEntity):

    patterns = (P_HALF_HOUR,)

    def __init__(self, raw, value, position):

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), 30 * MINUTE, res.span()) for res in results]

        return entities


class HourAndAHalfEntity(BaseEntity):

    patterns = (P_HOUR_AND_HALF,)

    def __init__(self, raw, value, position):

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), 90 * MINUTE, res.span()) for res in results]

        return entities


class OneHourEntity(BaseEntity):

    patterns = ('час',)

    def __init__(self, raw, value, position):

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), 60 * MINUTE, res.span()) for res in results]

        return entities


class HoursEntity(BaseEntity):

    patterns = (
        '({digit}){space}с половиной{space}{hour}'.format(
            digit=P_NUMBER, space=P_SPACE, hour=P_HOUR),
        '({digit}){space}{hour}'.format(digit=P_NUMBER, space=P_SPACE, hour=P_HOUR)
    )

    def __init__(self, raw, hours, minutes, position):

        hours = str_to_digit(hours)
        value = hours * HOUR + minutes * MINUTE

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        pattern_i, results = find_all(cls.patterns, text)
        if pattern_i == 0:
            entities = [cls(res.group(0), res.group(1), 30, res.span()) for res in results]
        else:
            entities = [cls(res.group(0), res.group(1), 0, res.span()) for res in results]

        return entities


class MinutesEntity(BaseEntity):

    patterns = (
        '({digit}){space}{minute}'.format(
            digit=P_NUMBER, space=P_SPACE, minute=P_MINUTE),
    )

    def __init__(self, raw, minutes, position):

        minutes = str_to_digit(minutes)
        value = minutes * MINUTE

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        _, results = find_all(cls.patterns, text)
        entities = [cls(res.group(0), res.group(1), res.span()) for res in results]

        return entities


class HoursMinutesEntity(BaseEntity):

    patterns = (
        '({digit}){space}{hour}{space}(и{space})?({digit}){space}{minute}'.format(
            digit=P_NUMBER, space=P_SPACE, minute=P_MINUTE, hour=P_HOUR),
        '({digit}){space}{hour}{space}({digit})'.format(
            digit=P_NUMBER, space=P_SPACE, hour=P_HOUR),
        'час{space}(и{space})?({digit})({space}{minute})?'.format(
            space=P_SPACE, digit=P_NUMBER, minute=P_MINUTE)
    )

    def __init__(self, raw, hours, minutes, position):

        hours = str_to_digit(hours)
        minutes = str_to_digit(minutes)

        value = hours * HOUR + minutes * MINUTE

        return super().__init__(raw, value, position)

    @classmethod
    def extract(cls, text):

        pattern_i, results = find_all(cls.patterns, text)
        if pattern_i == 0:
            entities = [cls(res.group(0), res.group(1), res.group(7), res.span()) for res in results]
        elif pattern_i == 1:
            entities = [cls(res.group(0), res.group(1), res.group(6), res.span()) for res in results]
        else:
            entities = [cls(res.group(0), '1', res.group(2), res.span()) for res in results]

        return entities

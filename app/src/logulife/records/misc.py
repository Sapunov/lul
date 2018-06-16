import pytz

from django.utils import timezone


def local_to_utc(datetime):

    if timezone.is_naive(datetime):
        raise ValueError('Passed datetime has no timezone info')

    return datetime.astimezone(pytz.utc)


def is_true(text):

    true_marks = ('1', 1, True, 'true', 'yes')

    return text.lower() in true_marks

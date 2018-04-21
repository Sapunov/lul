import pytz

from django.utils import timezone


def local_to_utc(datetime):

    if timezone.is_naive(datetime):
        raise ValueError('Passed datetime has no timezone info')

    return datetime.astimezone(pytz.utc)


def deserialize(serializer_class, data, **kwargs):

    serializer = serializer_class(data=data, **kwargs)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize(serializer_class, instance, data=None, **kwargs):

    if data is None:
        serializer = serializer_class(instance, **kwargs)
    else:
        serializer = serializer_class(instance, data=data, **kwargs)
        serializer.is_valid(raise_exception=True)

    return serializer

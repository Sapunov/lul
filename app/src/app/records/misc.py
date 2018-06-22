from importlib import import_module
import pytz

from django.utils import timezone


def local_to_utc(datetime):

    if timezone.is_naive(datetime):
        raise ValueError('Passed datetime has no timezone info')

    return datetime.astimezone(pytz.utc)


def is_true(text):

    true_marks = ('1', 1, True, 'true', 'yes')

    return text.lower() in true_marks


def import_module_attr(path_to_attr):

    module_name, attr_name = path_to_attr.rsplit('.', 1)

    module = import_module(module_name)

    try:
        attr = getattr(module, attr_name)
    except AttributeError:
        raise ImportError('No attribute <%s> in %s' % (attr_name, module))

    return attr

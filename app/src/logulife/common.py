import logging

from django.conf import settings


def get_logger(name):

    return logging.getLogger(settings.APP_GROUP_NAME + '.' + name)


def expand_context_for_logging(context):

    return {
        'view_name': context['view'].get_view_name(),
        'absolute_uri': context['request'].build_absolute_uri(),
        'http_method': context['request'].method,
        'user': context['request'].user
    }

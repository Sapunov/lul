from rest_framework import status
from rest_framework.views import exception_handler

from app.common import get_logger, expand_context_for_logging


log = get_logger(__name__)


def error_format(error_code, error_msg):

    return {
        'error': {
            'error_code': error_code,
            'error_msg': error_msg
        }
    }


def api_exception_handler(exception, context):

    log.debug('APIError: %s. Context: %s',
        exception, expand_context_for_logging(context))

    response = exception_handler(exception, context)

    if not response is None and isinstance(response.data, dict):
        response.data = error_format(response.status_code, response.data)

    return response

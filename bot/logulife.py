import logging
import requests

import settings
import common


log = common.mini_log(__name__)

HEADERS = {
    'Authorization': 'Token {0}'.format(settings.LOGULIFE['token'])
}

TIMEOUT = 10

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'


def _post_data(path, data):

    req = requests.post(
        '{0}/{1}'.format(settings.LOGULIFE['host'], path),
        json=data,
        headers=HEADERS,
        timeout=TIMEOUT)

    return req


def _put_data(path, data):

    req = requests.put(
        '{0}/{1}'.format(settings.LOGULIFE['host'], path),
        json=data,
        headers=HEADERS,
        timeout=TIMEOUT)

    return req


def make_record(text, message_id, timestamp=None):

    data = {
        'text': text,
        'source_record_id': message_id,
        'source_name': settings.SOURCE_NAME
    }

    if not timestamp is None:
        data['timestamp'] = timestamp.strftime(DATETIME_FORMAT)

    log.debug('Trying to create record with data: %s', data)

    try:
        ans = _post_data('api/records', data)
    except requests.exceptions.RequestException as exc:
        logging.exception(exc)
        return -1

    if ans.status_code == 200:
        return 0
    else:
        return ans.status_code


def update_record(new_text, message_id):

    data = {
        'text': new_text,
        'source_record_id': message_id,
        'source_name': settings.SOURCE_NAME
    }

    log.debug('Trying to update record with data: %s', data)

    try:
        ans = _put_data('api/records', data)
    except requests.exceptions.RequestException as exc:
        logging.exception(exc)
        return -1

    if ans.status_code == 200:
        return 0
    else:
        return ans.status_code

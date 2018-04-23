from datetime import datetime
import requests

from logulife import exceptions
from logulife import misc


DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'


class LogulifeClient:

    def __init__(self, hostname, token=None, timeout=10):

        self.hostname = hostname.rstrip('/')
        self.token = token
        self.timeout = timeout

    def get_access_token(self, username, password):

        req = self._post(
            '/api/tokens',
            data={
                'username': username,
                'password': password
            },
            headers={})

        if req.status_code == requests.codes['ok']:
            self.token = req.json()['token']
            return self.token

        raise exceptions.LogulifeException(req.text)

    def make_record(self, source_name, message_id, text, timestamp=None):

        data = {
            'text': text,
            'source_record_id': message_id,
            'source_name': source_name
        }

        if timestamp is not None:
            assert isinstance(timestamp, datetime), 'Timestamp must be of type `datetime`'

            data['timestamp'] = timestamp.strftime(DATETIME_FORMAT)

        req = self._post(
            '/api/records',
            data=data
        )

        if req.status_code == requests.codes['ok']:
            record = req.json()
            return record

        raise exceptions.LogulifeException(req.text)

    def update_record(self, source_name, message_id, text):

        data = {
            'text': text,
            'source_record_id': message_id,
            'source_name': source_name
        }

        req = self._put(
            '/api/records',
            data=data
        )

        if req.status_code == requests.codes['ok']:
            record = req.json()
            return record

        if req.status_code == requests.codes['not_found']:
            raise exceptions.NotFoundException(req.text)

        raise exceptions.LogulifeException(req.text)

    def _post(self, url, data=None, headers=None):

        full_url = self.hostname + '/' + url.lstrip('/')

        if data is None:
            data = {}

        if headers is None:
            headers = self._get_default_headers()

        req = requests.post(
            full_url,
            json=data,
            headers=headers,
            timeout=self.timeout)

        return req

    def _put(self, url, data=None, headers=None):

        full_url = self.hostname + '/' + url.lstrip('/')

        if data is None:
            data = {}

        if headers is None:
            headers = self._get_default_headers()

        req = requests.put(
            full_url,
            json=data,
            headers=headers,
            timeout=self.timeout)

        return req

    def _get_default_headers(self):

        assert self.token is not None, 'Auth first please'

        return {
            'Authorization': 'Token {0}'.format(self.token)
        }

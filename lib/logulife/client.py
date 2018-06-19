from datetime import datetime
import requests

from logulife import exceptions
from logulife import misc
from logulife import settings

from logulife.records import RecordsHandler


class LogulifeClient:

    def __init__(
            self,
            token=None,
            username=None,
            password=None,
            apps=None
    ):

        self.apps_hostname = {}
        self.handlers = {
            'records': {
                'instance': None,
                'class': RecordsHandler
            }
        }

        if isinstance(apps, dict):
            self.apps_hostname.update(apps)

        if token:
            self.token = token
        elif username and password:
            self._auth_with_credentials(username, password)
        else:
            raise exceptions.NoCredentialsProvidedException()

    def __getattr__(self, name):

        if name in self.handlers:
            if self.handlers[name]['instance'] is None:
                self.handlers[name]['instance'] = \
                    self.handlers[name]['class'](self)
            return self.handlers[name]['instance']

        raise exceptions.LogulifeException('Method {0} is absent'.format(name))

    def get(self, url, params=None, headers=None):

        url = self._resolve_url(url)

        if headers is None:
            headers = self._get_auth_header()

        try:
            resp = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkException(
                'Error while making GET request to {0}: {1}'.format(url, exc), exc)

        return resp

    def post(self, url, json_data=None, headers=None):

        url = self._resolve_url(url)

        if json_data is None:
            json_data = {}

        if headers is None:
            headers = self._get_auth_header()

        try:
            resp = requests.post(
                url,
                json=json_data,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkException(
                'Error while making POST request to {0}: {1}'.format(url, exc), exc)

        return resp

    def put(self, url, json_data=None, headers=None):

        url = self._resolve_url(url)

        if json_data is None:
            json_data = {}

        if headers is None:
            headers = self._get_auth_header()

        try:
            resp = requests.put(
                url,
                json=json_data,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkException(
                'Error while making PUT request to {0}: {1}'.format(url, exc), exc)

        return resp

    def delete(self, url, headers=None):

        url = self._resolve_url(url)

        if headers is None:
            headers = self._get_auth_header()

        try:
            resp = requests.delete(
                url,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkException(
                'Error while making DELETE request to {0}: {1}'.format(url, exc), exc)

        return resp

    def _auth_with_credentials(self, username, password):

        resp = self.post(
            'app:/api/tokens',
            json_data={
                'username': username,
                'password': password
            },
            headers={})

        if resp.status_code == requests.codes['ok']:
            self.token = resp.json()['token']
            return self.token
        elif resp.status_code == requests.codes['400']:
            raise exceptions.WrongCredentialsException()
        else:
            raise exceptions.LogulifeException(resp.text)

    def _split_app_url(self, url):

        try:
            first_colon = url.index(':')
        except ValueError:
            raise exceptions.BadUrlException()

        app_name = url[:first_colon]
        target_url = url[first_colon + 1:]

        return app_name, target_url

    def _resolve_url(self, app_url):

        app, url = self._split_app_url(app_url)

        if app not in self.apps_hostname:
            try:
                self.apps_hostname[app] = settings.conf_param(
                    'services.' + app + '.hostname').rstrip('/')
            except exceptions.BadConfigPath:
                raise exceptions.LogulifeException(
                    'No configuration for service: {0}'.format(app))

        return self.apps_hostname[app] + '/' + url.lstrip('/')

    def _get_auth_header(self):

        return {
            'Authorization': 'Token {0}'.format(self.token)
        }

    def __str__(self):

        return '<LogulifeClient>'

    def __repr__(self):

        return self.__str__()

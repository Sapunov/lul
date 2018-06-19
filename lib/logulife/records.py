from logulife import exceptions
from logulife.base import BaseHandler


class RecordsHandler(BaseHandler):

    def create(self, text, source=None, ext_id=None, timestamp=None, label=None):

        pass

    def update(self, record_id, text):

        pass

    def update_by_ext_id(self, source, ext_id, text):

        return self.update('{0}_{1}'.format(source, ext_id), text)

    def delete(self, record_id):

        return self._client.delete(
            'app:api/records/{0}'.format(record_id)).json()

    def delete_by_ext_id(self, source, ext_id):

        return self.delete('{0}_{1}'.format(source, ext_id))

    def get(self, record_id):

        return self._client.get('app:api/records/{0}'.format(record_id)).json()

    def filter(self, q=None):

        params = {}

        if q is not None:
            params.update({'q': q})

        return self._client.get('app:/api/records', params=params).json()

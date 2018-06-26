from datetime import datetime

from logulife import exceptions
from logulife.base import BaseHandler


class RecordsHandler(BaseHandler):

    def create(self, text, source=None, ext_id=None, timestamp=None, label=None):

        user_data = {
            'text': text
        }

        if source is not None:
            user_data['source'] = source
            assert ext_id is not None, \
                'Specify ext_id if you are specifying source'
            user_data['ext_id'] = ext_id

        if timestamp is not None:
            assert isinstance(timestamp, datetime), \
                'Timestamp must be of type datetime'
            user_data['timestamp'] = timestamp.isoformat()

        if label is not None:
            user_data['label'] = label

        return self._client.post('app:api/records', json_data=user_data)

    def update(self, record_id, text):

        user_data = {
            'text': text
        }

        return self._client.put(
            'app:api/records/{0}'.format(record_id), json_data=user_data)

    def update_by_ext_id(self, source, ext_id, text):

        return self.update('{0}_{1}'.format(source, ext_id), text)

    def delete(self, record_id):

        return self._client.delete(
            'app:api/records/{0}'.format(record_id))

    def delete_by_ext_id(self, source, ext_id):

        return self.delete('{0}_{1}'.format(source, ext_id))

    def get(self, record_id):

        return self._client.get('app:api/records/{0}'.format(record_id))

    def filter(self, q=None, limit=10, offset=0):

        params = {
            'limit': limit,
            'offset': offset
        }

        if q is not None:
            params.update({'q': q})

        return self._client.get('app:/api/records', params=params)

    def set_label(self, record_id, label):

        data = {
            'label': label
        }

        return self._client.post(
            'app:api/records/{0}/label'.format(record_id), json_data=data)


    def set_label_by_ext_id(self, source, ext_id, label):

        return self.set_label('{0}_{1}'.format(source, ext_id), label)

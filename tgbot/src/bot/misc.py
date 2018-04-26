import settings
import json
import os

import common


log = common.mini_log(__name__)


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


def save_json(filename, data):

    if not isinstance(filename, str):
        filename = str(filename)

    full_path = os.path.join(settings.DATA_DIR, filename)

    log.debug('Path for saving json: %s', full_path)

    uniq_counter = 0
    while os.path.exists(full_path):
        full_path += '_{0}'.format(uniq_counter)
        uniq_counter += 1

    with open(full_path, 'w') as fid:
        json.dump(data, fid)

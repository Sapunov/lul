import os
import json

from logulife import exceptions


APP_GROUP_NAME = 'logulife'

APP_NAME = 'lib'

VERSION = '0.0.2'

ETC = '/etc'

VAR = '/var'

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, APP_GROUP_NAME)

CONFIG_DIR = os.path.join(ETC, APP_GROUP_NAME)

DEPLOY_CONFIG = os.path.join(
    CONFIG_DIR, '{0}.deploy.json'.format(APP_GROUP_NAME))

CONFIG = {

}

if os.path.exists(DEPLOY_CONFIG):
    with open(DEPLOY_CONFIG) as opened:
        try:
            data = json.load(opened)
            CONFIG.update(data)
        except Exception as exc:
            print('Error while parsing config file: %s' % exc)


def conf_param(path_to_param):

    path = path_to_param.split('.')
    current_state = CONFIG

    for current_param in path:
        if current_param in current_state:
            current_state = current_state[current_param]
        else:
            raise exceptions.BadConfigPath(
                'Bad config path: {0}'.format(path_to_param))

    return current_state


REQUEST_TIMEOUT = 10

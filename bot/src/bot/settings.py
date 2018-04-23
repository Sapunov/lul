import json
import logging
import os
import re


PROGRAM_NAME = 'logulife_bot'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TELEGRAM_TOKEN = None

USERS = None

with open(os.path.join(BASE_DIR, 'tokens.json')) as fid:
    data = json.load(fid)
    TELEGRAM_TOKEN = data['telegram']
    USERS = data['users']

assert 'LOGULIFE_HOST' in os.environ, 'Specify logulife host in env, please'

LOGULIFE_HOST = os.environ.get('LOGULIFE_HOST')

SOURCE_NAME = 'telegram'

BASE_LOGLEVEL = logging.DEBUG

VAR = '/var'

VAR_LOG = os.path.join(VAR, 'log')

VAR_LIB = os.path.join(VAR, 'lib')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)

PROGRAM_DIR = os.path.join(VAR_LIB, PROGRAM_NAME)

DATA_DIR = os.path.join(PROGRAM_DIR, 'data')

USE_PROXY = True

PROXY_HOST = 'socks5://heirh.tgproxy.me:1080'

PROXY_USERNAME = 'telegram'

PROXY_PASSWORD = 'telegram'

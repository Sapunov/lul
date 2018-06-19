import json
import logging
import os
import re


APP_GROUP_NAME = 'logulife'

APP_NAME = 'tgbot'

VERSION = '0.0.1'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TELEGRAM_TOKEN = None

USERS = None

ADMIN_ACCOUNT = None

with open(os.path.join(BASE_DIR, 'tokens.json')) as fid:
    data = json.load(fid)
    TELEGRAM_TOKEN = data['telegram']
    USERS = data['users']
    ADMIN_ACCOUNT = data['admin']

SOURCE_NAME = 'telegram'

BASE_LOGLEVEL = logging.DEBUG

VAR = '/var'

VAR_LOG = os.path.join(VAR, 'log')

VAR_LIB = os.path.join(VAR, 'lib')

LOGS_DIR = os.path.join(VAR_LOG, APP_GROUP_NAME)

PROGRAM_DIR = os.path.join(VAR_LIB, APP_GROUP_NAME)

DATA_DIR = os.path.join(PROGRAM_DIR, 'data')

USE_PROXY = True

PROXY_HOST = 'socks5://heirh.tgproxy.me:1080'

PROXY_USERNAME = ''

PROXY_PASSWORD = ''

import json
import logging
import re


PROGRAM_NAME = 'logulife'

TELEGRAM_TOKEN = None
LOGULIFE_TOKEN = None


with open('TOKENS') as fid:
    data = json.load(fid)
    TELEGRAM_TOKEN = data['telegram']
    LOGULIFE_TOKEN = data['logulife']


LOGULIFE = {
    'host': 'http://localhost:8000',
    'token': LOGULIFE_TOKEN
}

SOURCE_NAME = 'telegram'

BASE_LOGLEVEL = logging.DEBUG

CONFIRM_CHOICE_OPTION_REXP = re.compile(r'^(да|нет)$', re.IGNORECASE)

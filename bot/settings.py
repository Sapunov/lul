import json


TELEGRAM_TOKEN = None
LOGULIFE_TOKEN = None

with open('TOKENS') as fid:
    data = json.load(fid)
    TELEGRAM_TOKEN = data['telegram']
    LOGULIFE_TOKEN = data['logulife']


SOURCE_NAME = 'telegram'

LOGULIFE = {
    'host': 'http://localhost:8000',
    'token': LOGULIFE_TOKEN
}

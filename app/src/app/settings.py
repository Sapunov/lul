import json
import os


APP_GROUP_NAME = 'logulife'

APP_NAME = 'app'

VERSION = '0.0.5'

ETC = '/etc'

VAR = '/var'

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, APP_GROUP_NAME)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

#
# Загрузка соответствующей конфигурации
#
config_file = os.path.join(ETC, APP_GROUP_NAME, APP_NAME + '.conf.json')

assert os.path.exists(config_file), 'No config file at %s' % config_file

with open(config_file) as config_open:
    temp_data = json.load(config_open)
    if DEBUG:
        CONF = temp_data['dev']
    else:
        CONF = temp_data['prod']

SECRET_KEY = CONF['django_key']

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'app.records',
    'app.spender',
    'app.web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.ExceptionsHandlingMiddleware'
]

ROOT_URLCONF = 'app.urls'

APPEND_SLASH = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': CONF['database']['name'],
        'HOST': CONF['database']['host'],
        'PORT': CONF['database']['port'],
        'USER': CONF['database']['user'],
        'PASSWORD': CONF['database']['password']
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'EXCEPTION_HANDLER': 'app.rest.api_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

ADMIN_ENABLED = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(filename)s:'
                      '%(funcName)s:%(lineno)s '
                      '%(levelname)s: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'logulife': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, APP_NAME + '.log'),
            'formatter': 'verbose'
        },
        'logulife_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, APP_NAME + '.error.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'logulife': {
            'handlers': ['logulife', 'logulife_error'],
            'level': 'DEBUG',
            'propagate': True
        }
    },
}

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

DEFAULT_SOURCE_NAME = 'native'

ALLOWED_LABELS = ('expence', 'income', 'time', 'other')

DEFAULT_CURRENCY = 'rub'

LABEL_CLASSIFICATION_THRESHOLD = 0.9

SAVED_PREDICTION_RESULTS = 3

RECORDS_LISTENERS = {
    'spender': {
        'create': 'app.spender.views.record_create',
        'update': 'app.spender.views.record_update',
        'delete': 'app.spender.views.record_delete'
    }
}

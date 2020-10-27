import json
import logging.config
import os
import sys

from decouple import config

DATA = {}
file_path_prod = '/etc/app/configuration/configuration.json'
if os.path.isfile(file_path_prod):
    with open(file_path_prod, encoding='utf-8') as json_data:
        DATA = json.load(json_data, strict=False)


class Production(object):
    APP_PORT = config('APP_PORT', default=DATA.get('APP_PORT', 8081), cast=int)
    APP_DEBUG = config('APP_DEBUG', default=DATA.get('APP_DEBUG', False), cast=bool)
    SQL_USER = config('SQL_USER', default=DATA.get('SQL_USER', 'usr_dev'), cast=str)
    SQL_PWD = config('SQL_PWD', default=DATA.get('SQL_PWD', '123456'), cast=str)
    SQL_HOST = config('SQL_HOST', default=DATA.get('SQL_HOST', 'localhost'), cast=str)
    SQL_DB = config('SQL_DB', default=DATA.get('SQL_DB', 'gaivota'), cast=str)
    SQL_PORT = config('SQL_PORT', default=DATA.get('SQL_PORT', 'usr_dev'), cast=str)
    SQL_POOL_SIZE = config('SQL_POOL_SIZE', default=DATA.get('SQL_POOL_SIZE', 10), cast=int)
    SQL_SCHEMA = config('SQL_SCHEMA', default=DATA.get('SQL_SCHEMA', 10), cast=str)
    APP_VERSION = config('APP_VERSION', default=DATA.get('APP_VERSION', '1.0.0'), cast=str)
    APP_TITLE = config('APP_TITLE', default=DATA.get('APP_TITLE', '1.0.0'), cast=str)
    PAGE_SIZE = config('PAGE_SIZE', default=DATA.get('PAGE_SIZE', 20), cast=int)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%s'
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            'dev_null': {
                'class': 'logging.NullHandler'
            }
        },
        "loggers": {
            '': {
                "handlers": ["console"],
                'propagate': True,
                'level': 'INFO',
            }
        }
    }


class Developer(Production):
    API_ENVIRONMENT = 'DEV'


class Staging(Production):
    API_ENVIRONMENT = 'HMG'


class Local(Production):
    API_ENVIRONMENT = 'LOCAL'


def _load_config():
    environment = DATA.get('ENVIRONMENT', config('ENVIRONMENT', 'Local'))
    _config_class = getattr(sys.modules[__name__], str(environment))
    return _config_class()


config = _load_config()
logging.config.dictConfig(config.LOGGING)

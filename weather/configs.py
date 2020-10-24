import json
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

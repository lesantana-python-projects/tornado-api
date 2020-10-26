import tornado
from tornado.web import Application
from tornado_swagger.setup import setup_swagger

from weather.configs import config
from weather.urls import routes


class ApiApplication(tornado.web.Application):

    def __init__(self):
        settings = {
            'debug': config.APP_DEBUG
        }

        setup_swagger(routes,
                      swagger_url='/doc',
                      api_base_url='/',
                      description='',
                      api_version=config.APP_VERSION,
                      title=config.APP_TITLE,
                      schemes=['http']
                      )
        super(ApiApplication, self).__init__(routes, **settings)

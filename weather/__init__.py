from tornado.web import Application
from tornado_swagger.setup import setup_swagger

from weather.configs import config
from weather.urls import routes


class ApiApplication(Application):

    def __init__(self):
        settings = {
            'debug': config.APP_DEBUG
        }

        setup_swagger(routes,
                      swagger_url='/doc',
                      description='Api to available knowledge with python and tornado',
                      api_version=config.APP_VERSION,
                      title=config.APP_TITLE)

        super(ApiApplication, self).__init__(routes, **settings)

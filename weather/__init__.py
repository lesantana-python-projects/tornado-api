from tornado.web import Application

from weather.ulrs import routes


def create_app():
    app = Application(routes)
    return app

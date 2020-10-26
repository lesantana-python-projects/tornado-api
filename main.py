import multiprocessing
import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from weather import ApiApplication
from weather.configs import config

if __name__ == '__main__':
    app = ApiApplication()

    server = HTTPServer(app)
    port = int(os.getenv('PORT', config.APP_PORT))
    server.bind(port)
    server.start(multiprocessing.cpu_count() if not config.APP_DEBUG else 1)
    IOLoop.instance().start()
    app.listen(port)
    IOLoop.current().start()

import logging

from tornado.web import RequestHandler

logger = logging.getLogger(__name__)


class ApiJsonHandler(RequestHandler):
    @staticmethod
    def __response_message(status, response='success'):
        return {'result': response, 'status': status}

    def initialize(self):
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        message = kwargs["exc_info"][1]
        logger.error(message)
        if status_code not in range(400, 500):
            message = 'Internal Server Error'
        self.error(message=str(message), code=status_code)

    def success(self, code=200, message='OK', status='success'):
        self.set_status(code)
        self.finish(self.__response_message(status=status, response=message))

    def error(self, message, code=500, status='error'):
        self.set_status(code)
        logger.error(message)
        self.finish(self.__response_message(status=status, response=message))

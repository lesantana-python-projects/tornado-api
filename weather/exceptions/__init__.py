from http import HTTPStatus


class GenericError(Exception):
    code = 500
    message = 'Internal Server Error'

    def __init__(self, message=None):
        if message:
            self.message = message


class CustomDatabaseError(GenericError):
    def __init__(self, message, code=HTTPStatus.BAD_REQUEST.value):
        super(CustomDatabaseError, self).__init__(message)
        self.code = code
        self.message = message


KNOWN_ERRORS = (CustomDatabaseError,)

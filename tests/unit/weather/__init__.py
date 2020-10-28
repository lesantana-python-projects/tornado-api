import unittest

from tornado.testing import AsyncHTTPTestCase
import mock

from weather import ApiApplication


class BaseAsyncAwait:
    @staticmethod
    def mock_await():
        async def async_magic():
            pass

        mock.MagicMock.__await__ = lambda x: async_magic().__await__()


class BaseAsyncHttpTestCase(AsyncHTTPTestCase, BaseAsyncAwait):
    def get_app(self):
        return ApiApplication()

    def setUp(self):
        self.mock_await()
        super().setUp()

    def tearDown(self):
        super().tearDown()


class BaseTests(unittest.TestCase):
    def setUp(self):
        super().setUp()


class MixinTest(object):
    class Instance(object):
        @staticmethod
        async def agreement(request=None):
            return mock.MagicMock()

        @staticmethod
        async def process(params=None):
            return {
                "result": {
                    "resultsCount": 3,
                    "next_page": 2,
                    "previous_page": None,
                    "data": [
                        {
                            "id": 59999,
                            "name_station": "ALTO PARNAIBA",
                            "latitude": "-9.1",
                            "longitude": "-45.9333"
                        }
                    ]
                },
                "status": "success"
            }

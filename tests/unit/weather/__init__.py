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
        async def process(params=None, method=None):
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

    class InstanceEdit(object):
        def __init__(self, mock_result=None):
            self.mock_result = mock_result

        @staticmethod
        async def agreement(request=None, **kwargs):
            return mock.MagicMock()

        async def process(self, params=None, method=None, **kwargs):
            response = self.mock_result
            if not response:
                response = {
                    "result": {
                        "id": 59999,
                        "name_station": "ALTO PARNAIBA",
                        "latitude": "-9.1",
                        "longitude": "-45.9333"
                    },
                    "status": "success"
                }
            return response

    class InstanceWeatherDataEdit(object):
        def __init__(self, mock_result=None):
            self.mock_result = mock_result

        @staticmethod
        async def agreement(request=None, **kwargs):
            return mock.MagicMock()

        async def process(self, params=None, method=None, **kwargs):
            response = self.mock_result
            if not response:
                response = {
                    "result": {
                        "id": 20,
                        "date": "1976-09-07",
                        "hour": "12",
                        "precipitation": None,
                        "dry_bulb_temperature": 29.9,
                        "high_temperature": None,
                        "low_temperature": 16.3,
                        "relative_humidity": 47,
                        "relative_humidity_avg": None,
                        "pressure": 979.8,
                        "sea_pressure": None,
                        "wind_direction": 32,
                        "wind_speed_avg": None,
                        "cloud_cover": None,
                        "evaporation": 7,
                        "name_station": "ALTO PARNAIBA"
                    },
                    "status": "success"
                }
            return response

import mock
from sqlalchemy.exc import IntegrityError
from tornado.concurrent import Future
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test
from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration.weather_detail import WeatherDetail
from weather.models.model_base import ModelBase


@mock.patch('weather.integration.weather_detail.logger', mock.MagicMock())
class TestWeatherDetail(BaseAsyncHttpTestCase):
    def setUp(self):
        super(TestWeatherDetail, self).setUp()
        self.weather_detail = WeatherDetail()
        self.mock_response = {
            "result": {
                "resultsCount": 1,
                "next_page": None,
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

    @gen_test
    async def test_process(self):
        future_1 = Future()
        future_1.set_result(self.mock_response)
        self.weather_detail._run_process = mock.MagicMock(return_value=future_1)
        response = await self.weather_detail.process(params={})
        self.assertEqual(response, self.mock_response)

    @gen_test
    async def test_result_mount(self):
        response = await self.weather_detail.result_mount(mock.MagicMock())
        self.assertIsNotNone(response.get('id'))
        self.assertIsNotNone(response.get('name_station'))
        self.assertIsNotNone(response.get('latitude'))
        self.assertIsNotNone(response.get('longitude'))

    @mock.patch('weather.integration.weather_detail.Weather')
    @mock.patch('weather.integration.weather_detail.paginate')
    @gen_test
    async def test_query_mount_success(self, mock_paginate, mock_weather):
        await self.weather_detail.query_mount('name_station', 'a', 0, 1)
        self.assertTrue(mock_paginate.called)
        self.assertTrue(mock_weather.called)

    @mock.patch('weather.integration.weather_detail.Weather')
    @mock.patch('weather.integration.weather_detail.paginate')
    @mock.patch('weather.integration.weather_detail.default_exception_error')
    @gen_test
    async def test_query_mount_error(self, mock_default_exception_error, mock_paginate, mock_weather):
        mock_weather().KNOWN_ERROR_SQLALCHEMY = ModelBase().KNOWN_ERROR_SQLALCHEMY
        mock_paginate.side_effect = IntegrityError('mock', 'mock', 'mock')

        await self.weather_detail.query_mount('name_station', 'a', 0, 1)

        self.assertTrue(mock_paginate.called)
        self.assertTrue(mock_weather.called)
        self.assertTrue(mock_default_exception_error.called)

    @mock.patch('weather.integration.weather_detail.Weather')
    @gen_test
    async def test_query_mount_exception(self, mock_weather):
        with self.assertRaises(HTTPClientError) as context:
            await self.weather_detail.query_mount('unknown_name', 'a', 0, 1)
        self.assertTrue(mock_weather.called)
        self.assertTrue('not found in model Weather' in str(context.exception))

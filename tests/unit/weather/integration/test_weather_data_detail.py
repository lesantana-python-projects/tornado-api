import mock
from tornado.concurrent import Future
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test
from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration.weather_data_detail import WeatherDataDetail


@mock.patch('weather.integration.weather_data_detail.logger', mock.MagicMock())
class TestWeatherDataDetail(BaseAsyncHttpTestCase):
    def setUp(self):
        super(TestWeatherDataDetail, self).setUp()
        self.weather_data_detail = WeatherDataDetail()
        self.mock_response = {
            "result": {
                "resultsCount": 1,
                "next_page": None,
                "previous_page": None,
                "data": [
                    {
                        "id": 1,
                        "date": "1976-09-01",
                        "hour": "0",
                        "precipitation": None,
                        "dry_bulb_temperature": None,
                        "high_temperature": 34.1,
                        "low_temperature": None,
                        "relative_humidity": None,
                        "relative_humidity_avg": 23.12,
                        "pressure": None,
                        "sea_pressure": None,
                        "wind_direction": None,
                        "wind_speed_avg": 52,
                        "cloud_cover": 10,
                        "evaporation": None,
                        "name_station": "ALTO PARNAIBA"
                    }
                ]
            },
            "status": "success"
        }

    @gen_test
    async def test_process(self):
        future_1 = Future()
        future_1.set_result(self.mock_response)
        self.weather_data_detail._run_process = mock.MagicMock(return_value=future_1)
        response = await self.weather_data_detail.process(params={})
        self.assertEqual(response, self.mock_response)

    @gen_test
    async def test_result_mount(self):
        response = await self.weather_data_detail.result_mount(mock.MagicMock())
        self.assertIsNotNone(response.get('id'))
        self.assertIsNotNone(response.get('date'))
        self.assertIsNotNone(response.get('hour'))
        self.assertIsNotNone(response.get('precipitation'))
        self.assertIsNotNone(response.get('dry_bulb_temperature'))
        self.assertIsNotNone(response.get('high_temperature'))
        self.assertIsNotNone(response.get('low_temperature'))
        self.assertIsNotNone(response.get('relative_humidity'))
        self.assertIsNotNone(response.get('pressure'))
        self.assertIsNotNone(response.get('sea_pressure'))
        self.assertIsNotNone(response.get('wind_direction'))
        self.assertIsNotNone(response.get('wind_speed_avg'))
        self.assertIsNotNone(response.get('cloud_cover'))
        self.assertIsNotNone(response.get('evaporation'))
        self.assertIsNotNone(response.get('name_station'))

    @mock.patch('weather.integration.weather_data_detail.WeatherData')
    @mock.patch('weather.integration.weather_data_detail.paginate')
    @gen_test
    async def test_query_mount_success(self, mock_paginate, mock_weather_data):
        await self.weather_data_detail.query_mount('name_station', 'a', 0, 1)
        self.assertTrue(mock_paginate.called)
        self.assertTrue(mock_weather_data.called)

    @mock.patch('weather.integration.weather_data_detail.WeatherData')
    @mock.patch('weather.integration.weather_data_detail.Weather')
    @gen_test
    async def test_query_mount_exception(self, mock_weather, mock_weather_data):
        with self.assertRaises(HTTPClientError) as context:
            await self.weather_data_detail.query_mount('unknown_name', 'a', 0, 1)
        self.assertTrue(mock_weather_data.called)
        self.assertTrue('not found in model Weather' in str(context.exception))

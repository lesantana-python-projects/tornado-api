import mock
from sqlalchemy.exc import IntegrityError
from tornado.concurrent import Future
from tornado.testing import gen_test
from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration.weather_data import WeatherDataController
from weather.models.model_base import ModelBase


@mock.patch('weather.integration.weather_data.logger', mock.MagicMock())
class TestWeatherDataController(BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestWeatherDataController, self).setUp()
        self.weather_data_controller = WeatherDataController()
        self.expected_response = {
            "id": 10,
            "date": "1976-09-04",
            "hour": "0",
            "precipitation": None,
            "dry_bulb_temperature": 21.4,
            "high_temperature": 34.5,
            "low_temperature": None,
            "relative_humidity": 62,
            "relative_humidity_avg": 24.36,
            "pressure": 976.9,
            "sea_pressure": None,
            "wind_direction": 23,
            "wind_speed_avg": 49,
            "cloud_cover": 10.6,
            "evaporation": None,
            "name_station": "ALTO PARNAIBA"
        }

    @gen_test
    async def test_process(self):
        message = 'anything'
        future_1 = Future()
        future_1.set_result(message)

        self.weather_data_controller._run_process = mock.MagicMock(return_value=future_1)
        response = await self.weather_data_controller.process(params={})

        self.assertEqual(message, response)

    @mock.patch('weather.integration.weather_data.parser')
    @gen_test
    async def test_agreement(self, mock_parser):
        mock_parser.parse.return_value = self.expected_response
        response = await self.weather_data_controller.agreement('request')

        self.assertEqual(self.expected_response, response)

    @mock.patch('weather.integration.weather_data.weather_data_response')
    @gen_test
    async def test_method_get(self, mock_weather_data_response):
        self.weather_data_controller.model = mock.MagicMock()
        mock_weather_data_response.return_value = self.expected_response
        response = await self.weather_data_controller.method_get(id=1)
        self.assertEqual(self.expected_response, response)

    @mock.patch('weather.integration.weather_data.weather_data_response')
    @gen_test
    async def test_method_put_success(self, mock_weather_data_response):
        self.weather_data_controller.model = mock.MagicMock()
        mock_weather_data_response.return_value = self.expected_response
        response = await self.weather_data_controller.method_put(id=1)
        self.assertEqual(self.expected_response, response)

    @mock.patch('weather.integration.weather_data.default_exception_error')
    @mock.patch('weather.integration.weather_data.weather_data_response')
    @gen_test
    async def test_method_put_error(self, mock_weather_data_response, mock_default_exception_error):
        self.weather_data_controller.model = mock.MagicMock(KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY)

        future_1 = Future()
        future_1.set_result(mock.MagicMock(update=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock'))))

        future_2 = Future()
        future_2.set_result(mock.MagicMock())

        self.weather_data_controller._get_object_weather_data = mock.MagicMock(return_value=future_1)
        self.weather_data_controller._get_object_weather_data_join = mock.MagicMock(return_value=future_2)

        await self.weather_data_controller.method_put(id=1)
        self.assertTrue(mock_default_exception_error.called)
        self.assertTrue(mock_weather_data_response.called)

    @gen_test
    async def test_method_delete_success(self):
        self.weather_data_controller.model = mock.MagicMock()

        response = await self.weather_data_controller.method_delete(id=1)
        self.assertEqual('object deleted successfully', response)

    @mock.patch('weather.integration.weather_data.default_exception_error')
    @gen_test
    async def test_method_delete_error(self, mock_default_exception_error):
        self.weather_data_controller.model = mock.MagicMock(
            KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY)

        future_1 = Future()
        future_1.set_result(mock.MagicMock(first=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock'))))

        self.weather_data_controller._get_object_weather_data = mock.MagicMock(return_value=future_1)

        await self.weather_data_controller.method_delete(id=1)
        self.assertTrue(mock_default_exception_error.called)

    @gen_test
    async def test_method_post_success(self):
        self.weather_data_controller.model = mock.MagicMock()

        response = await self.weather_data_controller.method_post(id=1)
        self.assertEqual('object created successfully', response)

    @mock.patch('weather.integration.weather_data.default_exception_error')
    @gen_test
    async def test_method_post_error(self, mock_default_exception_error):
        self.weather_data_controller.model = mock.MagicMock(
            KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY,
            orm=mock.MagicMock(object_commit=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock')))
        )
        await self.weather_data_controller.method_post(id=1)
        self.assertTrue(mock_default_exception_error.called)

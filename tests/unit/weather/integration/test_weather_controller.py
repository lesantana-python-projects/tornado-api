import mock
from sqlalchemy.exc import IntegrityError

from tornado.concurrent import Future
from tornado.testing import gen_test
from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration.weather import WeatherController
from weather.models.model_base import ModelBase


@mock.patch('weather.integration.weather.logger', mock.MagicMock())
class TestWeatherController(BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestWeatherController, self).setUp()
        self.weather_controller = WeatherController()
        self.expected_response = {
            "id": 59999,
            "name_station": "ALTO PARNAIBA",
            "latitude": "-9.1",
            "longitude": "-45.9333"
        }

    @gen_test
    async def test_process(self):
        message = 'anything'
        future_1 = Future()
        future_1.set_result(message)

        self.weather_controller._run_process = mock.MagicMock(return_value=future_1)
        response = await self.weather_controller.process(params={})

        self.assertEqual(message, response)

    @mock.patch('weather.integration.weather.parser')
    @gen_test
    async def test_agreement(self, mock_parser):
        expected_response = {'latitude': '1', 'longitude': '2', 'name_station': 'anything'}

        mock_parser.parse.return_value = expected_response
        response = await self.weather_controller.agreement('request')

        self.assertEqual(expected_response, response)

    @mock.patch('weather.integration.weather.weather_response')
    @gen_test
    async def test_method_get(self, mock_weather_response):
        self.weather_controller.model = mock.MagicMock()

        mock_weather_response.return_value = self.expected_response
        response = await self.weather_controller.method_get(id=1)
        self.assertEqual(self.expected_response, response)

    @mock.patch('weather.integration.weather.weather_response')
    @gen_test
    async def test_method_put_success(self, mock_weather_response):
        self.weather_controller.model = mock.MagicMock()

        mock_weather_response.return_value = self.expected_response
        response = await self.weather_controller.method_put(id=1)
        self.assertEqual(self.expected_response, response)

    @mock.patch('weather.integration.weather.default_exception_error')
    @mock.patch('weather.integration.weather.weather_response')
    @gen_test
    async def test_method_put_error(self, mock_weather_response, mock_default_exception_error):
        self.weather_controller.model = mock.MagicMock(KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY)

        future_1 = Future()
        future_1.set_result(mock.MagicMock(update=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock'))))

        self.weather_controller._get_object_weather = mock.MagicMock(return_value=future_1)

        await self.weather_controller.method_put(id=1)
        self.assertTrue(mock_default_exception_error.called)
        self.assertTrue(mock_weather_response.called)

    @gen_test
    async def test_method_delete_success(self):
        self.weather_controller.model = mock.MagicMock()

        response = await self.weather_controller.method_delete(id=1)
        self.assertEqual('object deleted successfully', response)

    @mock.patch('weather.integration.weather.default_exception_error')
    @gen_test
    async def test_method_delete_error(self, mock_default_exception_error):
        self.weather_controller.model = mock.MagicMock(
            KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY)

        future_1 = Future()
        future_1.set_result(mock.MagicMock(first=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock'))))

        self.weather_controller._get_object_weather = mock.MagicMock(return_value=future_1)

        await self.weather_controller.method_delete(id=1)
        self.assertTrue(mock_default_exception_error.called)

    @gen_test
    async def test_method_post_success(self):
        self.weather_controller.model = mock.MagicMock()

        response = await self.weather_controller.method_post(id=1)
        self.assertEqual('object created successfully', response)

    @mock.patch('weather.integration.weather.default_exception_error')
    @gen_test
    async def test_method_post_error(self, mock_default_exception_error):
        self.weather_controller.model = mock.MagicMock(
            KNOWN_ERROR_SQLALCHEMY=ModelBase().KNOWN_ERROR_SQLALCHEMY,
            orm=mock.MagicMock(object_commit=mock.MagicMock(side_effect=IntegrityError('mock', 'mock', 'mock')))
        )
        await self.weather_controller.method_post(id=1)
        self.assertTrue(mock_default_exception_error.called)

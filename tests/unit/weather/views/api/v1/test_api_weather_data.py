import json
import logging
import mock
from http import HTTPStatus

from tornado.concurrent import Future
from tornado.httpclient import HTTPError

from tests.unit.weather import BaseAsyncHttpTestCase, MixinTest
from weather.exceptions import CustomDatabaseError

logger = logging.getLogger(__name__)


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDataDetail(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherDataDetail, self).setUp()
        self.url = '/api/v1/weather-data/list?target=name_station&value=a&page=1&page_size=1'

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.Instance())
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_error_internal_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = Exception('mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.INTERNAL_SERVER_ERROR.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDataEdit(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherDataEdit, self).setUp()
        self.url = '/api/v1/weather-data/20'

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.InstanceWeatherDataEdit())
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_get_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_put_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.InstanceWeatherDataEdit())
        response = self.fetch(self.url, raise_error=False, method="PUT", body=json.dumps({}))
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_put_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="PUT", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_put_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="PUT", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_delete_on_success(self, mock_base_default_factory):
        message = 'object deleted successfully'
        mock_base_default_factory.get_instance = mock.MagicMock(
            return_value=self.InstanceWeatherDataEdit(mock_result=message))
        response = self.fetch(self.url, raise_error=False, method="DELETE")

        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertEqual(message, json.loads(response.body.decode()).get('result'))

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_delete_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="DELETE")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_delete_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="DELETE")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDataAdd(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherDataAdd, self).setUp()
        self.url = '/api/v1/weather-data'

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_post_on_success(self, mock_base_default_factory):
        post = {
            "date": "2020-10-10",
            "hour": 0,
            "precipitation": 0,
            "dry_bulb_temperature": 0,
            "wet_bulb_temperature": 0,
            "high_temperature": 0,
            "low_temperature": 0,
            "relative_humidity": 0,
            "relative_humidity_avg": 0,
            "pressure": 0,
            "sea_pressure": 0,
            "wind_direction": 0,
            "wind_speed_avg": 0,
            "cloud_cover": 0,
            "evaporation": 0,
            "weather_id": 59999
        }
        message = "object created successfully"
        mock_base_default_factory.get_instance = mock.MagicMock(
            return_value=self.InstanceWeatherDataEdit(mock_result=message))
        response = self.fetch(self.url, raise_error=False, method='POST', body=json.dumps(post))

        self.assertEqual(HTTPStatus.CREATED.value, response.code)
        self.assertEqual(message, json.loads(response.body.decode()).get('result'))

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_post_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="POST", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather_data.BaseDefaultFactory')
    def test_method_post_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="POST", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

import json
import mock
from http import HTTPStatus

from tornado.httpclient import HTTPError
from tornado.concurrent import Future
from tests.unit.weather import BaseAsyncHttpTestCase, MixinTest
from weather.exceptions import CustomDatabaseError


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDetail(MixinTest, BaseAsyncHttpTestCase):
    def setUp(self):
        super(TestApiWeatherDetail, self).setUp()
        self.url = '/api/v1/weather/list?target=id&value=1&page=1&page_size=1'

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.Instance())
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_error_internal_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = Exception('mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.INTERNAL_SERVER_ERROR.value)

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherEdit(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherEdit, self).setUp()
        self.url = '/api/v1/weather/1'

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.InstanceEdit())
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_get_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_put_on_success(self, mock_base_default_factory):
        mock_base_default_factory.get_instance = mock.MagicMock(return_value=self.InstanceEdit())
        response = self.fetch(self.url, raise_error=False, method='PUT', body=json.dumps({}))

        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertIn('result', json.loads(response.body.decode()))

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_put_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="PUT", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_put_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="PUT", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_delete_on_success(self, mock_base_default_factory):
        message = 'object deleted successfully'
        mock_base_default_factory.get_instance = mock.MagicMock(
            return_value=self.InstanceEdit(mock_result=message))
        response = self.fetch(self.url, raise_error=False, method='DELETE')

        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertEqual(message, json.loads(response.body.decode()).get('result'))

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_delete_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="DELETE")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_delete_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="DELETE")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherAdd(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherAdd, self).setUp()
        self.url = '/api/v1/weather'

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_post_on_success(self, mock_base_default_factory):
        post = {
            "name_station": "teste",
            "latitude": 10.2,
            "longitude": 1.0
        }
        message = "object created successfully"
        mock_base_default_factory.get_instance = mock.MagicMock(
            return_value=self.InstanceEdit(mock_result=message))
        response = self.fetch(self.url, raise_error=False, method='POST', body=json.dumps(post))

        self.assertEqual(HTTPStatus.CREATED.value, response.code)
        self.assertEqual(message, json.loads(response.body.decode()).get('result'))

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_post_on_error_http(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = HTTPError(
            HTTPStatus.BAD_REQUEST.value, 'mock')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="POST", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

    @mock.patch('weather.views.api.v1.api_weather.BaseDefaultFactory')
    def test_method_post_on_known_error(self, mock_base_default_factory):
        mock_base_default_factory.get_instance().process.side_effect = CustomDatabaseError(message='mock error')

        future_1 = Future()
        future_1.set_result({})
        mock_base_default_factory.get_instance().agreement = mock.MagicMock(return_value=future_1)

        response = self.fetch(self.url, raise_error=False, method="POST", body=json.dumps({}))
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST.value)
        self.assertEqual(response.reason, 'Bad Request')

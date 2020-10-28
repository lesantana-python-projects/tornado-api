import json
import mock
from http import HTTPStatus

from tornado.httpclient import HTTPError

from tests.unit.weather import BaseAsyncHttpTestCase, MixinTest


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDetail(MixinTest, BaseAsyncHttpTestCase):
    def setUp(self):
        super(TestApiWeatherDetail, self).setUp()
        self.url = '/api/v1/weather?target=id&value=1&page=1&page_size=1'

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

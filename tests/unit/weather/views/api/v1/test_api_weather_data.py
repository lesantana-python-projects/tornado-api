import json
import logging
import mock
from http import HTTPStatus
from tornado.httpclient import HTTPError

from tests.unit.weather import BaseAsyncHttpTestCase, MixinTest

logger = logging.getLogger(__name__)


@mock.patch('weather.views.logger', mock.MagicMock())
class TestApiWeatherDataDetail(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestApiWeatherDataDetail, self).setUp()
        self.url = '/api/v1/weather-data?target=name_station&value=a&page=1&page_size=1'

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

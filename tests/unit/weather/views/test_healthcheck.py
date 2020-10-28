import json
from http import HTTPStatus

import mock

from tests.unit.weather import MixinTest, BaseAsyncHttpTestCase
from weather.views.healthcheck import HealthcheckApi


@mock.patch('weather.views.logger', mock.MagicMock())
class TestHealthCheck(MixinTest, BaseAsyncHttpTestCase):

    def setUp(self):
        super(TestHealthCheck, self).setUp()
        self.url = '/api/healthcheck'

    @mock.patch('weather.views.healthcheck.HealthCheck')
    def test_method_get(self, mock_health_check):
        mock_health_check().run.return_value = ['message', 200, 'headers']
        response = self.fetch(self.url, raise_error=False, method="GET")
        self.assertEqual(HTTPStatus.OK.value, response.code)

    @mock.patch('weather.views.healthcheck.DBDriver')
    def test_method_check_database_success(self, mock_db_driver):
        response = self.fetch(self.url, raise_error=False, method="GET")
        dict_response = json.loads(response.body)
        self.assertEqual(HTTPStatus.OK.value, response.code)
        self.assertEqual(dict_response.get('results')[0].get('output'), 'database ok')
        self.assertTrue(mock_db_driver.called)

    @mock.patch('weather.views.healthcheck.DBDriver')
    def test_method_check_database_error(self, mock_db_driver):
        mock_db_driver().db_engine.connect.side_effect = Exception('error')
        response = HealthcheckApi(application=mock.MagicMock(), request=mock.MagicMock()).check_database()
        self.assertFalse(response[0])
        self.assertEqual(response[1], 'error')

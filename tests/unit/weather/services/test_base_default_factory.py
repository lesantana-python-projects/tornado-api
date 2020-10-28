import mock
from tornado.httpclient import HTTPError

from tests.unit.weather import BaseTests
from weather.services.base_factory import BaseDefaultFactory


@mock.patch('weather.services.base_factory.logger', mock.MagicMock())
class TestBaseDefaultFactory(BaseTests):

    def test_get_instance_return_class(self):
        carrier = 'weather_detail'
        target_class = 'WeatherDetail'
        instance = BaseDefaultFactory.get_instance(carrier=carrier)
        self.assertEqual(instance.carrier, carrier)
        self.assertEqual(instance.__class__.__name__, target_class)

    @mock.patch('weather.services.base_factory.ServiceBase')
    def test_get_instance_return_http_error(self, mock_service_base):
        with self.assertRaises(HTTPError) as context:
            mock_service_base.__class__.__subclasses__ = mock.MagicMock(return_value=[])
            BaseDefaultFactory.get_instance(carrier='nothing')

        self.assertTrue('instance not found' in str(context.exception))

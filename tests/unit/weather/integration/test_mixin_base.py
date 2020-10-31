from tornado.concurrent import Future
from tornado.httpclient import HTTPError
from tornado.testing import gen_test

from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration import MixinBase
import mock

from weather.integration.weather_data import WeatherDataController


class TestMixinBase(BaseAsyncHttpTestCase):
    @mock.patch.multiple(MixinBase, __abstractmethods__=set())
    def setUp(self):
        super(TestMixinBase, self).setUp()
        self.weather_data_controller = WeatherDataController()

    @gen_test
    async def test_run_process_success(self):
        message = 'object deleted successfully'
        future_1 = Future()
        future_1.set_result(message)
        self.weather_data_controller.method_delete = mock.MagicMock(return_value=future_1)

        response = await self.weather_data_controller.process(params={}, method='DELETE')
        self.assertEqual(message, response)

    @gen_test
    async def test_run_process_error(self):
        with self.assertRaises(HTTPError) as context:
            await self.weather_data_controller.process(params={}, method='error')
        self.assertEqual('controller to method error not found', context.exception.message)

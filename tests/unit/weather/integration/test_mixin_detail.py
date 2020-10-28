import mock
from tornado.concurrent import Future
from tornado.testing import gen_test
from tests.unit.weather import BaseAsyncHttpTestCase
from weather.integration import MixinDetail


class TestMixinDetail(BaseAsyncHttpTestCase):

    @mock.patch.multiple(MixinDetail, __abstractmethods__=set())
    def setUp(self):
        super(TestMixinDetail, self).setUp()
        self.mixin_detail = MixinDetail()

    @mock.patch('weather.integration.parser')
    @mock.patch('weather.integration.fields')
    @gen_test
    async def test_agreement(self, mock_fields, mock_parser):
        my_response = {'target': '', 'value': '', 'page': '', 'page_size': ''}

        mock_parser.parse = mock.MagicMock(return_value=my_response)
        response = await self.mixin_detail.agreement(request=mock.MagicMock())
        self.assertEqual(my_response, response)
        self.assertTrue(mock_fields.Str.called)
        self.assertTrue(mock_fields.Int.called)

    @gen_test
    async def test_run_process(self):
        future_1 = Future()
        future_1.set_result(mock.MagicMock(total=10, next_page=2, previous_page=1, items=[]))
        self.mixin_detail.query_mount = mock.MagicMock(return_value=future_1)

        future_2 = Future()
        future_2.set_result([])
        self.mixin_detail.result_mount = mock.MagicMock(return_value=future_2)

        response = await self.mixin_detail._run_process(params={})
        self.assertTrue(response.get('resultsCount') == 10)
        self.assertTrue(response.get('next_page') == 2)
        self.assertTrue(response.get('previous_page') == 1)
        self.assertTrue(response.get('data') == [])

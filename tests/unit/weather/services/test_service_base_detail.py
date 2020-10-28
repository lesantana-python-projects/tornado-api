import mock

from tests.unit.weather import BaseTests
from weather.services import ServiceBaseDetail


class TestServiceBaseDetail(BaseTests):

    @mock.patch.multiple(ServiceBaseDetail, __abstractmethods__=set())
    def test_validate_process(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceBaseDetail()
            base_default.query_mount('target', 'value', 'page', 'size')
        self.assertTrue('Implement me' in str(context.exception))

    @mock.patch.multiple(ServiceBaseDetail, __abstractmethods__=set())
    def test_validate_agreement(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceBaseDetail()
            base_default.result_mount(obj='')
        self.assertTrue('Implement me' in str(context.exception))

import mock

from tests.unit.weather import BaseTests
from weather.services import ServiceHTTPCommon


class TestServiceHTTPCommon(BaseTests):

    @mock.patch.multiple(ServiceHTTPCommon, __abstractmethods__=set())
    def test_validate_method_get(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceHTTPCommon()
            base_default.method_get(params='')
        self.assertTrue('Implement me' in str(context.exception))

    @mock.patch.multiple(ServiceHTTPCommon, __abstractmethods__=set())
    def test_validate_method_post(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceHTTPCommon()
            base_default.method_post(params='')
        self.assertTrue('Implement me' in str(context.exception))

    @mock.patch.multiple(ServiceHTTPCommon, __abstractmethods__=set())
    def test_validate_method_delete(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceHTTPCommon()
            base_default.method_delete(params='')
        self.assertTrue('Implement me' in str(context.exception))

    @mock.patch.multiple(ServiceHTTPCommon, __abstractmethods__=set())
    def test_validate_method_put(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceHTTPCommon()
            base_default.method_put(params='')
        self.assertTrue('Implement me' in str(context.exception))

import mock

from tests.unit.weather import BaseTests
from weather.services import ServiceBase


class TestServiceBase(BaseTests):

    @mock.patch.multiple(ServiceBase, __abstractmethods__=set())
    def test_validate_process(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceBase()
            base_default.process(params='')
        self.assertTrue('Implement me' in str(context.exception))

    @mock.patch.multiple(ServiceBase, __abstractmethods__=set())
    def test_validate_agreement(self):
        with self.assertRaises(NotImplementedError) as context:
            base_default = ServiceBase()
            base_default.agreement(request='')
        self.assertTrue('Implement me' in str(context.exception))

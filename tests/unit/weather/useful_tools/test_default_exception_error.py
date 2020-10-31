import mock

from tests.unit.weather import BaseTests
from weather.exceptions import CustomDatabaseError
from weather.useful_tools.controller_util import default_exception_error


class TestDefaultExceptionError(BaseTests):

    @mock.patch('weather.useful_tools.controller_util.logger')
    def test_default_exception_error(self, mock_logger):
        param_mock = mock.MagicMock()

        with self.assertRaises(CustomDatabaseError):
            default_exception_error(model=param_mock, error=param_mock)
        self.assertTrue(mock_logger.error.called)

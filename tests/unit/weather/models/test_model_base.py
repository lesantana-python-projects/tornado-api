import mock

from tests.unit.weather import BaseTests
from weather.models.model_base import ModelBase


class TestModelBase(BaseTests):
    @mock.patch('weather.models.model_base.DBDriver')
    def test_instance_orm(self, mock_db_driver):
        model_base = ModelBase()
        model_base.orm
        self.assertTrue(mock_db_driver.called)

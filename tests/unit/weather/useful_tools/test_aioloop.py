from tests.unit.weather import BaseTests
from weather.useful_tools.aioloop import execute_ioloop


class TestAioLoop(BaseTests):

    @staticmethod
    def __method_to_test_aioloop(value):
        return ['anything', value]

    def test_execute_ioloop(self):
        response = execute_ioloop(self.__method_to_test_aioloop, '1958')
        self.assertEqual(str(response), '<Future pending>')

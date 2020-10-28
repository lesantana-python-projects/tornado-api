from tests.unit.weather import BaseTests
from weather.models.weather import Weather


class TestModelWeather(BaseTests):

    def test_model_weather_get_table_name(self):
        weather = Weather()
        response = weather.get_table_name
        self.assertEqual(response, 'weather')

    def test_model_weather_get_schema_name(self):
        weather = Weather()
        response = weather.get_schema_name
        self.assertIsNotNone(response)

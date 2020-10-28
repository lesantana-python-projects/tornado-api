from tests.unit.weather import BaseTests
from weather.models.weather_data import WeatherData


class TestModelWeatherData(BaseTests):

    def test_model_weather_data_get_table_name(self):
        weather = WeatherData()
        response = weather.get_table_name
        self.assertEqual(response, 'weather_data')

    def test_model_weather_data_get_schema_name(self):
        weather = WeatherData()
        response = weather.get_schema_name
        self.assertIsNotNone(response)

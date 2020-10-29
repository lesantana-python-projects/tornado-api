import logging

from weather.exceptions import CustomDatabaseError

logger = logging.getLogger(__name__)


def weather_response(obj):
    return {'id': obj.id,
            'name_station': str(obj.name_station),
            'latitude': str(obj.latitude),
            'longitude': str(obj.longitude)}


def weather_data_response(obj):
    return {
        'id': obj.WeatherData.id,
        'date': str(obj.WeatherData.date),
        'hour': str(obj.WeatherData.hour),
        'precipitation': float(obj.WeatherData.precipitation) if obj.WeatherData.precipitation else None,
        'dry_bulb_temperature': float(
            obj.WeatherData.dry_bulb_temperature) if obj.WeatherData.dry_bulb_temperature else None,
        'high_temperature': float(obj.WeatherData.high_temperature) if obj.WeatherData.high_temperature else None,
        'low_temperature': float(obj.WeatherData.low_temperature) if obj.WeatherData.low_temperature else None,
        'relative_humidity': float(
            obj.WeatherData.relative_humidity) if obj.WeatherData.relative_humidity else None,
        'relative_humidity_avg': float(
            obj.WeatherData.relative_humidity_avg) if obj.WeatherData.relative_humidity_avg else None,
        'pressure': float(obj.WeatherData.pressure) if obj.WeatherData.pressure else None,
        'sea_pressure': float(obj.WeatherData.sea_pressure) if obj.WeatherData.sea_pressure else None,
        'wind_direction': float(obj.WeatherData.wind_direction) if obj.WeatherData.wind_direction else None,
        'wind_speed_avg': float(obj.WeatherData.wind_speed_avg) if obj.WeatherData.wind_speed_avg else None,
        'cloud_cover': float(obj.WeatherData.cloud_cover) if obj.WeatherData.cloud_cover else None,
        'evaporation': float(obj.WeatherData.evaporation) if obj.WeatherData.evaporation else None,
        'name_station': str(obj.Weather.name_station)
    }


def default_exception_error(model, error):
    logger.error(str(error))
    model.orm.remove_session()
    raise CustomDatabaseError(message=model.KNOWN_ERROR_SQLALCHEMY.get('friendly_message'))

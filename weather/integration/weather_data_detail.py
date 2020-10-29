import logging

from tornado.httpclient import HTTPError
from http import HTTPStatus
from weather.integration import MixinDetail
from weather.models.weather import Weather
from weather.models.weather_data import WeatherData
from sqlalchemy import func
from weather.services import ServiceBase
from weather.services.paginator import paginate
from weather.useful_tools.controller_util import weather_data_response

logger = logging.getLogger(__name__)


class WeatherDataDetail(MixinDetail, ServiceBase):
    carrier = 'weather_data_detail'

    async def query_mount(self, target, value, page, size):
        """ query mount Weather Detail """
        model = WeatherData()
        query = model.orm.db_session.query(WeatherData, Weather).join(Weather)

        condition = {
            "date": query.filter(WeatherData.date == value),
            "hour": query.filter(WeatherData.hour == value),
            "precipitation": query.filter(WeatherData.precipitation == value),
            "dry_bulb_temperature": query.filter(WeatherData.precipitation == value),
            "wet_bulb_temperature": query.filter(WeatherData.wet_bulb_temperature == value),
            "high_temperature": query.filter(WeatherData.high_temperature == value),
            "low_temperature": query.filter(WeatherData.low_temperature == value),
            "relative_humidity": query.filter(WeatherData.relative_humidity == value),
            "relative_humidity_avg": query.filter(WeatherData.relative_humidity_avg == value),
            "pressure": query.filter(WeatherData.pressure == value),
            "sea_pressure": query.filter(WeatherData.sea_pressure == value),
            "wind_direction": query.filter(WeatherData.wind_direction == value),
            "wind_speed_avg": query.filter(WeatherData.wind_speed_avg == value),
            "evaporation": query.filter(WeatherData.evaporation == value),
            "name_station": query.filter(func.lower(Weather.name_station).like("%{}%".format(value))),
            "id": query.filter(WeatherData.id == value),
        }

        if target not in condition:
            message = 'target "{}" not found in model WeatherData'.format(target)
            logger.error(message)
            raise HTTPError(code=HTTPStatus.BAD_REQUEST.value, message=message)

        result = paginate(condition[target], page, size)
        model.orm.remove_session()
        return result

    async def result_mount(self, obj):
        """ result mount """
        return weather_data_response(obj)

    async def process(self, params):
        """ default process"""
        return await self._run_process(params)
